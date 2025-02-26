"""
Common options for remote compute commands
"""

import sys
from os.path import isfile
import click

from ..user_interaction import print_error
from ..config import Config


# pylint: disable=unused-argument
def _callback_option_script(ctx, param, value) -> str:
    # Make sure the script is a valid file
    if ctx.invoked_subcommand not in (None, "script"):
        if not isfile(value):
            print_error(f"Script `{value}` does not exist.")
            sys.exit(1)

    return value


# pylint: disable=unused-argument
def _callback_argument_command(ctx, param, value) -> str:
    if len(value) == 0:
        print_error("No command provided. Exiting")
        sys.exit(1)

    return value


# pylint: disable=unused-argument
def _callback_option_container(ctx, param, value) -> str:
    if value:
        return value

    return Config().singularity.output_sif_name


option_interactive = click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Open an interactive session instead of running the script",
)

option_script = click.option(
    "-s",
    "--script",
    "script_name",
    default="script.sh",
    type=str,
    callback=_callback_option_script,
    help="Path to a bash script to run",
)

option_background = click.option(
    "-b",
    "--background",
    default=False,
    is_flag=True,
    help="Run the script in the background",
)

option_no_build = click.option(
    "--no-build",
    default=False,
    is_flag=True,
    help="Prevent trying to build the singularity container.",
)

argument_command = click.argument(
    "command",
    nargs=-1,
    type=str,
    callback=_callback_argument_command,
)


option_container: click.option = click.option(
    "-c",
    "--container",
    "container",
    type=str,
    callback=_callback_option_container,
    help="The container image to use (.sif)",
)
