"""
Utility functions for remi.
"""

import sys
import subprocess
from datetime import datetime, timedelta
from os.path import join
from socket import gethostname
from subprocess import Popen, DEVNULL
from typing import Union
from termcolor import colored

from .config import Config
from .user_interaction import to_bold, print_info, print_error


def run_local_cmd(
    command: list[str],
    check: bool = True,
    background: bool = False,
    redirect_output: bool = False,
) -> Union[subprocess.Popen, int]:
    """
    Run a command on the local computer.

    Args:
        command (list[str]):        The command to run.
        check (bool):               If True, raise an exception if the command fails.
        background (bool):          Run the command in the background.
        redirect_output (bool):     Redirects command standard and error outputs to
                                        `output/log.txt`.

    Returns:
        popen (subprocess.Popen):   If `background is True: the Popen object corresponding to the
                                        running command. (if background)
        return_code (int):          Else, the return code of the command.
    """
    config: Config = Config()
    if config.verbose:
        print_info(
            to_bold("Running command locally: ") + colored(" ".join(command), "blue"),
        )

    if redirect_output:
        log_file: str = join(config.output_path, "log.txt")
        command += [">>", log_file, "2>&1"]
        print_info(f"stdout and stderr will be logged to {log_file}")

    command = ["bash", "-c", " ".join(command)]

    # Run in background
    if background:
        print_info("Background mode enabled")
        # pylint: disable=consider-using-with
        return subprocess.Popen(
            args=command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
        )

    # If check is True, catch CalledProcessError exception and exit program with error.
    # Else, get the return_code and return it.
    try:
        return subprocess.run(command, check=check).returncode
    except subprocess.CalledProcessError:
        print_error(text="Local command failed. Exiting.")
        sys.exit(1)


def run_remote_command_inria(
    command: list[str],
    hostname: str = None,
    check: bool = False,
    background: bool = False,
    force_tty_allocation: bool = False,
    enable_x_forwarding: bool = False,
    redirect_output: bool = False,
    use_bastion: bool = None,
) -> Union[subprocess.Popen, int]:
    config: Config = Config()

    if not hostname:
        hostname = config.desktop.ip_adress

    if use_bastion is None:
        use_bastion = config.bastion.enable

    # If we are already connected to the remote, the command has to be run locally.
    if gethostname() in hostname:
        return run_local_cmd(
            command=command,
            check=check,
            background=background,
            redirect_output=redirect_output,
        )

    hostname_args: list[str] = []

    # Bastion ProxyJump (useless when working from an Inria computer)
    if not config.working_from_inria and use_bastion:
        hostname_args += ["-J", f"{config.username}@{config.bastion.hostname}"]

    hostname_args += [f"{config.username}@{hostname}"]

    return run_remote_command(
        command=command,
        hostname=hostname_args,
        pretty_hostname=hostname,
        check=check,
        background=background,
        force_tty_allocation=force_tty_allocation,
        enable_x_forwarding=enable_x_forwarding,
        redirect_output=redirect_output,
    )


def run_remote_command(
    command: list[str],
    hostname: str,
    pretty_hostname: str = None,
    check: bool = False,
    background: bool = False,
    force_tty_allocation: bool = False,
    enable_x_forwarding: bool = False,
    redirect_output: bool = False,
) -> Union[subprocess.Popen, int]:
    """
    Run a command on a remote computer.

    Args:
        command (list[str]):            A command to run remotely.
        hostname (str):                 The hostname of the computer to run the command on.
        pretty_hostname (str):          The hostname to display in the standard output.
        check (bool):                   If True, raise an exception if the command fails.
        background (bool):              Run the command in the background.
        force_tty_allocation (bool):    Force pseudo-terminal allocation.
        enable_x_forwarding (bool):     Enables X forwarding
        redirect_output (bool):         Redirects command standard and error outputs to
                                            `output/log.txt`.

    Returns:
        popen (subprocess.Popen):   If `background is True: the Popen object corresponding to the
                                        running command. (if background)
        return_code (int):          Else, the return code of the command.
    """
    config: Config = Config()

    cmd: list[str] = ["ssh"]

    if force_tty_allocation:
        cmd.append("-t")

    if enable_x_forwarding:
        cmd.append("-X")

    cmd += hostname if isinstance(hostname, list) else [hostname]

    if isinstance(command, str):
        command = [command]

    cmd += command

    if config.verbose:
        print_info(
            to_bold("Running command remotely: ") + colored(" ".join(command), "blue"),
        )
        if pretty_hostname is None:
            pretty_hostname = hostname[-1] if isinstance(hostname, list) else hostname

        print_info(
            to_bold("on remote host: ") + colored(str(pretty_hostname), "magenta"),
        )

    if redirect_output:
        log_file: str = join(config.output_path, "log.txt")
        cmd += [">>", log_file, "2>&1"]
        print_info(f"stdout and stderr will be logged to {log_file}")
        print_info("Use `remi pull-output` to sync them to your local machine.")

    # Run in background
    if background:
        print_info("Background mode enabled")
        # pylint: disable=consider-using-with
        return subprocess.Popen(
            args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
        )

    # Check the time the command takes to run
    start_time: float = datetime.now()

    return_code: int

    # Run directly (not in background)
    # If check is True, catch CalledProcessError exception and exit program with error.
    # Else, get the return_code and return it.
    try:
        return_code = subprocess.run(cmd, check=check).returncode
    except subprocess.CalledProcessError:
        print_error(
            text="Remote command failed. Exiting.",
            newline=True,
        )
        sys.exit(1)

    duration: timedelta = datetime.now() - start_time
    print_info(
        f"Command ran succesfully. It took: {str(duration).split('.')[0]}.",
        newline=True,
    )

    return return_code


def create_remote_directory(
    path: str,
    hostname: str = None,
) -> None:
    """
    Create a directory on the remote desktop if it does not exist yet.

    Args:
        path (str):         The absolute path to the remote directory.
        hostname (str):     The hostname of the remote computer.
    """
    run_remote_command_inria(
        command=["mkdir", "-p", path],
        hostname=hostname,
        check=True,
    )


def run_ssh_tunnel(
    hostname: str,
    port: int,
) -> Popen:
    config: Config = Config()

    print_info(f"Running SSH port forwarding for port {port}")
    print_info(to_bold("on host: ") + str(hostname))
    ssh_tunnel_cmd: list[str] = ["ssh", "-N"]

    ssh_tunnel_cmd += ["-L", f"{port}:localhost:{port}"]

    # Bastion ProxyJump
    if config.bastion.enable:
        ssh_tunnel_cmd += ["-J", f"{config.username}@{config.bastion.hostname}"]

    ssh_tunnel_cmd.append(f"{config.username}@{hostname}")

    print_info(to_bold("SSH tunnel command: ") + " ".join(ssh_tunnel_cmd))

    # pylint: disable=consider-using-with
    return Popen(
        args=ssh_tunnel_cmd,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
