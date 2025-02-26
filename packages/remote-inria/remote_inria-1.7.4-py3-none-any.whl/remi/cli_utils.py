"""
Common options for remi commands
"""

from collections import OrderedDict
import click
import re

from .config import Config

# Common options, arguments and their eventual callbacks


# pylint: disable=unused-argument
def _callback_option_hostname(ctx, param, value) -> str:
    config: Config = Config()
    # If no hostname was provided, use the one from the config file.
    if value == "":
        return config.desktop.ip_adress

    if re.match(r"gpu[0-9]$", value):
        value += "-perception"

    # Make sure the provided hostname is a valid Inria hostname
    if not value.endswith(".inrialpes.fr"):
        value += ".inrialpes.fr"

    return value


option_hostname: click.option = click.option(
    "-h",
    "--hostname",
    default="",
    type=str,
    callback=_callback_option_hostname,
    help="Name of an Inria computer",
)
option_no_push: click.option = click.option(
    "--no-push",
    default=False,
    is_flag=True,
    help="Prevent syncing the project files.",
)

option_xforwarding = click.option(
    "-X",
    "--xforwarding",
    "x_forwarding",
    default=False,
    is_flag=True,
    help="Enables X forwarding in SSH.",
)


def option_force(
    help_message: str,
    default: bool = False,
):
    return click.option(
        "-f",
        "--force",
        default=default,
        is_flag=True,
        help=help_message,
    )


class OrderedGroup(click.Group):
    """
    Override of the click.Group class in order to preserve custom ordering of commands in `--help`.
    """

    def __init__(
        self,
        name=None,
        commands=None,
        **attrs,
    ) -> None:
        super().__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or OrderedDict()

    def list_commands(self, ctx):
        """
        Override of the `list_commands` method.
        """
        return self.commands
