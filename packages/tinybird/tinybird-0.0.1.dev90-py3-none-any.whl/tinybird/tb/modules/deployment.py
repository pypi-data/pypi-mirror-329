import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import click
import requests

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_smart_table
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project


# TODO(eclbg): This should eventually end up in client.py, but we're not using it here yet.
def api_fetch(url: str, headers: dict) -> dict:
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    # Try to parse and print the error from the response
    try:
        result = r.json()
        error = result.get("error")
        logging.debug(json.dumps(result, indent=2))
        click.echo(FeedbackManager.error(message=f"Error: {error}"))
        sys.exit(1)
    except Exception:
        click.echo(FeedbackManager.error(message="Error parsing response from API"))
        sys.exit(1)


# TODO(eclbg): This logic should be in the server, and there should be a dedicated endpoint for promoting a deployment
# potato
def promote_deployment(host: Optional[str], headers: dict, wait: bool) -> None:
    TINYBIRD_API_URL = f"{host}/v1/deployments"
    r = requests.get(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))

    deployments = result.get("deployments")
    if not deployments:
        click.echo(FeedbackManager.error(message="No deployments found"))
        sys.exit(1)

    if len(deployments) < 2:
        click.echo(FeedbackManager.error(message="Only one deployment found"))
        sys.exit(1)

    last_deployment, candidate_deployment = deployments[0], deployments[1]

    if candidate_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Current deployment is not ready"))
        deploy_errors = candidate_deployment.get("errors", [])
        for deploy_error in deploy_errors:
            click.echo(FeedbackManager.error(message=f"* {deploy_error}"))
        sys.exit(1)

    if candidate_deployment.get("live"):
        click.echo(FeedbackManager.error(message="Candidate deployment is already live"))
    else:
        click.echo(FeedbackManager.success(message="Setting candidate deployment as live"))

        TINYBIRD_API_URL = f"{host}/v1/deployments/{candidate_deployment.get('id')}/set-live"
        r = requests.post(TINYBIRD_API_URL, headers=headers)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))
        if result.get("error"):
            click.echo(FeedbackManager.error(message=result.get("error")))
            sys.exit(1)

    click.echo(FeedbackManager.success(message="Removing old deployment"))

    TINYBIRD_API_URL = f"{host}/v1/deployments/{last_deployment.get('id')}"
    r = requests.delete(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys.exit(1)

    click.echo(FeedbackManager.success(message="Deployment promotion successfully started"))

    if wait:
        while True:
            TINYBIRD_API_URL = f"{host}/v1/deployments/{last_deployment.get('id')}"
            r = requests.get(TINYBIRD_API_URL, headers=headers)
            result = r.json()
            logging.debug(json.dumps(result, indent=2))

            last_deployment = result.get("deployment")
            if last_deployment.get("status") == "deleted":
                click.echo(FeedbackManager.success(message="Deployment promoted successfully"))
                break

            time.sleep(5)


# TODO(eclbg): This logic should be in the server, and there should be a dedicated endpoint for rolling back a
# deployment
def rollback_deployment(host: Optional[str], headers: dict, wait: bool) -> None:
    TINYBIRD_API_URL = f"{host}/v1/deployments"
    r = requests.get(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))

    deployments = result.get("deployments")
    if not deployments:
        click.echo(FeedbackManager.error(message="No deployments found"))
        return

    if len(deployments) < 2:
        click.echo(FeedbackManager.error(message="Only one deployment found"))
        return

    previous_deployment, current_deployment = deployments[0], deployments[1]

    if previous_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Previous deployment is not ready"))
        deploy_errors = previous_deployment.get("errors", [])
        for deploy_error in deploy_errors:
            click.echo(FeedbackManager.error(message=f"* {deploy_error}"))
        return

    if previous_deployment.get("live"):
        click.echo(FeedbackManager.error(message="Previous deployment is already live"))
    else:
        click.echo(FeedbackManager.success(message="Promoting previous deployment"))

        TINYBIRD_API_URL = f"{host}/v1/deployments/{previous_deployment.get('id')}/set-live"
        r = requests.post(TINYBIRD_API_URL, headers=headers)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))
        if result.get("error"):
            click.echo(FeedbackManager.error(message=result.get("error")))
            sys.exit(1)

    click.echo(FeedbackManager.success(message="Removing current deployment"))

    TINYBIRD_API_URL = f"{host}/v1/deployments/{current_deployment.get('id')}"
    r = requests.delete(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys.exit(1)

    click.echo(FeedbackManager.success(message="Deployment rollback successfully started"))

    if wait:
        while True:
            TINYBIRD_API_URL = f"{host}/v1/deployments/{current_deployment.get('id')}"
            r = requests.get(TINYBIRD_API_URL, headers=headers)
            result = r.json()
            logging.debug(json.dumps(result, indent=2))

            current_deployment = result.get("deployment")
            if current_deployment.get("status") == "deleted":
                click.echo(FeedbackManager.success(message="Deployment rolled back successfully"))
                break
            time.sleep(5)


@cli.group(name="deployment")
def deployment_group() -> None:
    """
    Deployment commands.
    """
    pass


@deployment_group.command(name="create")
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=False,
    help="Auto-promote the deployment. Only works if --wait is enabled. Disabled by default.",
)
@click.option(
    "--check/--no-check",
    is_flag=True,
    default=False,
    help="Validate the deployment before creating it. Disabled by default.",
)
@click.option(
    "--allow-destructive-operations/--no-allow-destructive-operations",
    is_flag=True,
    default=False,
    help="Allow removing datasources. Disabled by default.",
)
@click.pass_context
def deployment_create(
    ctx: click.Context, wait: bool, auto: bool, check: bool, allow_destructive_operations: bool
) -> None:
    """
    Validate and deploy the project server side.
    """
    create_deployment(ctx, wait, auto, check, allow_destructive_operations)


