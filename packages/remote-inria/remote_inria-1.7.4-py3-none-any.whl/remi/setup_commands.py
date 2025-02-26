"""
Commands for setting up remi for a project.
"""

import click

from .config import Config
from .config.defaults import create_default_project
from .user_interaction import print_info, prompt_user_yes_no
from .utils import create_remote_directory, run_local_cmd
from .cli_utils import option_hostname
from .file_transfer import push_inria


@click.command()
def init() -> None:
    """
    Initialize the project in the current working directory. Generate the configuration files.
    """
    print_info(
        text="Creating a brand new remi project.",
        bold=True,
    )
    create_default_project()


@click.command()
@option_hostname
def setup(hostname: str) -> None:
    """
    Set up remote project location.

    Args:
        hostname (str):     The hostname of the remote computer.
    """
    config: Config = Config()

    print_info(
        text=f"Setting up remote for project: {config.project_name}",
        bold=True,
    )

    paths_to_create: str = config.project_remote_path
    paths_to_create += (
        "/{"
        + ",".join(
            [
                config.output_path,
                config.notebooks_path,
                config.oarsub_log_path,
            ]
        )
        + "}"
    )

    # Create the project directory on the remote and the output folder within it.
    create_remote_directory(
        path=paths_to_create,
        hostname=hostname,
    )
    push_inria()

    print_info("Setup complete !")


@click.command()
def update() -> None:
    """
    Update remi to the latest version
    """
    if prompt_user_yes_no("Do you wish to update 'remi' to the latest version ?"):
        run_local_cmd(
            command=[
                "pip",
                "install",
                "-U",
                "remote-inria",
            ],
            check=True,
        )
    else:
        print_info("All right the, aborting.")
