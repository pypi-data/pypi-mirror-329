"""
Run code on a remote desktop computer.
"""

from socket import gethostname
import click
import re
import sys

from ..cli_utils import OrderedGroup, option_hostname, option_xforwarding, option_no_push
from .cli_utils import (
    option_script,
    option_background,
    option_no_build,
    argument_command,
    option_container,
)

from ..config import Config
from ..user_interaction import to_bold, print_info, print_warning, colored, print_error
from ..utils import run_remote_command_inria
from ..file_transfer import push_inria
from .singularity import build_singularity_container, get_binding_sub_command


def _desktop(
    sub_command: str,
    hostname: str,
    script_name: str = "",
    background: bool = False,
    session_name: str = "",
    container_sif: str = "",
    attach: bool = False,
    command: tuple[str] = "",
    gpus: str = "",
    enable_x_forwarding: bool = False,
    no_push: bool = False,
    no_build: bool = False,
) -> None:
    assert sub_command in ["script", "interactive", "command"]

    # Sync project.
    if not no_push:
        push_inria()

    config: Config = Config()

    cmd: list[str] = ["cd", config.project_remote_path, "&&"]

    singularity_cmd: list[str] = []

    use_container: bool = config.desktop.use_container

    if use_container:
        if not no_build:
            build_singularity_container(
                output_sif_name=container_sif,
            )
            print()

        singularity_cmd = ["singularity"]
        if sub_command == "interactive":
            singularity_cmd.append("shell")
        else:
            singularity_cmd.append("exec")

        singularity_cmd += get_binding_sub_command(
            project_remote_path=config.project_remote_path,
            bindings=config.singularity.bindings,
            env_variables=config.singularity.env_variables,
            no_home=config.singularity.no_home,
        )

        if config.singularity.bind_beegfs:
            singularity_cmd += ["--bind", f"/mnt/beegfs/perception/{config.username}/:/beegfs/"]

        # Export the PYTHONPATH environment variable so as to use the project python module
        singularity_cmd += ["--env", "PYTHONPATH=."]

        if gpus:
            singularity_cmd += ["--env", f"CUDA_VISIBLE_DEVICES={gpus}"]

        # Enable GPU support and provide the path to the container image
        singularity_cmd += ["--nv", container_sif]

    # Interactive
    if sub_command == "interactive":
        if gethostname() in hostname:
            print_info(
                "Running an interactive session on this workstation.",
                bold=True,
            )

        else:
            print_info(
                f"Connecting to remote desktop ({hostname}) in interactive mode.",
                bold=True,
            )

        if use_container:
            cmd += singularity_cmd

        # No container
        else:
            cmd += ["exec", "bash"]

    # Script or command
    else:
        cmd_suffix: str = ""

        # Script
        if sub_command == "script":
            print_info(
                to_bold("Running script ")
                + colored(script_name, "yellow")
                + " on remote desktop "
                + colored(hostname, "magenta")
            )
            print()

            cmd_suffix += f"bash {script_name}"

        # Command
        else:
            assert len(command) > 0

            command_merge: str = " ".join(command)
            print_info(
                to_bold("Running command ")
                + colored(command_merge, "yellow")
                + " on remote desktop "
                + colored(hostname, "magenta")
            )
            print()

            cmd_suffix += command_merge

        # Use `screen` to run a command in the background.
        if background:
            if config.desktop.background.backend == "screen":
                cmd += ["screen", "-dmS"]
            elif config.desktop.background.backend == "tmux":
                cmd += ["tmux", "new-session", "-d"]

                # Set the session working directory to the project remote path
                cmd += ["-c", config.project_remote_path]

                # Name the session
                cmd += ["-s"]

            cmd += [session_name, "bash", "-c"]

            # If singularity + container, add singularity prefix in the cmd_suffix.
            if use_container:
                cmd_suffix = " ".join(singularity_cmd) + " " + cmd_suffix

            # Keep session alive
            if config.desktop.background.keep_session_alive:
                print_warning(
                    f"The `{config.desktop.background.backend}` session will be kept alive once the"
                    " job command will have exited.\n"
                    "You can run `remi desktop attach-session` to re-attach to the session."
                )
                cmd_suffix += "; exec bash"

            # Keep the session running only if the command fails
            else:
                cmd_suffix += " || exec bash"

            cmd_suffix = '"' + cmd_suffix + '"'

        # If not in background, the singularity cmd is appended as a list of arguments.
        elif use_container:
            cmd += singularity_cmd

        cmd.append(cmd_suffix)

    run_remote_command_inria(
        command=cmd,
        hostname=hostname,
        check=True,
        force_tty_allocation=True,
        enable_x_forwarding=enable_x_forwarding,
    )

    if background and attach:
        _attach_session(
            hostname=hostname,
            session_name=session_name,
        )


