# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import logging
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import click
import humanfriendly
from click import Context

from tinybird.client import (
    AuthException,
    AuthNoTokenException,
    TinyB,
)
from tinybird.config import get_config
from tinybird.tb import __cli__
from tinybird.tb.modules.common import (
    CatchAuthExceptions,
    CLIException,
    _get_tb_client,
    coro,
    echo_safe_format_table,
    get_current_main_workspace,
    getenv_bool,
    try_update_config_with_remote,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.build import build_graph
from tinybird.tb.modules.datafile.diff import diff_command
from tinybird.tb.modules.datafile.pull import folder_pull
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.project import Project

__old_click_echo = click.echo
__old_click_secho = click.secho
DEFAULT_PATTERNS: List[Tuple[str, Union[str, Callable[[str], str]]]] = [
    (r"p\.ey[A-Za-z0-9-_\.]+", lambda v: f"{v[:4]}...{v[-8:]}")
]
VERSION = f"{__cli__.__version__} (rev {__cli__.__revision__})"


@click.group(cls=CatchAuthExceptions, context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("--token", help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file.")
@click.option("--host", help="Use custom host, defaults to TB_HOST envvar, then to https://api.tinybird.co")
@click.option("--show-tokens", is_flag=True, default=False, help="Enable the output of tokens.")
@click.option("--cloud/--local", is_flag=True, default=False, help="Run against cloud or local.")
@click.option("--build", is_flag=True, default=False, help="Run against build mode.")
@click.option("--staging", is_flag=True, default=False, help="Run against a staging deployment.")
@click.version_option(version=VERSION)
@click.pass_context
@coro
async def cli(
    ctx: Context,
    debug: bool,
    token: str,
    host: str,
    show_tokens: bool,
    cloud: bool,
    build: bool,
    staging: bool,
) -> None:
    """
    Use `OBFUSCATE_REGEX_PATTERN` and `OBFUSCATE_PATTERN_SEPARATOR` environment variables to define a regex pattern and a separator (in case of a single string with multiple regex) to obfuscate secrets in the CLI output.
    """
    # We need to unpatch for our tests not to break
    if show_tokens or not cloud or ctx.invoked_subcommand == "build" or build:
        __unpatch_click_output()
    else:
        __patch_click_output()

    if getenv_bool("TB_DISABLE_SSL_CHECKS", False):
        click.echo(FeedbackManager.warning_disabled_ssl_checks())

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    config_temp = CLIConfig.get_project_config()

    if token:
        config_temp.set_token(token)
    if host:
        config_temp.set_host(host)
    if token or host:
        await try_update_config_with_remote(config_temp, auto_persist=False, raise_on_errors=False)

    # Overwrite token and host with env vars manually, without resorting to click.
    #
    # We need this to avoid confusing the new config class about where are
    # token and host coming from (we need to show the proper origin in
    # `tb auth info`)
    if not token and "TB_TOKEN" in os.environ:
        token = os.environ.get("TB_TOKEN", "")
    if not host and "TB_HOST" in os.environ:
        host = os.environ.get("TB_HOST", "")

    config = await get_config(host, token, config_file=config_temp._path)
    client = _get_tb_client(config.get("token", None), config["host"])
    folder = os.path.join(config_temp._path.replace(".tinyb", ""), config.get("cwd", os.getcwd()))
    project = Project(folder=folder)
    config["path"] = str(project.path)
    # If they have passed a token or host as paramter and it's different that record in .tinyb, refresh the workspace id
    if token or host:
        try:
            workspace = await client.workspace_info()
            config["id"] = workspace.get("id", "")
            config["name"] = workspace.get("name", "")
        # If we can not get this info, we continue with the id on the file
        except (AuthNoTokenException, AuthException):
            pass

    ctx.ensure_object(dict)["config"] = config

    logging.debug("debug enabled")

    if "--help" in sys.argv or "-h" in sys.argv:
        return

    client = await create_ctx_client(ctx, config, cloud, build, staging)

    if client:
        ctx.ensure_object(dict)["client"] = client

    ctx.ensure_object(dict)["project"] = project
    ctx.ensure_object(dict)["env"] = get_target_env(cloud, build)


@cli.command(hidden=True)
@click.option("-f", "--force", is_flag=True, default=False, help="Override existing files")
@click.option("--fmt", is_flag=True, default=False, help="Format files before saving")
@click.pass_context
@coro
async def pull(ctx: Context, force: bool, fmt: bool) -> None:
    """Retrieve latest versions for project files from Tinybird."""

    client = ctx.ensure_object(dict)["client"]
    project = ctx.ensure_object(dict)["project"]

    return await folder_pull(client, project.path, force, fmt=fmt)


@cli.command(hidden=True)
@click.option("--no-deps", is_flag=True, default=False, help="Print only data sources with no pipes using them")
@click.option("--match", default=None, help="Retrieve any resource matching the pattern")
@click.option("--pipe", default=None, help="Retrieve any resource used by pipe")
@click.option("--datasource", default=None, help="Retrieve resources depending on this data source")
@click.option(
    "--check-for-partial-replace",
    is_flag=True,
    default=False,
    help="Retrieve dependant data sources that will have their data replaced if a partial replace is executed in the data source selected",
)
@click.option("--recursive", is_flag=True, default=False, help="Calculate recursive dependencies")
@click.pass_context
@coro
async def dependencies(
    ctx: Context,
    no_deps: bool,
    match: Optional[str],
    pipe: Optional[str],
    datasource: Optional[str],
    check_for_partial_replace: bool,
    recursive: bool,
) -> None:
    """Print all data sources dependencies."""

    client = ctx.ensure_object(dict)["client"]

    response = await client.datasource_dependencies(
        no_deps, match, pipe, datasource, check_for_partial_replace, recursive
    )
    for ds in response["dependencies"]:
        click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        for pipe in response["dependencies"][ds]:
            click.echo(FeedbackManager.info_dependency_list_item(dependency=pipe))
    if "incompatible_datasources" in response and len(response["incompatible_datasources"]):
        click.echo(FeedbackManager.info_no_compatible_dependencies_found())
        for ds in response["incompatible_datasources"]:
            click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        raise CLIException(FeedbackManager.error_partial_replace_cant_be_executed(datasource=datasource))


@cli.command(
    name="diff",
    short_help="Diff local datafiles to the corresponding remote files in the workspace. Only diffs VERSION and SCHEMA for .datasource files.",
)
@click.argument("filename", type=click.Path(exists=True), nargs=-1, required=False)
@click.option(
    "--fmt/--no-fmt",
    is_flag=True,
    default=True,
    help="Format files before doing the diff, default is True so both files match the format",
)
@click.option("--no-color", is_flag=True, default=False, help="Don't colorize diff")
@click.option(
    "--no-verbose", is_flag=True, default=False, help="List the resources changed not the content of the diff"
)
@click.option(
    "--main",
    is_flag=True,
    default=False,
    help="Diff local datafiles to the corresponding remote files in the main workspace. Only works when authenticated on a Branch.",
    hidden=True,
)
@click.pass_context
@coro
async def diff(
    ctx: Context, filename: Optional[Tuple], fmt: bool, no_color: bool, no_verbose: bool, main: bool
) -> None:
    only_resources_changed = no_verbose
    client: TinyB = ctx.ensure_object(dict)["client"]

    if not main:
        changed = await diff_command(
            list(filename) if filename else None, fmt, client, no_color, with_print=not only_resources_changed
        )
    else:
        config = CLIConfig.get_project_config()

        response = await client.user_workspaces_and_branches()
        ws_client = None
        for workspace in response["workspaces"]:
            if config["id"] == workspace["id"]:
                if not workspace.get("is_branch"):
                    raise CLIException(FeedbackManager.error_not_a_branch())

                origin = workspace["main"]
                workspace = await get_current_main_workspace(config)

                if not workspace:
                    raise CLIException(FeedbackManager.error_workspace(workspace=origin))

                ws_client = _get_tb_client(workspace["token"], config["host"])
                break

        if not ws_client:
            raise CLIException(FeedbackManager.error_workspace(workspace=origin))
        changed = await diff_command(
            list(filename) if filename else None, fmt, ws_client, no_color, with_print=not only_resources_changed
        )

    if only_resources_changed:
        click.echo("\n")
        for resource, status in dict(sorted(changed.items(), key=lambda item: str(item[1]))).items():
            if status is None:
                continue
            status = "changed" if status not in ["remote", "local", "shared"] else status
            click.echo(f"{status}: {resource}")


@cli.command()
@click.argument("query", required=False)
@click.option("--rows_limit", default=100, help="Max number of rows retrieved")
@click.option("--pipeline", default=None, help="The name of the pipe to run the SQL Query")
@click.option("--pipe", default=None, help="The path to the .pipe file to run the SQL Query of a specific NODE")
@click.option("--node", default=None, help="The NODE name")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json", "csv", "human"], case_sensitive=False),
    default="human",
    help="Output format",
)
@click.option("--stats/--no-stats", default=False, help="Show query stats")
@click.pass_context
@coro
async def sql(
    ctx: Context,
    query: str,
    rows_limit: int,
    pipeline: Optional[str],
    pipe: Optional[str],
    node: Optional[str],
    format_: str,
    stats: bool,
) -> None:
    """Run SQL query over data sources and pipes."""

    client = ctx.ensure_object(dict)["client"]
    req_format = "CSVWithNames" if format_ == "csv" else "JSON"
    res = None
    try:
        if query:
            q = query.lower().strip()
            if q.startswith("insert"):
                click.echo(FeedbackManager.info_append_data())
                raise CLIException(FeedbackManager.error_invalid_query())
            if q.startswith("delete"):
                raise CLIException(FeedbackManager.error_invalid_query())
            res = await client.query(
                f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline
            )
        elif pipe and node:
            filenames = [pipe]

            # build graph to get new versions for all the files involved in the query
            # dependencies need to be processed always to get the versions
            dependencies_graph = await build_graph(
                filenames,
                client,
                dir_path=".",
                process_dependencies=True,
                skip_connectors=True,
            )

            query = ""
            for _, elem in dependencies_graph.to_run.items():
                for _node in elem["nodes"]:
                    if _node["params"]["name"].lower() == node.lower():
                        query = "".join(_node["sql"])
            pipeline = pipe.split("/")[-1].split(".pipe")[0]
            res = await client.query(
                f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline
            )

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))

    if isinstance(res, dict) and "error" in res:
        raise CLIException(FeedbackManager.error_exception(error=res["error"]))

    if stats:
        stats_query = f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON"
        stats_res = await client.query(stats_query, pipeline=pipeline)
        stats_dict = stats_res["statistics"]
        seconds = stats_dict["elapsed"]
        rows_read = humanfriendly.format_number(stats_dict["rows_read"])
        bytes_read = humanfriendly.format_size(stats_dict["bytes_read"])
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

    if format_ == "csv":
        click.echo(res)
    elif isinstance(res, dict) and "data" in res and res["data"]:
        if format_ == "json":
            click.echo(json.dumps(res, indent=8))
        else:
            dd = []
            for d in res["data"]:
                dd.append(d.values())
            echo_safe_format_table(dd, columns=res["meta"])
    else:
        click.echo(FeedbackManager.info_no_rows())


