import os
import shlex
import subprocess  # nosec
import time
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess  # nosec
from dotenv import dotenv_values, load_dotenv

from pathlib import Path
from typing import Any, Optional
from typing_extensions import Annotated

import typer
from labcli.cli import app
from labcli.utils.containerlab_utils import (
    containerlab_deploy,
    containerlab_destroy,
    containerlab_inspect,
)
from labcli.utils.docker_utils import docker_ps, docker_destroy, docker_start

# lab_app = typer.Typer(help="Lab related commands", rich_markup_mode="rich")

# app.add_typer(lab_app, name="lab")

app._add_completion = False

load_dotenv(verbose=True, override=True, dotenv_path=Path("./.env"))
ENVVARS = {**dotenv_values(".env"), **dotenv_values(".setup.env"), **os.environ}

# @app.command()
# def create(lab: str = typer.Argument(..., help="Name of the lab")):
#     """Create a lab

#     Example:

#     $ lab create netobs
#     """
#     # Deploy containerlab topology
#     clab_cmd = containerlab_deploy(
#         sudo=True, topology=Path(f"./labs/{lab}/containerlab/lab.clab.yml")
#     )
#     if clab_cmd is not None and clab_cmd.returncode != 0:
#         typer.echo(clab_cmd.stderr)
#         raise typer.Abort()
#     # Start docker containers
#     docker_cmd = docker_start(compose_file=Path(f"./labs/{lab}/docker-compose.yml"))
#     if docker_cmd is not None and docker_cmd.returncode != 0:
#         typer.echo(docker_cmd.stderr)
#         raise typer.Abort()

# --------------------------------------#
#           Digital Ocean VM            #
# --------------------------------------#


def run_cmd(
    exec_cmd: str,
    envvars: dict[str, Any] = ENVVARS,
    cwd: Optional[str] = None,
    timeout: Optional[int] = None,
    shell: bool = False,
    capture_output: bool = False,
    task_name: str = "",
) -> CompletedProcess:
    """Run a command and return the result.

    Args:
        exec_cmd (str): Command to execute
        envvars (dict, optional): Environment variables. Defaults to ENVVARS.
        cwd (str, optional): Working directory. Defaults to None.
        timeout (int, optional): Timeout in seconds. Defaults to None.
        shell (bool, optional): Run the command in a shell. Defaults to False.
        capture_output (bool, optional): Capture stdout and stderr. Defaults to True.
        task_name (str, optional): Name of the task. Defaults to "".

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    typer.echo(f"Running command: {exec_cmd}")
    result = subprocess.run(
        shlex.split(exec_cmd),
        env=envvars,
        cwd=cwd,
        timeout=timeout,
        shell=shell,  # nosec
        capture_output=capture_output,
        text=True,
        check=False,
    )
    task_name = task_name if task_name else exec_cmd
    if result.returncode == 0:
        typer.echo(f"Successfully ran: {task_name}")
    else:
        typer.echo(f"Issues encountered running: {task_name}")
    typer.echo(f"End of task: {task_name}")
    return result


def ansible_command(
    playbook: str,
    inventories: list[str] | None = None,
    limit: str | None = None,
    extra_vars: str | None = None,
    verbose: int = 0,
) -> str:
    """Run an ansible playbook with the given inventories and limit.

    Args:
        playbook (str): The name of the playbook to run.
        inventories (List[str]): The list of inventories to use.
        limit (Optional[str], optional): The limit to use. Defaults to None.
        verbose (int, optional): The verbosity level. Defaults to 0.

    Returns:
        str: The ansible command to run.
    """
    exec_cmd = f"ansible-playbook setup/{playbook}"
    if inventories:
        for inventory in inventories:
            exec_cmd += f" -i setup/inventory/{inventory}"

    if limit:
        exec_cmd += f" -l {limit}"

    if extra_vars:
        exec_cmd += f' -e "{extra_vars}"'

    if verbose:
        exec_cmd += f" -{'v' * verbose}"

    return exec_cmd


@app.command(rich_help_panel="DigitalOcean", name="deploy")
def deploy_droplet(
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
    extra_vars: Annotated[
        Optional[str], typer.Option("--extra-vars", "-e", help="Extra vars to pass to the playbook")
    ] = None,
):
    """Create DigitalOcean Droplets.

    [u]Example:[/u]
        [i]> labcli setup deploy[/i]
    """
    # First create the keep_api_key file in the root directory from the environment variable using Path
    keep_api_key = Path("./keep_api_key")
    keep_api_key.write_text(ENVVARS.get("KEEP_API_KEY", ""))

    # Then create the droplets
    exec_cmd = ansible_command(
        playbook="create_droplet.yml",
        inventories=["localhost.yaml"],
        verbose=verbose,
        extra_vars=extra_vars,
    )
    result = run_cmd(exec_cmd=exec_cmd, envvars=ENVVARS, task_name="create droplets")
    if result.returncode == 0:
        typer.echo("Droplets created successfully")
    else:
        typer.echo("Issues encountered creating droplets")
        raise typer.Abort()
    typer.echo("Proceeding to setup the droplets")
    exec_cmd = ansible_command(
        playbook="setup_droplet.yml",
        inventories=["do_hosts.yaml", "localhost.yaml"],
        verbose=verbose,
        extra_vars=extra_vars,
    )
    result = run_cmd(exec_cmd=exec_cmd, envvars=ENVVARS, task_name="create droplets")
    if result.returncode == 0:
        typer.echo("Droplets setup successfully")
    else:
        typer.echo("Issues encountered setting up droplets")
        raise typer.Abort()

    # Delete the keep_api_key file
    keep_api_key.unlink()


@app.command(rich_help_panel="DigitalOcean", name="destroy")
def destroy_droplet(
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
    extra_vars: Annotated[
        Optional[str], typer.Option("--extra-vars", "-e", help="Extra vars to pass to the playbook")
    ] = None,
):
    """Destroy DigitalOcean Droplets.

    [u]Example:[/u]
        [i]> labcli setup destroy[/i]
    """
    exec_cmd = ansible_command(
        playbook="destroy_droplet.yml",
        inventories=["do_hosts.yaml"],
        verbose=verbose,
        extra_vars=extra_vars,
    )
    result = run_cmd(exec_cmd=exec_cmd, envvars=ENVVARS, task_name="destroy droplets")
    if result.returncode == 0:
        typer.echo("Droplets destroyed successfully")
    else:
        typer.echo("Issues encountered destroying droplets")
        raise typer.Abort()


@app.command(rich_help_panel="DigitalOcean", name="show")
def show_droplet():
    """Show the DigitalOcean Droplet SSH command.

    [u]Example:[/u]
        [i]> labcli setup list[/i]
    """
    exec_cmd = ansible_command(
        playbook="list_droplet.yml",
        inventories=["do_hosts.yaml"],
    )
    return run_cmd(exec_cmd=exec_cmd, envvars=ENVVARS, task_name="show droplets")
