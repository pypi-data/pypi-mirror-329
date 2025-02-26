"""
Tensorboard support.
"""

import click

from ..config import Config
from ..cli_utils import OrderedGroup, option_hostname
from .cli_utils import option_port, option_open_browser
from .remote_server import RemoteServer


class TensorBoard(RemoteServer):
    """
    TensorBoard remote server.
    """

    def __init__(
        self,
        port: int,
        hostname: str,
        logdir: str = "",
        open_browser: bool = True,
    ) -> None:
        super().__init__(
            server_start_command=f"tensorboard --bind_all --port {port} --logdir {logdir}",
            server_stop_command="pkill tensorboard",
            port=port,
            hostname=hostname,
            open_browser=open_browser,
            local_url=f"http://localhost:{port}",
        )

    def _server_start_callback(self, server_output_line: str) -> bool:
        return server_output_line.startswith("TensorBoard")


#######
# CLI #
#######
_option_tensorboard_port = option_port(service_name="tensorboard")


# pylint: disable=unused-argument
def _callback_option_tensorboard_logdir(ctx, param, value) -> str:
    if value:
        return value

    return Config().remote_servers.tensorboard.logdir


_option_tensorboard_logdir = click.option(
    "-d",
    "--logdir",
    callback=_callback_option_tensorboard_logdir,
    type=str,
    help="Log directory.",
)


@click.group(cls=OrderedGroup, invoke_without_command=True)
@click.pass_context
@_option_tensorboard_port
@option_hostname
@_option_tensorboard_logdir
@option_open_browser
def tensorboard(
    ctx,
    port: int,
    hostname: str,
    logdir: str,
    open_browser: bool,
) -> None:
    """
    Run TensorBoard on the remote host.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            tensorboard_run,
            port=port,
            hostname=hostname,
            logdir=logdir,
            open_browser=open_browser,
        )


@tensorboard.command("run")
@_option_tensorboard_port
@option_hostname
@option_open_browser
@_option_tensorboard_logdir
def tensorboard_run(
    port: int,
    hostname: str,
    logdir: str,
    open_browser: bool,
) -> None:
    """
    Run TensorBoard on the remote host.
    """
    TensorBoard(
        hostname=hostname,
        port=port,
        logdir=logdir,
        open_browser=open_browser,
    ).start()


@tensorboard.command("stop")
@_option_tensorboard_port
@option_hostname
def tensorboard_stop(port: int, hostname: str) -> None:
    """
    Stop TensorBoard on the remote host.
    """
    TensorBoard(
        hostname=hostname,
        port=port,
    ).stop_server()
