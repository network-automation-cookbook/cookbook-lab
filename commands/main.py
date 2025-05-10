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
from labcli.utils.docker_utils import (
    docker_ps,
    docker_destroy,
    docker_start,
    docker_network,
    docker_rm,
    docker_stop,
    docker_build,
    DockerNetworkAction
)

# lab_app = typer.Typer(help="Lab related commands", rich_markup_mode="rich")

# app.add_typer(lab_app, name="lab")

app._add_completion = False
setup_app = typer.Typer(help="Lab hosting machine setup related commands.", rich_markup_mode="rich")
app.add_typer(setup_app, name="setup")

lab_app = typer.Typer(help="Overall Lab management related commands.", rich_markup_mode="rich")
app.add_typer(lab_app, name="lab")

load_dotenv(verbose=True, override=True, dotenv_path=Path("./.env"))
ENVVARS = {**dotenv_values(".env"), **dotenv_values(".setup.env"), **os.environ}


# --------------------------------------#
#                  Lab                  #
# --------------------------------------#


class LabCLIScenarios(Enum):
    """LabCLI scenarios."""

    BATTERIES_INCLUDED = "batteries-included"


@lab_app.command("deploy")
def lab_deploy(
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
    topology: Annotated[Path, typer.Option(help="Path to the topology file", exists=True)] = Path(
        "./containerlab/lab.yml"
    ),
    network_name: Annotated[
        str, typer.Option(help="Network name", envvar="LAB_NETWORK_NAME")
    ] = "network-cookbook-lab",
    subnet: Annotated[str, typer.Option(help="Network subnet", envvar="LAB_SUBNET")] = "198.51.100.0/24",
    sudo: Annotated[bool, typer.Option(help="Use sudo to run containerlab", envvar="LAB_SUDO")] = False,
):
    """Deploy a lab topology."""
    typer.echo(f"Deploying lab environment for scenario: [orange1 i]{scenario.value}")

    # First create docker network if not exists
    docker_network(
        DockerNetworkAction.CREATE,
        name=network_name,
        driver="bridge",
        subnet=subnet,
    )

    # Deploy containerlab topology
    containerlab_deploy(topology=topology, sudo=sudo)

    # Start docker compose
    docker_start(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), verbose=True)

    typer.echo(f"Lab environment deployed for scenario: [orange1 i]{scenario.value}")


@lab_app.command("destroy")
def lab_destroy(
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
    topology: Annotated[Path, typer.Option(help="Path to the topology file", exists=True)] = Path(
        "./containerlab/lab.yml"
    ),
    sudo: Annotated[bool, typer.Option(help="Use sudo to run containerlab", envvar="LAB_SUDO")] = False,
):
    """Destroy a lab topology."""
    typer.echo(f"Destroying lab environment for scenario: [orange1 i]{scenario.value}")

    # Stop docker compose
    docker_destroy(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), volumes=True, verbose=True)

    # Destroy containerlab topology
    containerlab_destroy(topology=topology, sudo=sudo)

    typer.echo(f"Lab environment destroyed for scenario: [orange1 i]{scenario.value}")


@lab_app.command("purge")
def lab_purge(
    sudo: Annotated[bool, typer.Option(help="Use sudo to run containerlab", envvar="LAB_SUDO")] = False,
):
    """Purge all lab environments."""
    typer.echo("[b i]PURGING ALL LAB ENVIRONMENTS")
    typer.echo("Purging lab environments")

    # Iterate over all scenarios and destroy them
    for scenario in LabCLIScenarios:
        try:
            lab_destroy(scenario=scenario, sudo=sudo)
        except typer.Exit:
            pass

    typer.echo("[b i]LAB ENVIRONMENTS PURGED")


@lab_app.command("show")
def lab_show(
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
    topology: Annotated[Path, typer.Option(help="Path to the topology file", exists=True)] = Path(
        "./containerlab/lab.yml"
    ),
    sudo: Annotated[bool, typer.Option(help="Use sudo to run containerlab", envvar="LAB_SUDO")] = False,
):
    """Show lab environment."""
    typer.echo(f"Showing lab environment for scenario: [orange1 i]{scenario.value}")

    # Show docker compose
    docker_ps(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), verbose=True)

    # Show containerlab topology
    containerlab_inspect(topology=topology, sudo=sudo)

    typer.echo(f"Lab environment shown for scenario: [orange1 i]{scenario.value}")