@deployment_group.command(name="ls")
@click.pass_context
def deployment_ls(ctx: click.Context) -> None:
    """
    List all the deployments you have in the project.
    """
    client = ctx.ensure_object(dict)["client"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
    url = f"{client.host}/v1/deployments"

    result = api_fetch(url, HEADERS)
    logging.debug(json.dumps(result, indent=2))

    status_map = {"data_ready": "Ready", "failed": "Failed"}
    columns = ["ID", "Status", "Created at", "Live"]
    table = []
    for deployment in result.get("deployments", []):
        if deployment.get("id") == "0":
            continue

        table.append(
            [
                deployment.get("id"),
                status_map.get(deployment.get("status"), "In progress"),
                datetime.fromisoformat(deployment.get("created_at")).strftime("%Y-%m-%d %H:%M:%S"),
                deployment.get("live"),
            ]
        )

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@deployment_group.command(name="promote")
@click.pass_context
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
def deployment_promote(ctx: click.Context, wait: bool) -> None:
    """
    Promote last deploy to ready and remove old one.
    """
    client = ctx.ensure_object(dict)["client"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    promote_deployment(client.host, HEADERS, wait=wait)


@deployment_group.command(name="rollback")
@click.pass_context
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
def deployment_rollback(ctx: click.Context, wait: bool) -> None:
    """
    Rollback to the previous deployment.
    """
    client = ctx.ensure_object(dict)["client"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    rollback_deployment(client.host, HEADERS, wait=wait)


@cli.command(name="deploy", hidden=True)
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=True,
    help="Wait for deploy to finish. Disabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=True,
    help="Auto-promote the deployment. Only works if --wait is enabled. Disabled by default.",
)
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Validate the deployment before creating it. Disabled by default.",
)
@click.option(
    "--allow-destructive-operations/--no-allow-destructive-operations",
    is_flag=True,
    default=False,
    help="Allow removing datasources. Disabled by default.",
)
@click.pass_context
def deploy(ctx: click.Context, wait: bool, auto: bool, check: bool, allow_destructive_operations: bool) -> None:
    """
    Deploy the project.
    """
    create_deployment(ctx, wait, auto, check, allow_destructive_operations)


def create_deployment(
    ctx: click.Context,
    wait: bool,
    auto: bool,
    check: Optional[bool] = None,
    allow_destructive_operations: Optional[bool] = None,
) -> None:
    # TODO: This code is duplicated in build_server.py
    # Should be refactored to be shared
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }
    project: Project = ctx.ensure_object(dict)["project"]
    client = ctx.ensure_object(dict)["client"]
    config = ctx.ensure_object(dict)["config"]
    TINYBIRD_API_URL = f"{client.host}/v1/deploy"
    TINYBIRD_API_KEY = client.token

    files = [
        ("context://", ("cli-version", "1.0.0", "text/plain")),
    ]
    fds = []
    for file_path in project.get_project_files():
        relative_path = str(Path(file_path).relative_to(project.path))
        fd = open(file_path, "rb")
        fds.append(fd)
        content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
        files.append((MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd.read().decode("utf-8"), content_type)))

    deployment = None
    try:
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
        params = {}
        if check:
            click.echo(FeedbackManager.highlight(message="\n» Validating deployment...\n"))
            params["check"] = "true"
        if allow_destructive_operations:
            params["allow_destructive_operations"] = "true"
        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS, params=params)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))

        print_changes(result, project)

        feedback = result.get("deployment", {}).get("feedback", [])
        for f in feedback:
            if f.get("level", "").upper() == "ERROR":
                feedback_func = FeedbackManager.error
                feedback_icon = ""
            else:
                feedback_func = FeedbackManager.warning
                feedback_icon = "△ "
            resource = f.get("resource")
            resource_bit = f"{resource}: " if resource else ""
            click.echo(feedback_func(message=f"{feedback_icon}{f.get('level')}: {resource_bit}{f.get('message')}"))

        deploy_errors = result.get("deployment", {}).get("errors")
        for deploy_error in deploy_errors:
            if deploy_error.get("filename", None):
                click.echo(
                    FeedbackManager.error(message=f"{deploy_error.get('filename')}\n\n{deploy_error.get('error')}")
                )
            else:
                click.echo(FeedbackManager.error(message=f"{deploy_error.get('error')}"))

        status = result.get("result")
        if check:
            if status == "success":
                click.echo(FeedbackManager.success(message="\n✓ Deployment is valid"))
                sys.exit(0)

            click.echo(FeedbackManager.error(message="\n✗ Deployment is not valid"))
            sys.exit(1)

        status = result.get("result")
        if status == "success":
            deployment = result.get("deployment", {})
            # TODO: This is a hack to show the url in the case of region is public. The URL should be returned by the API
            if client.host == "https://api.europe-west2.gcp.tinybird.co":
                click.echo(
                    FeedbackManager.gray(message="Deployment URL: ")
                    + FeedbackManager.info(
                        message=f"https://cloud.tinybird.co/gcp/europe-west2/{config.get('name')}/deployments/{deployment.get('id')}"
                    )
                )

            if wait:
                click.echo(FeedbackManager.info(message="\n✓ Deployment submitted successfully"))
            else:
                click.echo(FeedbackManager.success(message="\n✓ Deployment submitted successfully"))
        elif status == "failed":
            click.echo(FeedbackManager.error(message="Deployment failed"))
        else:
            click.echo(FeedbackManager.error(message=f"Unknown build result {status}"))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
    finally:
        for fd in fds:
            fd.close()

        if not deployment and not check:
            sys.exit(1)

    if deployment and wait and not check:
        while True:
            url = f"{client.host}/v1/deployments/{deployment.get('id')}"
            res = api_fetch(url, HEADERS)
            deployment = res.get("deployment")
            if not deployment:
                click.echo(FeedbackManager.error(message="Error parsing deployment from response"))
                sys.exit(1)
            if deployment.get("status") == "failed":
                click.echo(FeedbackManager.error(message="Deployment failed"))
                deploy_errors = deployment.get("errors")
                for deploy_error in deploy_errors:
                    click.echo(FeedbackManager.error(message=f"* {deploy_error}"))

                if auto:
                    click.echo(FeedbackManager.error(message="Rolling back deployment"))
                    rollback_deployment(client.host, HEADERS, wait=wait)
                sys.exit(1)

            if deployment.get("status") == "data_ready":
                break

            time.sleep(5)

        click.echo(FeedbackManager.success(message="Deployment is ready"))

        if auto:
            promote_deployment(client.host, HEADERS, wait=wait)


