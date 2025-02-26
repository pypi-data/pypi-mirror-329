"""
Common options for remote servers commands
"""

import click

from ..config import Config


def option_port(service_name: str):
    # pylint: disable=unused-argument
    def _callback(ctx, param, value) -> int:
        if value is not None:
            return value

        # The default port for an SSH tunnel is the TensorBoard port.
        if service_name == "ssh tunnel":
            _service_name = "tensorboard"
        else:
            _service_name = service_name

        return getattr(Config().remote_servers, _service_name).port

    return click.option(
        "-p",
        "--port",
        type=int,
        callback=_callback,
        help=f"Local port for accessing {service_name}.",
    )


# pylint: disable=unused-argument
def _callback_option_browser(ctx, param, value) -> bool:
    if value is not None:
        return value

    config: Config = Config()

    if ctx.command.name == "jupyter":
        return config.jupyter.open_browser

    if ctx.command.name == "tensorboard":
        return config.tensorboard.open_browser

    return True


option_open_browser = click.option(
    "--browser/--no-browser",
    "open_browser",
    default=True,
    callback=_callback_option_browser,
    help="Open the local browser after running server.",
)
