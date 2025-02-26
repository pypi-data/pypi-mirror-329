"""
Functions specific to the Inria cluster.
"""

from os.path import join
import subprocess
from typing import Union

import click
from termcolor import colored

from ...config import Config
from ...user_interaction import to_bold, print_info
from ...file_transfer import push_inria
from ...utils import run_remote_command_inria
from ...cli_utils import OrderedGroup, option_no_push, option_xforwarding
from ..cli_utils import option_script, option_no_build, argument_command, option_container
from .cli_utils import argument_oar_job_id, argument_oar_job_id_list

from ..singularity import get_binding_sub_command, build_singularity_container
from .oarsub import get_oarsub_cmd_prefix, add_standard_output_params


def _run_remote_command_cluster(
    command: list[str],
    enable_x_forwarding: bool = False,
) -> Union[subprocess.Popen, int]:
    return run_remote_command_inria(
        command=command,
        hostname="access2-cp.inrialpes.fr",
        check=True,
        force_tty_allocation=True,
        enable_x_forwarding=enable_x_forwarding,
        use_bastion=True,
    )


def _cluster(
    sub_command: str,
    script_name: str = "",
    command: tuple[str] = "",
    host_id: str = "",
    job_name: str = "",
    container_sif: str = "",
    enable_x_forwarding: bool = False,
    no_build: bool = False,
    no_push: bool = False,
) -> None:
    assert sub_command in ["script", "interactive", "command"]

    # Sync project.
    if not no_push:
        push_inria()
        print()

    config: Config = Config()

    oarsub_cmd: list[str] = get_oarsub_cmd_prefix(
        job_name=job_name,
        host_id=host_id,
    )

    # Interactive
    if sub_command == "interactive":
        print_info("Connecting to cluster in interactive mode", bold=True)
        oarsub_cmd += ["--interactive"]

    # TODO

    # Script or command
    else:
        # X11 xforwarding makes no sense when not in interactive mode.
        enable_x_forwarding = False

        if not no_build:
            print()
            build_singularity_container(
                output_sif_name=container_sif,
            )
            print()

        oarsub_cmd += add_standard_output_params(
            oarsub_log_path=join(
                config.project_remote_path,
                config.oarsub_log_path,
            ),
            base_name=config.oarsub.log_file_name,
        )

        job_cmd: list[str] = ["cd", config.project_remote_path, "&&", "singularity", "exec"]

        # Path bindings between host system and singularity container
        job_cmd += get_binding_sub_command(
            project_remote_path=config.project_remote_path,
            bindings=config.singularity.bindings,
            env_variables=config.singularity.env_variables,
            no_home=config.singularity.no_home,
        )

        if config.singularity.bind_beegfs:
            job_cmd += ["--bind", f"/services/scratch/perception/{config.username}/:/beegfs/"]

        # Export the PYTHONPATH environment variable so as to use the project python module
        # job_cmd += ['--env', 'PYTHONPATH=.']

        if config.oarsub.num_gpus > 0:
            job_cmd.append("--nv")

        job_cmd.append(container_sif)

        if sub_command == "script":
            script_name_pretty: str = colored(script_name, "yellow")
            print_info(
                to_bold("Running script ")
                + colored(script_name_pretty, "yellow")
                + " on the cluster"
            )
            print()

            job_cmd += ["bash", script_name]

        elif sub_command == "command":
            command_merge: str = " ".join(command)
            command_merge_pretty: str = colored(command_merge, "yellow")
            print_info(
                to_bold("Running command ")
                + colored(command_merge_pretty, "yellow")
                + " on the cluster"
            )
            print()

            job_cmd += command

        if config.verbose:
            job_cmd_pretty: str = colored(" ".join(job_cmd), "cyan")
            print_info(f"Command to run on the cluster: {job_cmd_pretty}")

        oarsub_cmd += ['"' + " ".join(job_cmd) + '"']

    _run_remote_command_cluster(
        command=oarsub_cmd,
        enable_x_forwarding=enable_x_forwarding,
    )


#######
# CLI #
#######
# pylint: disable=unused-argument
def _callback_option_cluster_job_name(ctx, param, value) -> str:
    if not value:
        return Config().oarsub.job_name

    return value


