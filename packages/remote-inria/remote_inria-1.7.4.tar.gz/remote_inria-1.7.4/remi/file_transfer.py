"""
Commands related to file management and transfer:
- push
- pull
- clean
"""

from os import getcwd
from os.path import isfile, join
from typing import Optional

import click
from termcolor import colored

from .config import Config
from .user_interaction import print_info, print_warning, prompt_user_yes_no
from .utils import run_local_cmd, run_remote_command_inria
from .cli_utils import option_force


########
# Push #############################################################################################
########


def push_(
    rsync_destination: str,
    rsync_e_opt: str = None,
    last_push_fn_suffix: str = "",
    force: bool = False,
) -> None:
    """
    Sync the project folder to the remote workstation.

    Args:
        force (bool):   Run the sync command even if no local changes were detected.
    """
    config: Config = Config()

    rsync_cmd: list[str] = [
        "rsync",
        "-zravut",
        "--human-readable",
        "--executability",
        "--delete",
    ]

    if isfile(config.exclude_file):
        rsync_cmd.append(f"--exclude-from='{config.exclude_file}'")

    # Source
    rsync_cmd.append(".")

    # Smart push
    # The 'smart push' mechanism stores the folder state (list of files along with their timestamps
    # and size) at each push. Then we are able to check if something has changed locally
    # since last push and run the rsync push command only if necessary.
    # This avoids opening a useless ssh tunnel with the server (which can sometimes last a few
    # seconds).
    last_push_file_path: str = f".remi/last_push{last_push_fn_suffix}.log"
    last_push_file_path_temp: str = f".remi/.last_push_temp{last_push_fn_suffix}.log"

    def _get_last_push_log(filename) -> str:
        _last_push_log: str = ""
        if isfile(filename):
            with open(filename, "r") as last_push_log_file:
                _last_push_log = last_push_log_file.read()

        return _last_push_log

    rsync_check_cmd: list[str] = rsync_cmd + ["--list-only", ">", last_push_file_path_temp]

    # Run rsync check command
    run_local_cmd(command=rsync_check_cmd, check=True)

    if (
        _get_last_push_log(last_push_file_path) == _get_last_push_log(last_push_file_path_temp)
        and not force
    ):
        print_info("Nothing has changed since last push. Cancelling push.")
        return

    # Eventually, add remote shell option (for proxy-jumping)
    if rsync_e_opt:
        rsync_cmd += ["-e", f"'{rsync_e_opt}'"]

    # Else, something has changed: so we sync with remote.
    rsync_cmd.append(rsync_destination)

    # Run the rsync command
    run_local_cmd(command=rsync_cmd, check=True)

    # Now that we know the sync was succesfull, store the sync state permanently
    run_local_cmd(["mv", last_push_file_path_temp, last_push_file_path])


def push_inria(force: bool = False) -> None:
    config: Config = Config()

    # Not pushing if already working from Inria.
    if config.working_from_inria and (
        getcwd()
        in (
            # /scratch/HOSTNAME/PATH
            config.project_remote_path,
            # /local_scratch/PATH
            config.project_remote_path.replace(
                f"/scratch/{config.desktop.hostname}/",
                "/local_scratch/",
            ),
        )
    ):
        print_warning(
            "You seem to be working directly from your Inria desktop and the `project_remote_path`"
            " defined in the config file is the same as the current working directory."
            f"\n=> Nothing will get 'pushed' and the current working directory (`{getcwd()}`) will"
            " be used by the cluster and other Inria desktops to access the project files."
        )
        return

    host_str: str = colored(config.desktop.ip_adress, "cyan")
    print_info(
        f"Pushing project folder to remote host `{host_str}`",
        bold=True,
    )

    rsync_destination: str
    rsync_e_opt: str = ""

    if config.working_from_inria:
        # Destination
        rsync_destination = config.project_remote_path

    else:
        # Bastion
        if config.bastion.enable:
            rsync_e_opt = f"ssh -J {config.username}@{config.bastion.hostname}"

        # Destination
        rsync_destination = (
            f"{config.username}@{config.desktop.ip_adress}:{config.project_remote_path}"
        )

    push_(
        rsync_destination=rsync_destination,
        rsync_e_opt=rsync_e_opt,
        force=force,
    )


option_push_force = option_force(
    help_message="Push the project even though no local changes were noticed."
)


@click.command()
@option_push_force
def push(force: bool) -> None:
    """
    Sync the project folder to the remote workstation.

    Args:
        force (bool):   Run the sync command even if no local changes were detected.
    """
    push_inria(force=force)


