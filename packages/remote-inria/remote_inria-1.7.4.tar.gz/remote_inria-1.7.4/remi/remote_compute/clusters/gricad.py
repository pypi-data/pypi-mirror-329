"""
Run code on the GriCAD cluster.
"""

import sys
import subprocess
from typing import Union, Optional
from os.path import join, isfile

from termcolor import colored
import click

from ...cli_utils import OrderedGroup, option_no_push
from ..cli_utils import option_script, argument_command, option_no_build
from .cli_utils import argument_oar_job_id, argument_oar_job_id_list
from ...utils import run_remote_command, run_remote_command_inria
from ...user_interaction import print_info, to_bold, print_error, print_warning
from ... import config
from ...file_transfer import (
    push_,
    option_push_force,
    pull_,
    argument_pull_remote_path,
    option_pull_force,
    clean_,
    argument_clean_directory,
    option_clean_force,
)
from ..singularity import get_binding_sub_command, build_singularity_container
from .oarsub import print_cluster_request_prop, add_standard_output_params


def _get_ssh_proxy_command(cluster_name: str = None) -> str:
    g_config: config.Gricad = config.Config().gricad
    if not cluster_name:
        cluster_name = g_config.prefered_cluster

    ssh_proxy_command: str = (
        f"ProxyCommand ssh -q {g_config.username}@access-gricad.univ-grenoble-alpes.fr"
        f" nc -w 60 {cluster_name} 22"
    )

    return ssh_proxy_command


def _run_remote_command_gricad(
    command: list[str],
    cluster_name: str = None,
    check: bool = False,
    force_tty_allocation: bool = False,
) -> Union[subprocess.Popen, int]:
    g_config: config.Gricad = config.Config().gricad

    if not cluster_name:
        cluster_name = g_config.prefered_cluster

    hostname_args: list[str] = [
        "-o",
        _get_ssh_proxy_command(cluster_name=cluster_name),
        f"{g_config.username}@{cluster_name}",
    ]

    return run_remote_command(
        command=command,
        hostname=hostname_args,
        pretty_hostname=cluster_name,
        check=check,
        force_tty_allocation=force_tty_allocation,
    )


# pylint: disable=unused-argument
def _callback_option_gricad_job_name(ctx, param, value) -> str:
    if not value:
        return config.Config().gricad.oarsub.job_name

    return value


_option_gricad_job_name = click.option(
    "-n",
    "--job-name",
    default="",
    callback=_callback_option_gricad_job_name,
    help="Custom job name",
)


# pylint: disable=unused-argument
def _callback_option_container(ctx, param, value) -> str:
    if value:
        return value

    return config.Config().gricad.singularity_image


_option_container: click.option = click.option(
    "-c",
    "--container",
    "container",
    type=str,
    callback=_callback_option_container,
    help="The container image to use (.sif)",
)


# pylint: disable=unused-argument
def _callback_option_gricad_gpu_model(ctx, param, value) -> str:
    if not value:
        value = config.Config().gricad.oarsub.gpu_model

    # Give more flexibility w.r.t the input: 'a100' --> 'A100'
    value = value.upper()

    if value not in ["A100", "V100", "T4"]:
        print_error(
            f"Invalid `gpu_model` '{value}'." " Supported values are: 'A100', 'V100' and 'T4'."
        )
        sys.exit(1)

    return value


_option_gricad_gpu_model = click.option(
    "-g",
    "--gpu-model",
    callback=_callback_option_gricad_gpu_model,
    help="GPU model ('A100', 'V100' or 'T4')",
)