_option_cluster_job_name = click.option(
    "-n",
    "--job-name",
    default="",
    callback=_callback_option_cluster_job_name,
    help="Custom job name",
)


# pylint: disable=unused-argument
def _callback_option_host_id(ctx, param, value) -> str:
    if not value:
        return Config().oarsub.host_id

    return value


_option_host_id = click.option(
    "-h",
    "--host",
    "host_id",
    default="",
    callback=_callback_option_host_id,
    type=str,
    help="A specific host id.",
)


@click.group(cls=OrderedGroup, invoke_without_command=True)
@option_script
@_option_host_id
@_option_cluster_job_name
@option_container
@option_no_push
@option_no_build
@click.pass_context
def cluster(
    ctx,
    script_name: str,
    job_name: str,
    host_id: str,
    container: str,
    no_push: bool,
    no_build: bool,
) -> None:
    """
    Run a script on the cluster (see config for options).
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            cluster_script,
            script_name=script_name,
            job_name=job_name,
            host_id=host_id,
            container=container,
            no_push=no_push,
            no_build=no_build,
        )


@cluster.command("script")
@option_script
@_option_host_id
@_option_cluster_job_name
@option_container
@option_no_push
@option_no_build
def cluster_script(
    script_name: str,
    host_id: str,
    job_name: str,
    container: str,
    no_push: bool,
    no_build,
) -> None:
    _cluster(
        sub_command="script",
        script_name=script_name,
        host_id=host_id,
        job_name=job_name,
        container_sif=container,
        no_push=no_push,
        no_build=no_build,
    )


@cluster.command("command")
@argument_command
@_option_host_id
@_option_cluster_job_name
@option_container
@option_no_push
@option_no_build
def cluster_command(
    command: list[str],
    host_id: str,
    job_name: str,
    container: str,
    no_push: bool,
    no_build: bool,
) -> None:
    _cluster(
        sub_command="command",
        command=command,
        host_id=host_id,
        job_name=job_name,
        container_sif=container,
        no_push=no_push,
        no_build=no_build,
    )


@cluster.command("interactive")
@_option_host_id
@_option_cluster_job_name
@option_xforwarding
@option_no_push
def cluster_interactive(
    host_id: str,
    job_name: str,
    x_forwarding: bool,
    no_push: bool,
) -> None:
    _cluster(
        sub_command="interactive",
        host_id=host_id,
        job_name=job_name,
        enable_x_forwarding=x_forwarding,
        no_push=no_push,
    )


@cluster.command("stat")
@click.option(
    "-t",
    "--team",
    default=False,
    is_flag=True,
    help="Query the current jobs for the RobotLearn team members",
)
def cluster_stat(
    team: bool,
) -> None:
    """
    Get the state of your jobs.
    """
    command: list[str] = ["oarstat"]

    if team:
        command += [
            "|",
            "grep",
            "'"
            + "\\|".join(
                (
                    "aauterna",
                    "aballou",
                    "creinke",
                    "galepage",
                    "lairale",
                    "visanche",
                    "wguo",
                    "xilin",
                    "xbie",
                    "yixu",
                )
            )
            + "'",
        ]
    else:
        command += ["-u", Config().username]

    _run_remote_command_cluster(
        command=command,
    )


@cluster.command("connect")
@argument_oar_job_id
def cluster_connect(oar_job_id: int) -> None:
    """
    Connect to a job on the cluster.

    Arguments:
        OAR_JOB_ID: The id of the job you want to kill (It has to have been run by you)'
    """
    _run_remote_command_cluster(
        command=f"oarsub -C {oar_job_id}",
    )


@cluster.command("kill")
@argument_oar_job_id_list
def cluster_kill(oar_job_ids: tuple[int]) -> None:
    """
    Kill a job on the cluster.

    Arguments:
        OAR_JOB_IDS: The ids of the jobs you want to kill (they have to have been run by you)'
    """
    oar_job_ids_str: str = " ".join(str(job_id) for job_id in oar_job_ids)
    _run_remote_command_cluster(
        command=f"oardel {oar_job_ids_str}",
    )
