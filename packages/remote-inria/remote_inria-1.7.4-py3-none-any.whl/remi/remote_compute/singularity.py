"""
Functions to interact with singularity.
"""

import sys
from typing import Optional
import subprocess
from os.path import isfile
from termcolor import colored

import click

from ..cli_utils import option_force
from ..user_interaction import to_bold, print_info, print_warning, print_error
from ..utils import run_remote_command_inria
from ..file_transfer import push_inria
from ..config import Config


def get_binding_sub_command(
    project_remote_path: str,
    bindings: dict[str, Optional[str]] = None,
    env_variables: dict[str, str | int] = None,
    no_home: bool = False,
) -> list[str]:
    """
    Path bindings between host system and singularity container
    """
    binding_sub_cmd: list[str] = []

    if bindings is not None:
        if project_remote_path not in bindings:
            binding_sub_cmd += ["--bind", project_remote_path]
        for host_path, container_path in bindings.items():
            binding_sub_cmd += ["--bind", host_path]
            if container_path:
                binding_sub_cmd[-1] += ":" + container_path
    else:
        binding_sub_cmd += ["--bind", project_remote_path]

    if env_variables:
        for var_name, var_value in env_variables.items():
            var_value_str: str = ""
            match var_value:
                case int():
                    var_value_str = str(var_value)
                case str():
                    var_value_str = f'"{var_value}"'
                case None:
                    var_value_str = ""
                case _:
                    print_error(
                        f"Value for environment variable `${var_name}` has an unexpected type."
                        f"\nType: {type(var_value)}.\nValue: {str(var_value)}"
                    )
                    sys.exit(1)

            binding_sub_cmd += ["--env", f"{var_name}={var_value_str}"]

    if no_home:
        binding_sub_cmd.append("--no-home")

    return binding_sub_cmd


def build_singularity_container(
    output_sif_name: str = "",
    force: bool = False,
) -> None:
    singularity_config = Config().singularity

    def_file_name: str = singularity_config.def_file_name

    if output_sif_name == "":
        output_sif_name = singularity_config.output_sif_name

    # If not using the default sif, don't try to build
    elif output_sif_name != singularity_config.output_sif_name:
        return

    if not isfile(def_file_name):
        print_warning(f"Recipe file not found (`{def_file_name}`). Aborting")
        return

    # Smart build
    # The 'smart build' mechanism stores the last built recipe file at each build
    # under `.remi/last_built_recipe.def`.
    # Then we are able to check if something has changed locally since last build and run the
    # singularity command only if necessary (if `container.def` differs from
    # `.remi/last_built_recipe.def`).
    # This avoids opening a useless ssh tunnel with the server (which can sometimes last a few
    # seconds) and asking a confirmation to the user.
    last_built_recipe_path: str = ".remi/last_built_recipe.def"

    last_built_recipe: str = ""
    if isfile(last_built_recipe_path):
        with open(last_built_recipe_path, "r") as last_recipe_built_file:
            last_built_recipe = last_recipe_built_file.read()

    with open(def_file_name, "r") as current_recipe_file:
        current_recipe: str = current_recipe_file.read()

    # Check if something has changed
    if current_recipe == last_built_recipe and not force:
        print_info("Nothing has changed since last build. Cancelling build.")
        return

    # Else, something has changed: so we build the image remotely.

    # Run singularity build on Inria remote
    build_command: list[str] = [
        "cd",
        Config().project_remote_path,
        "&&",
        "sudo",
        "singularity",
        "build",
    ]

    print_info(
        to_bold("Building container image ")
        + "`"
        + colored(output_sif_name, "yellow")
        + "`"
        + to_bold(" from recipe ")
        + "`"
        + colored(def_file_name, "yellow")
        + "`"
    )

    if force:
        build_command += ["--force"]

    build_command += [output_sif_name, def_file_name]

    return_code: int = run_remote_command_inria(
        command=build_command,
        check=False,
        force_tty_allocation=True,
    )

    if return_code == 0:
        print_info("Build succesfull.")
        # If the build command succeeded, save the current recipe as the 'last built recipe'
        subprocess.run(
            [
                "cp",
                "-f",
                def_file_name,
                last_built_recipe_path,
            ],
            check=True,
        )
    else:
        print_info("You canceled the build remotely")


@click.command("build-container")
@option_force(help_message="Build the container even if the sif image already exists.")
def build_container(force: bool) -> None:
    """
    Build the singularity container on the remote desktop.
    """
    # First, sync project with remote
    push_inria()

    build_singularity_container(force=force)
