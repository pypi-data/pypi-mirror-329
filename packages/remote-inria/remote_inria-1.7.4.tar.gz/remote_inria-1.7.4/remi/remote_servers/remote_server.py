"""
A class representing a remote server (an application that run on the remote and is accessible via
http).
A ssh tunnel transports the traffic on the selected port between the local and remote computers.
"""

import sys
from abc import ABC
from signal import signal, SIGINT
from subprocess import Popen
from socket import gethostname
from typing import Optional
from termcolor import colored
import click

from ..user_interaction import to_bold, print_info, print_error
from ..config import Config
from ..utils import run_remote_command_inria
from ..file_transfer import push_inria
from .cli_utils import option_port
from ..cli_utils import option_hostname


def _print_stdout(text: str) -> None:
    print(colored("[STDOUT]", "blue", attrs=["bold"]), text)


def _print_stderr(text: str) -> None:
    print(colored("[STDERR]", "magenta", attrs=["bold"]), text)


class SshTunnel:
    """
    Class for running and stopping a SSH tunnel.
    """

    def __init__(
        self,
        hostname: str,
        port: int,
    ) -> None:
        self.hostname: str = hostname
        self.port: int = port

        self.process: Optional[Popen] = None

    def start(self) -> None:
        """
        Start the ssh tunnel.
        """
        config: Config = Config()

        print_info(f"Running SSH port forwarding for port {self.port}")
        print_info(to_bold("on host: ") + str(self.hostname))

        ssh_tunnel_cmd: list[str] = ["ssh", "-N"]

        ssh_tunnel_cmd += ["-L", f"{self.port}:localhost:{self.port}"]

        # Bastion ProxyJump
        if config.bastion.enable:
            ssh_tunnel_cmd += ["-J", f"{config.username}@{config.bastion.hostname}"]

        ssh_tunnel_cmd.append(f"{config.username}@{self.hostname}")

        # Run the command
        print_info(to_bold("SSH tunnel command: ") + " ".join(ssh_tunnel_cmd))

        # pylint: disable=consider-using-with
        self.process = Popen(args=ssh_tunnel_cmd)

    def stop(self) -> None:
        """
        Stop the ssh tunnel.
        """
        if self.process is not None:
            print_info("Killing the ssh tunnel process")
            self.process.kill()


class RemoteServer(ABC):
    """
    Abstract class for remote servers.
    """

    def __init__(
        self,
        server_start_command: str,
        server_stop_command: str,
        port: int,
        hostname: str,
        open_browser: bool,
        local_url: str,
    ) -> None:
        self.server_start_command: list[str] = self._wrap_command(server_start_command)
        self.server_stop_command: list[str] = self._wrap_command(server_stop_command)
        self.port = port
        self.hostname = hostname

        self.open_browser: bool = open_browser
        self.local_url: str = local_url

        self.ssh_tunnel: Optional[SshTunnel] = None
        if gethostname() not in self.hostname:
            self.ssh_tunnel = SshTunnel(
                hostname=hostname,
                port=port,
            )

        self.server_process: Popen = None

    def _server_start_callback(self, server_output_line: str) -> bool:
        """
        Given an line from the server standard output tells is this line means that the server is
        properly running.
        """
        raise NotImplementedError

    @staticmethod
    def _wrap_command(command: str) -> None:
        config: Config = Config()

        # cd to project directory
        wrapped_command: list[str] = ["cd", config.project_remote_path, "&&"]

        # Server command
        wrapped_command += command.split()

        return wrapped_command

    def _stop(self) -> None:
        self.stop_server()

        # Kill the ssh tunnel process.
        if self.ssh_tunnel is not None:
            self.ssh_tunnel.stop()

        # Finally, quit remi.
        sys.exit(0)

    # pylint: disable=unused-argument
    def _sigint_handler(self, signal_received, frame) -> None:
        """
        See more here (https://docs.python.org/3/library/signal.html#signal.signal).
        This function implements a signal handler
        """
        self._stop()

    def _standby_loop(self) -> None:
        """
        A loop that runs as long as the server is running and displays its output.
        """
        # Check if the server launch command have not failed (due to port busy).
        # In case it is running, wait to have the url (which contains the token).
        return_code: int = None
        server_stdout_line: str = ""
        while True:
            return_code = self.server_process.poll()

            # Case 1: the server is running
            if return_code is None:
                server_stdout_line = self.server_process.stdout.readline().strip()

                print(server_stdout_line)

                if self._server_start_callback(server_stdout_line):
                    break

            # Case 2: command failed
            # Example: a server was already running on this port
            elif return_code > 0:
                print_error(
                    f"{self.__class__.__name__} command failed with exit code {return_code}"
                )

                server_stdout_lines: list[str] = self.server_process.stdout.readlines()

                # Print stderr output
                for line in server_stdout_lines:
                    print(line.strip())

                # Kill the ssh tunnel process before leaving
                if self.ssh_tunnel is not None:
                    self.ssh_tunnel.stop()

                # Exit remi with a non-zero exit code
                sys.exit(1)

            else:
                print_info(f"{self.__class__.__name__} has exited succesfully.")

                # Kill the ssh tunnel process before leaving
                if self.ssh_tunnel is not None:
                    self.ssh_tunnel.stop()

                # Exit remi
                sys.exit(0)

    def start(self, callback: callable = None) -> None:
        """
        Run the server on the remote computer.
        """
        # First, sync the project
        push_inria()

        # Run the server

        # Server process
        self.server_process: Popen = run_remote_command_inria(
            command=self.server_start_command,
            hostname=self.hostname,
            background=True,
        )

        # Wait for the server to succesfully start.
        self._standby_loop()

        print_info("The server is now succesfully running !")

        # Then, open an ssh tunnel in the background (if working remotely)
        if gethostname() not in self.hostname:
            self.ssh_tunnel.start()

        # Catch Ctrl-c signal from local user and use it as a remote server killer.
        signal(SIGINT, self._sigint_handler)

        # If enabled, open the browser on the local machine.
        browser_cmd: str = Config().remote_servers.browser_cmd
        if self.open_browser and browser_cmd != "":
            print_info("Opening the service in the browser")

            # pylint: disable=consider-using-with
            Popen(args=browser_cmd.split() + [self.local_url])

        print_info("To quit, simply press `Ctrl+c`")

        self._standby_loop()

    def stop_server(self) -> None:
        run_remote_command_inria(
            command=self.server_stop_command,
            hostname=self.hostname,
            check=False,
        )


@click.command("ssh-tunnel")
@option_hostname
@option_port(service_name="ssh tunnel")
def ssh_bridge(hostname: str, port: int) -> None:
    """
    Run a standalone ssh tunnel.
    """
    ssh_tunnel: SshTunnel = SshTunnel(
        hostname=hostname,
        port=port,
    )
    ssh_tunnel.start()

    def _sigint_handler(signal_received, frame) -> None:
        ssh_tunnel.stop()

    signal(SIGINT, _sigint_handler)

    # Block indefinitely
    ssh_tunnel.process.wait()