########
# Pull #############################################################################################
########


# pylint: disable=unused-argument
def _callback_argument_output_path_default(ctx, param, value) -> str:
    if value == "":
        return Config().output_path

    return value


argument_pull_remote_path: click.argument = click.argument(
    "remote_path",
    default="",
    type=str,
    callback=_callback_argument_output_path_default,
    nargs=1,
)

option_pull_force: click.option = option_force(
    help_message="Do not prompt for any confirmation.",
)


def pull_(
    remote_path: str,
    source_prefix: str,
    rsync_e_opt: str = None,
    force: bool = False,
) -> None:
    is_dir: bool = remote_path.endswith("/")
    node_type: str = "directory" if is_dir else "file"

    if not force:
        if not is_dir:
            print_info("Assuming that the provided path targets a FILE.")
            print_warning(
                f"==> If you meant to target a DIRECTORY, add a `/` at the end --> `{remote_path}/`"
            )

    remote_path_str: str = colored(remote_path, "cyan")
    print_info(
        f"Pulling {node_type} `{remote_path_str}` from the remote host",
        bold=True,
    )

    rsync_cmd: list[str] = [
        "rsync",
        "-zravut",
        "--human-readable",
        "--executability",
    ]

    # Eventually, add remote shell option (for proxy-jumping)
    if rsync_e_opt:
        rsync_cmd += ["-e", f"'{rsync_e_opt}'"]

    # Source
    rsync_cmd.append(join(source_prefix, remote_path))

    # Destination (copy at the same path on the local computer)
    rsync_cmd.append(remote_path)

    run_local_cmd(command=rsync_cmd, check=True)


@click.command()
@argument_pull_remote_path
@option_pull_force
def pull(
    remote_path: str,
    force: bool,
) -> None:
    """
    Sync the content of the provided remote directories to the equivalent folder to the local
    machine.

    Args:
        remote_path (str):  The remote folder to sync to the local computer.
        force (bool):       Do not ask for a confirmation before pulling.
                                Eventually conflicting local files might be overridden.
    """
    config: Config = Config()
    source_prefix: str = config.project_remote_path

    rsync_e_opt: str = ""

    # Not pushing if already working from Inria.
    if config.working_from_inria:
        if getcwd() == config.project_remote_path:
            print_warning(
                "You seem to be working directly from your Inria desktop and the"
                " `project_remote_path` defined in the config file is the same as the current"
                " working directory."
                "\n=> Nothing will get 'pulled'."
            )
            return

    else:
        # Bastion
        if config.bastion.enable:
            rsync_e_opt = f"ssh -J {config.username}@{config.bastion.hostname}"

        # Source
        source_prefix = f"{config.username}@{config.desktop.ip_adress}:" + source_prefix

    pull_(
        remote_path=remote_path,
        source_prefix=source_prefix,
        rsync_e_opt=rsync_e_opt,
        force=bool,
    )


#########
# Clean ############################################################################################
#########

option_clean_force: click.option = option_force(
    help_message="Do not ask for confirmation before deleting the folder content."
)
argument_clean_directory: click.argument = click.argument(
    "directory",
    default="",
    type=str,
    callback=_callback_argument_output_path_default,
    nargs=1,
)


def clean_(
    directory: str,
    force: bool,
    remote_path: str,
) -> Optional[list[str]]:
    directory_str: str = directory
    if not directory_str.endswith("/"):
        directory_str += "/"
    directory_str = colored(directory_str, "cyan")
    if force or prompt_user_yes_no(
        question=f"Do you really want to delete the content of the `{directory_str}` directory"
        " on the remote location ?"
    ):
        print_info(
            text=f"Cleaning folder `{directory_str}` on the remote location.",
            bold=True,
        )

        clean_cmd: list[str] = ["rm", "-rf", join(remote_path, directory, "*")]

        return clean_cmd

    print_info("Aborting.")


@click.command()
@option_clean_force
@argument_clean_directory
def clean(directory: str, force: bool) -> None:
    """
    Clean the content of a folder on the remote computer.

    Args:
        directory (str):        The directory of which content should be deleted.
        force (bool):           Do not ask for a confirmation before cleaning.
    """
    clean_cmd: Optional[list[str]] = clean_(
        directory=directory,
        remote_path=Config().project_remote_path,
        force=force,
    )
    if clean_cmd:
        run_remote_command_inria(clean_cmd, check=False)