def __patch_click_output():
    import re

    CUSTOM_PATTERNS: List[str] = []

    _env_patterns = os.getenv("OBFUSCATE_REGEX_PATTERN", None)
    if _env_patterns:
        CUSTOM_PATTERNS = _env_patterns.split(os.getenv("OBFUSCATE_PATTERN_SEPARATOR", "|"))

    def _obfuscate(msg: Any, *args: Any, **kwargs: Any) -> Any:
        for pattern in CUSTOM_PATTERNS:
            msg = re.sub(pattern, "****...****", str(msg))

        for pattern, substitution in DEFAULT_PATTERNS:
            if isinstance(substitution, str):
                msg = re.sub(pattern, substitution, str(msg))
            else:
                msg = re.sub(pattern, lambda m: substitution(m.group(0)), str(msg))  # noqa: B023
        return msg

    def _obfuscate_echo(msg: Any, *args: Any, **kwargs: Any) -> None:
        msg = _obfuscate(msg, *args, **kwargs)
        __old_click_echo(msg, *args, **kwargs)

    def _obfuscate_secho(msg: Any, *args: Any, **kwargs: Any) -> None:
        msg = _obfuscate(msg, *args, **kwargs)
        __old_click_secho(msg, *args, **kwargs)

    click.echo = lambda msg, *args, **kwargs: _obfuscate_echo(msg, *args, **kwargs)
    click.secho = lambda msg, *args, **kwargs: _obfuscate_secho(msg, *args, **kwargs)


