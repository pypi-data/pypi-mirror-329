"""
Jupyter notebook support.
"""

import click

from .remote_server import RemoteServer
from ..cli_utils import OrderedGroup, option_hostname
from .cli_utils import option_port, option_open_browser


class Jupyter(RemoteServer):
    """
    Jupyter remote server.
    """

    def __init__(
        self,
        port: int,
        hostname: str,
        open_browser: bool = True,
    ) -> None:
        super().__init__(
            server_start_command="python -m jupyter notebook --no-browser"
            f" --port={port} --port-retries=0",
            server_stop_command=f"python -m jupyter notebook stop {port}",
            port=port,
            hostname=hostname,
            open_browser=open_browser,
            local_url="",
        )

    def _server_start_callback(self, server_output_line: str) -> bool:
        if server_output_line.startswith("http://localhost:"):
            self.local_url = server_output_line
            return True

        return False


_option_jupyter_port = option_port(service_name="jupyter")


@click.group(cls=OrderedGroup, invoke_without_command=True)
@click.pass_context
@_option_jupyter_port
@option_hostname
@option_open_browser
def jupyter(
    ctx,
    port: int,
    hostname: str,
    open_browser: bool,
) -> None:
    """
    Run a jupyter server on the remote host.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            jupyter_run,
            port=port,
            hostname=hostname,
            open_browser=open_browser,
        )


@jupyter.command("run")
@_option_jupyter_port
@option_hostname
@option_open_browser
def jupyter_run(
    port: int,
    hostname: str,
    open_browser: bool,
) -> None:
    """
    Run a jupyter server on the remote host.
    """
    Jupyter(
        port=port,
        hostname=hostname,
        open_browser=open_browser,
    ).start()


@jupyter.command("stop")
@_option_jupyter_port
@option_hostname
def jupyter_stop(port: int, hostname: str) -> None:
    """
    Stop the jupyter server on the remote host.
    """
    Jupyter(
        port=port,
        hostname=hostname,
    ).stop_server()