@lab_app.command("prepare")
def lab_prepare(
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
    topology: Annotated[Path, typer.Option(help="Path to the topology file", exists=True)] = Path(
        "./containerlab/lab.yml"
    ),
    sudo: Annotated[bool, typer.Option(help="Use sudo to run containerlab", envvar="LAB_SUDO")] = False,
):
    """Prepare the lab for the scenario."""
    typer.echo(f"Preparing lab environment for scenario: [orange1 i]{scenario.value}")

    # Destroy all other lab environments and network topologies
    lab_purge(sudo=sudo)

    # Deploy containerlab topology
    containerlab_deploy(topology=topology, sudo=sudo)

    # Start docker compose
    docker_start(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=[], verbose=True)

    typer.echo(f"Lab environment prepared for scenario: [orange1 i]{scenario.value}")


@lab_app.command("update")
def lab_update(
    services: Annotated[list[str], typer.Argument(help="Service(s) to update")],
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
):
    """Update the service(s) of a lab scenario.

    [u]Example:[/u]]

    To update all services:
        [i]labcli lab update --scenario batteries-included[/i]

    To update a specific service:
        [i]labcli lab update telegraf-01 telegraf-02 --scenario batteries-included[/i]
    """
    typer.echo(f"Updating lab environment for scenario: [orange1 i]{scenario.value}")

    # Delete the containers
    docker_rm(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=services, volumes=True, force=True, verbose=True)

    # Start them back
    docker_start(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=services, verbose=True)

    typer.echo(f"Lab environment updated for scenario: [orange1 i]{scenario.value}")


@lab_app.command("rebuild")
def lab_rebuild(
    services: Annotated[list[str], typer.Argument(help="Service(s) to rebuild")],
    scenario: Annotated[
        LabCLIScenarios, typer.Option("--scenario", "-s", help="Scenario to execute command", envvar="LAB_SCENARIO")
    ],
):
    """Rebuild the service(s) of a lab scenario.

    [u]Example:[/u]

    To rebuild all services:
        [i]labcli lab rebuild --scenario batteries-included[/i]

    To rebuild a specific service:
        [i]labcli lab rebuild webhook --scenario batteries-included[/i]
    """
    typer.echo(f"Rebuilding lab environment for scenario: [orange1 i]{scenario.value}")

    # Stop the containers
    docker_stop(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=services, verbose=True)

    # Rebuild the containers
    docker_build(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=services, verbose=True)

    # Start them back
    docker_start(compose_file=Path("./chapters/{scenario.value}/docker-compose.yml"), services=services, verbose=True)

    typer.echo(f"Lab environment rebuilt for scenario: [orange1 i]{scenario.value}")


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


@setup_app.command(rich_help_panel="DigitalOcean", name="deploy")
def deploy_droplet(
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
    extra_vars: Annotated[
        Optional[str], typer.Option("--extra-vars", "-e", help="Extra vars to pass to the playbook")
    ] = None,
):
    """Create DigitalOcean Droplets.

    [u]Example:[/u]
        [i]> lab setup deploy[/i]
    """

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


@setup_app.command(rich_help_panel="DigitalOcean", name="destroy")
def destroy_droplet(
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0,
    extra_vars: Annotated[
        Optional[str], typer.Option("--extra-vars", "-e", help="Extra vars to pass to the playbook")
    ] = None,
):
    """Destroy DigitalOcean Droplets.

    [u]Example:[/u]
        [i]> lab setup destroy[/i]
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


@setup_app.command(rich_help_panel="DigitalOcean", name="show")
def show_droplet():
    """Show the DigitalOcean Droplet SSH command.

    [u]Example:[/u]
        [i]> lab setup list[/i]
    """
    exec_cmd = ansible_command(
        playbook="list_droplet.yml",
        inventories=["do_hosts.yaml"],
    )
    return run_cmd(exec_cmd=exec_cmd, envvars=ENVVARS, task_name="show droplets")