def _attach_session(
    hostname: str,
    session_name: str,
) -> None:
    background_backend: str = Config().desktop.background.backend

    cmd: list[str]
    if background_backend == "screen":
        cmd = ["screen", "-r", session_name]
    elif background_backend == "tmux":
        cmd = ["tmux", "attach-session", "-t", session_name]

    run_remote_command_inria(
        cmd,
        hostname=hostname,
        check=True,
        force_tty_allocation=True,
    )


#######
# CLI #
#######
_option_attach: click.option = click.option(
    "-a",
    "--attach",
    default=False,
    is_flag=True,
    help="Automatically attach to screen/tmux session (Only useful when `background` is enabled.",
)


# pylint: disable=unused-argument
def _callback_option_session_name(ctx, param, value) -> str:
    # Make sure the script is a valid file
    if value:
        return value

    return Config().project_name


_option_session_name: click.option = click.option(
    "-n",
    "--name",
    "session_name",
    type=str,
    callback=_callback_option_session_name,
    help="Manually name the screen/tmux session",
)


# pylint: disable=unused-argument
def _callback_option_gpus(ctx, param, value) -> str:
    if (value is not None) and (not re.fullmatch(r"[0-9](,[0-9])*", value)):
        print_error(
            f"Provided value (`{value}`) for the -g/--gpus option is invalid."
            "\nIt should be one or several GPU ids."
            "\nExamples: `0`, `0,1`, `1,3,4`"
        )
        sys.exit(1)

    return value


_option_gpus: click.option = click.option(
    "-g",
    "--gpus",
    "gpus",
    type=str,
    callback=_callback_option_gpus,
    help="The value for `$CUDA_VISIBLE_DEVICES` (e.g.: '1,2')",
)


@click.group(cls=OrderedGroup, invoke_without_command=True)
@click.pass_context
@option_script
@option_hostname
@option_background
@_option_session_name
@option_container
@_option_attach
@_option_gpus
@option_xforwarding
@option_no_push
@option_no_build
def desktop(
    ctx,
    script_name: str,
    background: bool,
    session_name: str,
    container: str,
    attach: bool,
    hostname: str,
    gpus: str,
    x_forwarding: bool,
    no_push: bool,
    no_build: bool,
) -> None:
    """
    Run a script on the remote workstation.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            desktop_script,
            script_name=script_name,
            hostname=hostname,
            background=background,
            session_name=session_name,
            container=container,
            attach=attach,
            gpus=gpus,
            x_forwarding=x_forwarding,
            no_push=no_push,
            no_build=no_build,
        )


@desktop.command("script")
@option_script
@option_hostname
@option_background
@_option_session_name
@option_container
@_option_attach
@_option_gpus
@option_xforwarding
@option_no_push
@option_no_build
def desktop_script(
    script_name: str,
    hostname: str,
    background: bool,
    session_name: str,
    container: str,
    attach: bool,
    gpus: str,
    x_forwarding: bool,
    no_push: bool,
    no_build,
) -> None:
    _desktop(
        sub_command="script",
        script_name=script_name,
        hostname=hostname,
        background=background,
        session_name=session_name,
        container_sif=container,
        attach=attach,
        gpus=gpus,
        enable_x_forwarding=x_forwarding,
        no_push=no_push,
        no_build=no_build,
    )


@desktop.command("command")
@option_hostname
@option_background
@_option_session_name
@option_container
@_option_attach
@_option_gpus
@option_xforwarding
@option_no_push
@option_no_build
@argument_command
def desktop_command(
    command: list[str],
    background: bool,
    session_name: str,
    container: str,
    attach: bool,
    hostname: str,
    gpus: str,
    x_forwarding: bool,
    no_push: bool,
    no_build: bool,
) -> None:
    _desktop(
        sub_command="command",
        command=command,
        background=background,
        session_name=session_name,
        container_sif=container,
        attach=attach,
        hostname=hostname,
        gpus=gpus,
        enable_x_forwarding=x_forwarding,
        no_push=no_push,
        no_build=no_build,
    )


@desktop.command("interactive")
@option_hostname
@option_container
@_option_gpus
@option_xforwarding
@option_no_push
@option_no_build
def desktop_interactive(
    hostname: str,
    container: str,
    gpus: str,
    x_forwarding: bool,
    no_push: bool,
    no_build: bool,
) -> None:
    _desktop(
        sub_command="interactive",
        hostname=hostname,
        container_sif=container,
        gpus=gpus,
        enable_x_forwarding=x_forwarding,
        no_push=no_push,
        no_build=no_build,
    )


argument_session_name: click.argument = click.argument(
    "session_name",
    default="",
    type=str,
    callback=_callback_option_session_name,
    nargs=1,
)


@desktop.command("attach-session")
@argument_session_name
@option_hostname
def desktop_attach_session(
    hostname: str,
    session_name: str,
) -> None:
    _attach_session(
        hostname=hostname,
        session_name=session_name,
    )