def print_changes(result: dict, project: Project) -> None:
    deployment = result.get("deployment", {})
    columns = ["status", "name", "path"]
    resources: list[list[Union[str, None]]] = []

    for ds in deployment.get("new_datasource_names", []):
        resources.append(["new", ds, project.get_resource_path(ds, "datasource")])

    for p in deployment.get("new_pipe_names", []):
        resources.append(["new", p, project.get_resource_path(p, "pipe")])

    for ds in deployment.get("changed_datasource_names", []):
        resources.append(["modified", ds, project.get_resource_path(ds, "datasource")])

    for p in deployment.get("changed_pipe_names", []):
        resources.append(["modified", p, project.get_resource_path(p, "pipe")])

    for ds in deployment.get("deleted_datasource_names", []):
        resources.append(["deleted", ds, project.get_resource_path(ds, "datasource")])

    for p in deployment.get("deleted_pipe_names", []):
        resources.append(["deleted", p, project.get_resource_path(p, "pipe")])

    if resources:
        click.echo(FeedbackManager.highlight(message="\n» Changes to be deployed...\n"))
        echo_safe_humanfriendly_tables_format_smart_table(resources, column_names=columns)
    else:
        click.echo(FeedbackManager.highlight(message="\n» No changes to be deployed\n"))
