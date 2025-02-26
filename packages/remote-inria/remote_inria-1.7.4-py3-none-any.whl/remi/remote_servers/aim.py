"""
Aim support.
https://github.com/aimhubio/aim
"""

import click

from .remote_server import RemoteServer
from ..cli_utils import OrderedGroup, option_hostname
from .cli_utils import option_port, option_open_browser
from ..config import Config


class Aim(RemoteServer):
    """
    Aim remote server.
    https://github.com/aimhubio/aim
    """

    def __init__(
        self,
        port: int,
        hostname: str,
        repo: str = "",
        open_browser: bool = True,
    ) -> None:
        super().__init__(
            server_start_command=f"aim up --port {port} --repo {repo}",
            server_stop_command="pkill aim && pkill uvicorn",
            port=port,
            hostname=hostname,
            open_browser=open_browser,
            local_url=f"http://localhost:{port}",
        )

    def _server_start_callback(self, server_output_line: str) -> bool:
        return server_output_line.startswith("Open ")


#######
# CLI #
#######
_option_aim_port = option_port(service_name="aim")


# pylint: disable=unused-argument
def _callback_option_aim_repo(ctx, param, value) -> str:
    if value:
        return value

    return Config().remote_servers.aim.repo


_option_aim_repo = click.option(
    "-r",
    "--repo",
    callback=_callback_option_aim_repo,
    type=str,
    help="Log directory.",
)


@click.group(cls=OrderedGroup, invoke_without_command=True)
@click.pass_context
@_option_aim_port
@option_hostname
@_option_aim_repo
@option_open_browser
def aim(
    ctx,
    port: int,
    hostname: str,
    repo: str,
    open_browser: bool,
) -> None:
    """
    Run Aim on the remote host.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            aim_run,
            port=port,
            hostname=hostname,
            repo=repo,
            open_browser=open_browser,
        )


@aim.command("run")
@_option_aim_port
@option_hostname
@option_open_browser
@_option_aim_repo
def aim_run(
    port: int,
    hostname: str,
    repo: str,
    open_browser: bool,
) -> None:
    """
    Run Aim on the remote host.
    """
    Aim(
        hostname=hostname,
        port=port,
        repo=repo,
        open_browser=open_browser,
    ).start()


@aim.command("stop")
@_option_aim_port
@option_hostname
def aim_stop(port: int, hostname: str) -> None:
    """
    Stop Aim on the remote host.
    """
    Aim(
        hostname=hostname,
        port=port,
    ).stop_server()
