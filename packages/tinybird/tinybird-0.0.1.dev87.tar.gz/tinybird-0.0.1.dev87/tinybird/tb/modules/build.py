import asyncio
import json
import logging
import sys
import threading
import time
from functools import partial
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlencode

import click
import requests

from tinybird.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import push_data
from tinybird.tb.modules.datafile.build import folder_build
from tinybird.tb.modules.datafile.fixture import get_fixture_dir, persist_fixture
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.shell import Shell, print_table_formatted
from tinybird.tb.modules.watch import watch_project


@cli.command()
@click.option("--watch", is_flag=True, default=False, help="Watch for changes and rebuild automatically")
@click.pass_context
def build(ctx: click.Context, watch: bool) -> None:
    """
    Validate and build the project server side.
    """
    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    click.echo(FeedbackManager.highlight_building_project())
    process(project=project, tb_client=tb_client, watch=False)
    if watch:
        run_watch(
            project=project,
            tb_client=tb_client,
            process=partial(process, project=project, tb_client=tb_client, watch=True),
        )


@cli.command("dev", help="Build the project server side and watch for changes.")
@click.pass_context
def dev(ctx: click.Context) -> None:
    project: Project = ctx.ensure_object(dict)["project"]
    tb_client: TinyB = ctx.ensure_object(dict)["client"]
    click.echo(FeedbackManager.highlight_building_project())
    process(project=project, tb_client=tb_client, watch=True)
    run_watch(project=project, tb_client=tb_client, process=partial(process, project=project, tb_client=tb_client))


def build_project(project: Project, tb_client: TinyB, file_changed: Optional[str] = None) -> None:
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }
    TINYBIRD_API_URL = tb_client.host + "/v1/build"
    logging.debug(TINYBIRD_API_URL)
    TINYBIRD_API_KEY = tb_client.token
    error: Optional[str] = None
    try:
        files = [
            ("context://", ("cli-version", "1.0.0", "text/plain")),
        ]
        fds = []
        project_path = project.path
        project_files = project.get_project_files()

        if not project_files:
            return

        for file_path in project_files:
            relative_path = str(Path(file_path).relative_to(project_path))
            fd = open(file_path, "rb")
            fds.append(fd)
            content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
            files.append((MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd.read().decode("utf-8"), content_type)))
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS)
        try:
            result = r.json()
        except Exception as e:
            logging.debug(e, exc_info=True)
            click.echo(FeedbackManager.error(message="Couldn't parse response from server"))
            sys.exit(1)

        logging.debug(json.dumps(result, indent=2))

        build_result = result.get("result")
        if build_result == "success":
            build = result.get("build")
            datasources = build.get("new_datasource_names", [])
            pipes = build.get("new_pipe_names", [])
            if not file_changed:
                for ds in datasources:
                    ds_path_str: Optional[str] = next(
                        (p for p in project_files if p.endswith(ds + ".datasource")), None
                    )
                    if ds_path_str:
                        ds_path = Path(ds_path_str)
                        ds_path_str = ds_path_str.replace(f"{project.folder}/", "")
                        click.echo(FeedbackManager.info(message=f"✓ {ds_path_str} created"))
                for pipe in pipes:
                    pipe_name = pipe
                    pipe_path_str: Optional[str] = next(
                        (p for p in project_files if p.endswith(pipe_name + ".pipe")), None
                    )
                    if pipe_path_str:
                        pipe_path_str = pipe_path_str.replace(f"{project.folder}/", "")
                        click.echo(FeedbackManager.info(message=f"✓ {pipe_path_str} created"))

            try:
                for filename in project_files:
                    if filename.endswith(".datasource"):
                        ds_path = Path(filename)
                        ds_name = ds_path.stem
                        fixture_folder = get_fixture_dir(project.folder)
                        fixture_path = fixture_folder / f"{ds_name}.ndjson"
                        if fixture_path.exists():
                            append_fixture(tb_client, ds_name, str(fixture_path))

            except Exception as e:
                click.echo(FeedbackManager.error_exception(error=f"Error appending fixtures for '{ds_name}': {e}"))

            feedback = result.get("feedback", [])
            for f in feedback:
                click.echo(
                    FeedbackManager.warning(message=f"△ {f.get('level')}: {f.get('resource')}: {f.get('message')}")
                )
        elif build_result == "failed":
            build_errors = result.get("errors")
            error_msg = None
            for build_error in build_errors:
                filename_bit = f"{build_error.get('filename', '')}"
                error_bit = build_error.get("error") or build_error.get("message") or ""
                error_msg = ((filename_bit + "\n\n") if filename_bit else "") + error_bit
            error = error_msg or "Unknown build error"
        else:
            error = f"Unknown build result. Error: {result.get('error')}"
    except Exception as e:
        error = str(e)
    finally:
        for fd in fds:
            fd.close()
        if error:
            raise click.ClickException(error)