@click.group(cls=OrderedGroup, invoke_without_command=True)
@option_script
@_option_gricad_gpu_model
@_option_gricad_job_name
@option_no_push
@click.pass_context
def gricad(
    ctx,
    script_name: str,
    job_name: str,
    gpu_model: str,
    no_push: bool,
) -> None:
    """
    Run a script on the cluster (see config for options).
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(
            cluster_script,
            script_name=script_name,
            job_name=job_name,
            gpu_model=gpu_model,
            no_push=no_push,
        )


#########
# Setup ############################################################################################
#########


@gricad.command()
def setup() -> None:
    """
    Set up remote project on the Gricad cluster.
    """
    _config: config.Config = config.Config()
    g_config: config.Gricad = _config.gricad

    print_info(
        text=f"Setting up gricad project: {_config.project_name}",
        bold=True,
    )

    paths_to_create: str = g_config.project_remote_path
    paths_to_create += (
        "/{"
        + ",".join(
            [
                _config.output_path,
                _config.notebooks_path,
                _config.oarsub_log_path,
            ]
        )
        + "}"
    )

    # Create the project directory on the remote and the output folder within it.
    _run_remote_command_gricad(
        command=["mkdir", "-p", paths_to_create],
        check=True,
    )
    _push_gricad()

    print_info("Setup complete !")


########
# Push #############################################################################################
########


def _push_gricad(force: bool = False):
    g_config: config.Gricad = config.Config().gricad

    cluster_name: str = g_config.prefered_cluster

    print_info("Pushing project folder to gricad", bold=True)

    rsync_destination: str = f"{g_config.username}@{cluster_name}:{g_config.project_remote_path}"
    rsync_e_opt: str = f'ssh -o "{_get_ssh_proxy_command(cluster_name=cluster_name)}"'

    push_(
        rsync_destination=rsync_destination,
        rsync_e_opt=rsync_e_opt,
        last_push_fn_suffix="_gricad",
        force=force,
    )


@gricad.command()
@option_push_force
def push(force: bool) -> None:
    """
    Sync the project folder to the gricad storage.

    Args:
        force (bool):   Run the sync command even if no local changes were detected.
    """
    _push_gricad(force=force)


########
# Pull #############################################################################################
########


@gricad.command()
@argument_pull_remote_path
@option_pull_force
def pull(remote_path: str, force: bool) -> None:
    """
    Sync the content of the provided remote directories to the equivalent folder to the local
    machine.

    Args:
        remote_path (str):  The remote folder to sync to the local computer.
        force (bool):       Do not ask for a confirmation before pulling.
                                Eventually conflicting local files might be overridden.
    """
    g_config: config.Gricad = config.Config().gricad

    rsync_e_opt: str = f'ssh -o "{_get_ssh_proxy_command()}"'

    # Source
    source_prefix: str = (
        f"{g_config.username}@{g_config.prefered_cluster}:{g_config.project_remote_path}"
    )

    pull_(
        remote_path=remote_path,
        source_prefix=source_prefix,
        rsync_e_opt=rsync_e_opt,
        force=bool,
    )


#########
# Clean ############################################################################################
#########


@gricad.command()
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
        remote_path=config.Config().gricad.project_remote_path,
        force=force,
    )
    if clean_cmd:
        _run_remote_command_gricad(clean_cmd, check=False)


###############
# Singularity ######################################################################################
###############
def _sync_container_from_inria() -> None:
    _config: config.Config = config.Config()
    singularity_config = _config.singularity
    def_file_name: str = singularity_config.def_file_name

    if not isfile(def_file_name):
        print_warning(f"Recipe file not found (`{def_file_name}`). Aborting")
        return

    # Compare gricad_last_synced_recipe.def to last_build_recipe.def
    last_built_recipe_path: str = ".remi/last_built_recipe.def"
    last_synced_recipe_path: str = ".remi/gricad_last_synced_recipe.def"

    last_built_recipe: str = ""
    if isfile(last_built_recipe_path):
        with open(last_built_recipe_path, "r") as last_recipe_built_file:
            last_built_recipe = last_recipe_built_file.read()

    last_synced_recipe: str = ""
    if isfile(last_synced_recipe_path):
        with open(last_synced_recipe_path, "r") as last_synced_recipe_file:
            last_synced_recipe = last_synced_recipe_file.read()

        # Check if something has changed
        if last_synced_recipe == last_built_recipe:
            print_info("Nothing has changed since last sync. Cancelling.")
            return

    # Else, something has changed: so we sync the image to gricad.

    rsync_e_opt: str = f'ssh -o "{_get_ssh_proxy_command()}"'
    inria_sif_name: str = singularity_config.output_sif_name
    path_to_sif_inria: str = join(
        _config.project_remote_path,
        inria_sif_name,
    )
    gricad_config: config.Gricad = _config.gricad
    path_to_sif_gricad: str = join(
        gricad_config.project_remote_path,
        gricad_config.singularity_image,
    )
    rsync_destination: str = (
        f"{gricad_config.username}@{gricad_config.prefered_cluster}:{path_to_sif_gricad}"
    )

    # Run singularity build on Inria remote
    sync_command: list[str] = [
        "rsync",
        "-avP",
        "-e",
        f"'{rsync_e_opt}'",
        path_to_sif_inria,
        rsync_destination,
    ]

    print_info(
        to_bold("Syncing container image ")
        + "`"
        + colored(inria_sif_name, "yellow")
        + "`"
        + to_bold(" to GRICAD: ")
        + "`"
        + colored(path_to_sif_gricad, "yellow")
        + "`"
    )

    return_code: int = run_remote_command_inria(
        command=sync_command,
        check=True,
        force_tty_allocation=True,
    )

    if return_code == 0:
        print_info("Sync succesfull.")
        # If the build command succeeded, save the current recipe as the 'last built recipe'
        subprocess.run(
            [
                "cp",
                "-f",
                last_built_recipe_path,
                last_synced_recipe_path,
            ],
            check=True,
        )
    else:
        print_error(f"Sync failed with return code {return_code}")


###########
# Cluster ##########################################################################################
###########


def _print_cluster_request(
    oarsub_config: config.GricadOarsub,
    job_name: str,
    cluster_name: str,
    gpu_model: str,
    container_sif: str,
) -> None:
    print_info(to_bold("Cluster request:"))
    print_cluster_request_prop(
        property_name="Gricad cluster",
        value=cluster_name,
    )
    print_cluster_request_prop(
        property_name="Job name",
        value=job_name,
    )
    print_cluster_request_prop(
        property_name="Apptainer image",
        value=container_sif,
    )
    print_cluster_request_prop(
        property_name="Number of nodes",
        value=oarsub_config.num_nodes,
    )
    if oarsub_config.num_cpus > 0:
        print_cluster_request_prop(
            property_name="Number of CPUs",
            value=oarsub_config.num_cpus,
        )
    if oarsub_config.num_cpu_cores > 0:
        print_cluster_request_prop(
            property_name="Number of CPU cores",
            value=oarsub_config.num_cpu_cores,
        )

    print_cluster_request_prop(
        property_name="Number of GPUs",
        value=oarsub_config.num_gpus,
    )
    if oarsub_config.num_gpus > 0 and gpu_model:
        print_cluster_request_prop(
            property_name="GPU model",
            value=gpu_model,
        )

    print_cluster_request_prop(
        property_name="Walltime",
        value=oarsub_config.walltime,
    )


def get_oarsub_cmd_prefix(
    job_name: str,
    cluster_name: str,
    gpu_model: str,
    container_sif: str,
) -> list[str]:
    # Get the oarsub config
    g_config: config.Gricad = config.Config().gricad
    oarsub_config: config.GricadOarsub = g_config.oarsub

    # Oarsub command
    oarsub_cmd: list[str] = ["oarsub"]

    # Name the job
    oarsub_cmd += ["--name", job_name]

    # Resource list
    resource_list: str = f"/nodes={oarsub_config.num_nodes}"
    if oarsub_config.num_cpus > 0:
        resource_list += f"/cpu={oarsub_config.num_cpus}"
    if oarsub_config.num_cpu_cores > 0:
        resource_list += f"/core={oarsub_config.num_cpu_cores}"

    if oarsub_config.num_gpus > 0:
        resource_list += f"/gpu={oarsub_config.num_gpus}"

    if oarsub_config.walltime != "":
        resource_list += f",walltime={oarsub_config.walltime}"

    oarsub_cmd += ["-l", resource_list]

    if oarsub_config.num_gpus > 0 and gpu_model:
        oarsub_cmd += ["-p", f"\"gpumodel='{gpu_model}'\""]

    oarsub_cmd += ["--project", g_config.project_name]

    _print_cluster_request(
        oarsub_config=oarsub_config,
        job_name=job_name,
        cluster_name=cluster_name,
        gpu_model=gpu_model,
        container_sif=container_sif,
    )

    return oarsub_cmd


def _cluster(
    sub_command: str,
    script_name: str = "",
    command: tuple[str] = "",
    gpu_model: str = "",
    job_name: str = "",
    container_sif: str = "",
    no_push: bool = False,
    no_build: bool = False,
) -> None:
    assert sub_command in ["script", "interactive", "command"]

    # Sync project.
    if not no_push:
        _push_gricad()
        print()

    _config: config.Config = config.Config()
    g_config: config.Gricad = _config.gricad

    cluster_name: str = g_config.prefered_cluster

    oarsub_cmd: list[str] = get_oarsub_cmd_prefix(
        job_name=job_name,
        cluster_name=cluster_name,
        gpu_model=gpu_model,
        container_sif=container_sif,
    )

    # Interactive
    if sub_command == "interactive":
        print_info("Connecting to cluster in interactive mode", bold=True)
        oarsub_cmd += ["--interactive"]

    # Script or command
    else:
        if not no_build:
            print()
            build_singularity_container(
                output_sif_name=container_sif,
            )
            _sync_container_from_inria()

        oarsub_cmd += add_standard_output_params(
            oarsub_log_path=join(
                g_config.project_remote_path,
                _config.oarsub_log_path,
            ),
            base_name=g_config.oarsub.log_file_name,
        )

        job_cmd: list[str] = ["cd", g_config.project_remote_path, "&&"]

        use_container: bool = g_config.use_container

        if use_container:
            job_cmd += ["/usr/local/bin/singularity", "exec"]

            job_cmd += get_binding_sub_command(
                project_remote_path=g_config.project_remote_path,
                env_variables=_config.singularity.env_variables,
            )

            # Enable GPU support and provide the path to the container image
            job_cmd += ["--nv", container_sif]

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

        if _config.verbose:
            job_cmd_pretty: str = colored(" ".join(job_cmd), "cyan")
            print_info(f"Command to run on the cluster: {job_cmd_pretty}")

        oarsub_cmd += ['"' + " ".join(job_cmd) + '"']

    _run_remote_command_gricad(
        command=oarsub_cmd,
        cluster_name=cluster_name,
        check=True,
        force_tty_allocation=True,
    )


@gricad.command("script")
@option_script
@_option_gricad_gpu_model
@_option_gricad_job_name
@_option_container
@option_no_push
@option_no_build
def cluster_script(
    script_name: str,
    gpu_model: str,
    job_name: str,
    container: str,
    no_push: bool,
    no_build: bool,
) -> None:
    _cluster(
        sub_command="script",
        script_name=script_name,
        gpu_model=gpu_model,
        job_name=job_name,
        container_sif=container,
        no_push=no_push,
        no_build=no_build,
    )


@gricad.command("command")
@argument_command
@_option_gricad_gpu_model
@_option_gricad_job_name
@_option_container
@option_no_push
@option_no_build
def cluster_command(
    command: list[str],
    job_name: str,
    gpu_model: str,
    container: str,
    no_push: bool,
    no_build: bool,
) -> None:
    _cluster(
        sub_command="command",
        command=command,
        gpu_model=gpu_model,
        job_name=job_name,
        container_sif=container,
        no_push=no_push,
        no_build=no_build,
    )


@gricad.command("interactive")
@_option_gricad_gpu_model
@_option_gricad_job_name
@option_no_push
def cluster_interactive(
    job_name: str,
    gpu_model: str,
    no_push: bool,
) -> None:
    _cluster(
        sub_command="interactive",
        job_name=job_name,
        gpu_model=gpu_model,
        no_push=no_push,
    )


@gricad.command("chandler")
def cluster_chandler() -> None:
    """
    Run `chandler` on the cluster to list compute nodes occupation (free/busy).
    """
    _run_remote_command_gricad(
        command="chandler",
        force_tty_allocation=True,
        check=True,
    )


@gricad.command("recap")
def cluster_recap() -> None:
    """
    Run `recap.py` on the cluster to list compute nodes information (CPU, GPU…).
    """
    _run_remote_command_gricad(
        command="recap.py",
        force_tty_allocation=True,
        check=True,
    )


@gricad.command("stat")
def cluster_stat() -> None:
    """
    Get some information about your running/planned jobs thanks to `oarstat`.
    """
    _run_remote_command_gricad(
        command=f"oarstat -u {config.Config().gricad.username}",
        force_tty_allocation=True,
        check=True,
    )


@gricad.command("connect")
@argument_oar_job_id
def cluster_connect(oar_job_id: int) -> None:
    """
    Connect to a job on the cluster.

    Arguments:
        OAR_JOB_ID: The id of the job you want to kill (It has to have been run by you)'
    """
    _run_remote_command_gricad(
        command=f"oarsub -C {oar_job_id}",
        force_tty_allocation=True,
        check=True,
    )


@gricad.command("kill")
@argument_oar_job_id_list
def gricad_kill(oar_job_ids: tuple[int]) -> None:
    """
    Kill a job on the gricad cluster.

    Arguments:
        OAR_JOB_IDS: The ids of the jobs you want to kill (they have to have been run by you)'
    """
    oar_job_ids_str: str = " ".join(str(job_id) for job_id in oar_job_ids)
    _run_remote_command_gricad(
        command=f"oardel {oar_job_ids_str}",
        check=True,
    )