def __unpatch_click_output():
    click.echo = __old_click_echo
    click.secho = __old_click_secho


async def create_ctx_client(ctx: Context, config: Dict[str, Any], cloud: bool, build: bool, staging: bool):
    commands_without_ctx_client = ["auth", "check", "login", "local", "update", "upgrade", "logout"]
    command = ctx.invoked_subcommand
    if command in commands_without_ctx_client:
        return None

    commands_always_cloud = ["pull", "playground"]
    commands_always_build = ["build", "test", "dev", "create"]
    commands_always_local: List[str] = []
    if (
        (cloud or command in commands_always_cloud)
        and command not in commands_always_local
        and command not in commands_always_build
    ):
        click.echo(
            FeedbackManager.gray(message=f"Running against Tinybird Cloud: Workspace {config.get('name', 'default')}")
        )
        return _get_tb_client(config.get("token", None), config["host"], staging=staging)
    build = command in commands_always_build or build
    if not build and command not in commands_always_local and command not in commands_always_build:
        click.echo(FeedbackManager.gray(message="Running against Tinybird Local\n"))
    return await get_tinybird_local_client(config, build=build, staging=staging)


def get_target_env(cloud: bool, build: bool) -> str:
    if cloud:
        return "cloud"
    if build:
        return "build"
    return "local"