def append_fixture(
    tb_client: TinyB,
    datasource_name: str,
    url: str,
):
    asyncio.run(
        push_data(
            tb_client,
            datasource_name,
            url,
            mode="append",
            concurrency=1,
            silent=True,
        )
    )


def rebuild_fixture(project: Project, tb_client: TinyB, fixture: str) -> None:
    try:
        fixture_path = Path(fixture)
        datasources_path = Path(project.folder) / "datasources"
        ds_name = fixture_path.stem

        if ds_name not in project.datasources:
            try:
                ds_name = "_".join(fixture_path.stem.split("_")[:-1])
            except Exception:
                pass

        ds_path = datasources_path / f"{ds_name}.datasource"

        if ds_path.exists():
            asyncio.run(tb_client.datasource_truncate(ds_name))
            append_fixture(tb_client, ds_name, str(fixture_path))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))


def show_data(tb_client: TinyB, filename: str, diff: Optional[str] = None):
    table_name = diff
    resource_path = Path(filename)
    resource_name = resource_path.stem
    resource_content = resource_path.read_text()

    pipeline = resource_name if filename.endswith(".pipe") else None

    if not table_name:
        table_name = resource_name

    sql = f"SELECT * FROM {table_name} FORMAT JSON"

    res = asyncio.run(tb_client.query(sql, pipeline=pipeline))
    print_table_formatted(res, table_name)
    if Project.is_endpoint(resource_content):
        example_params = {
            "format": "json",
            "pipe": resource_name,
            "q": "",
            "token": tb_client.token,
        }
        endpoint_url = asyncio.run(tb_client._req(f"/examples/query.http?{urlencode(example_params)}"))
        if endpoint_url:
            endpoint_url = endpoint_url.replace("http://localhost:8001", tb_client.host)
            click.echo(FeedbackManager.gray(message="\nTest endpoint at ") + FeedbackManager.info(message=endpoint_url))


def process(
    project: Project, tb_client: TinyB, watch: bool, file_changed: Optional[str] = None, diff: Optional[str] = None
) -> None:
    time_start = time.time()
    build_failed = False
    if file_changed and file_changed.endswith(".ndjson"):
        rebuild_fixture(project, tb_client, file_changed)
    elif file_changed and file_changed.endswith(".sql"):
        rebuild_fixture_sql(project, tb_client, file_changed)
    else:
        try:
            build_project(project, tb_client, file_changed)
        except click.ClickException as e:
            click.echo(FeedbackManager.error(message=e))
            build_failed = True
        try:
            if file_changed and not build_failed:
                asyncio.run(folder_build(project, tb_client, filenames=[file_changed]))
                show_data(tb_client, file_changed, diff)
        except Exception:
            pass

    time_end = time.time()
    elapsed_time = time_end - time_start

    rebuild_str = "Rebuild" if watch and file_changed else "Build"
    if build_failed:
        click.echo(FeedbackManager.error(message=f"\n✗ {rebuild_str} failed"))
        if not watch:
            sys.exit(1)
    else:
        click.echo(FeedbackManager.success(message=f"\n✓ {rebuild_str} completed in {elapsed_time:.1f}s"))


def run_watch(
    project: Project, tb_client: TinyB, process: Callable[[bool, Optional[str], Optional[str]], None]
) -> None:
    shell = Shell(project=project, tb_client=tb_client, playground=False)
    click.echo(FeedbackManager.gray(message="\nWatching for changes..."))
    watcher_thread = threading.Thread(
        target=watch_project,
        args=(shell, process, project),
        daemon=True,
    )
    watcher_thread.start()
    shell.run()


def rebuild_fixture_sql(project: Project, tb_client: TinyB, sql_file: str) -> None:
    sql_path = Path(sql_file)
    datasource_name = sql_path.stem
    sql = sql_path.read_text()
    result = asyncio.run(tb_client.query(f"{sql} FORMAT JSON"))
    data = result.get("data", [])
    persist_fixture(datasource_name, data, project.folder)
