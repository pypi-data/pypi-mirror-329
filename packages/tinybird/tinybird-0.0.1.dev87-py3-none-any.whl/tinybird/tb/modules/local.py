import os
import re
import subprocess
import time

import click

import docker
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import coro
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_CONTAINER_NAME, TB_IMAGE_NAME, TB_LOCAL_PORT


def start_tinybird_local(
    docker_client,
):
    """Start the Tinybird container."""
    pull_show_prompt = False
    pull_required = False
    try:
        local_image = docker_client.images.get(TB_IMAGE_NAME)
        local_image_id = local_image.attrs["RepoDigests"][0].split("@")[1]
        remote_image = docker_client.images.get_registry_data(TB_IMAGE_NAME)
        pull_show_prompt = local_image_id != remote_image.id
    except Exception:
        pull_show_prompt = False
        pull_required = True

    if pull_show_prompt and click.confirm(
        FeedbackManager.warning(message="△ New version detected, download? [y/N]:"),
        show_default=False,
        prompt_suffix="",
    ):
        click.echo(FeedbackManager.info(message="* Downloading latest version of Tinybird Local..."))
        pull_required = True

    if pull_required:
        docker_client.images.pull(TB_IMAGE_NAME, platform="linux/amd64")

    container = None
    containers = docker_client.containers.list(all=True, filters={"name": TB_CONTAINER_NAME})
    if containers:
        container = containers[0]

    if container and not pull_required:
        # Container `start` is idempotent. It's safe to call it even if the container is already running.
        container.start()
    else:
        if container:
            container.remove(force=True)

        container = docker_client.containers.run(
            TB_IMAGE_NAME,
            name=TB_CONTAINER_NAME,
            detach=True,
            ports={"80/tcp": TB_LOCAL_PORT},
            remove=False,
            platform="linux/amd64",
        )

    click.echo(FeedbackManager.info(message="* Waiting for Tinybird Local to be ready..."))
    while True:
        container.reload()  # Refresh container attributes
        health = container.attrs.get("State", {}).get("Health", {}).get("Status")
        if health == "healthy":
            break
        if health == "unhealthy":
            raise CLIException("Tinybird Local is unhealthy. Try running `tb local restart` in a few seconds.")

        time.sleep(5)

    # Remove tinybird-local dangling images to avoid running out of disk space
    images = docker_client.images.list(name=re.sub(r":.*$", "", TB_IMAGE_NAME), all=True, filters={"dangling": True})
    for image in images:
        image.remove(force=True)


def get_docker_client():
    """Check if Docker is installed and running."""
    try:
        client = docker.from_env()  # type: ignore
        client.ping()
        return client
    except Exception:
        raise CLIException(
            "No container runtime is running. Make sure a Docker-compatible runtime is installed and running."
        )


def stop_tinybird_local(docker_client):
    """Stop the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.stop()
    except Exception:
        pass


def remove_tinybird_local(docker_client):
    """Remove the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.remove(force=True)
    except Exception:
        pass


def update_cli():
    click.echo(FeedbackManager.highlight(message="» Updating Tinybird CLI..."))
    process = subprocess.Popen(
        [f"{os.getenv('HOME')}/.local/bin/uv", "tool", "upgrade", "tinybird"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate()
    if "Nothing to upgrade" not in stdout + stderr:
        click.echo(FeedbackManager.success(message="✓ Tinybird CLI updated"))
    else:
        click.echo(FeedbackManager.info(message="✓ Tinybird CLI is already up-to-date"))


@cli.command()
def update():
    """Update Tinybird CLI to the latest version."""
    update_cli()


@cli.command(name="upgrade", hidden=True)
def upgrade():
    """Update Tinybird CLI to the latest version."""
    update_cli()


@cli.group()
@click.pass_context
def local(ctx):
    """Manage the local Tinybird instance."""


@local.command()
@coro
async def stop() -> None:
    """Stop Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Shutting down Tinybird Local..."))
    docker_client = get_docker_client()
    stop_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local stopped"))


@local.command()
@coro
async def remove() -> None:
    """Remove Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Removing Tinybird Local..."))
    docker_client = get_docker_client()
    remove_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local removed"))


@local.command()
@coro
async def start() -> None:
    """Start Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Starting Tinybird Local..."))
    docker_client = get_docker_client()
    start_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))


@local.command()
@coro
async def restart() -> None:
    """Restart Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Restarting Tinybird Local..."))
    docker_client = get_docker_client()
    remove_tinybird_local(docker_client)
    click.echo(FeedbackManager.info(message="✓ Tinybird Local stopped"))
    start_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))
