"""
Default configuration.
"""

from os.path import join, isdir, isfile, basename
from os import mkdir, getcwd
from typing import Any
from socket import gethostname

from ..user_interaction import prompt_user_yes_no, prompt_user_value, print_info, print_warning


def _config_file_template(
    project_name: str,
    username: str,
    pc_name: str,
    project_remote_path: str,
    gricad_username: str = "GRICAD_USERNAME",
    gricad_prefered_cluster: str = "bigfoot",
    gricad_project_name: str = "GRICAD_PROJECT_NAME",
    gricad_project_remote_path: str = "GRICAD_PROJECT_REMOTE_PATH",
) -> str:
    return f"""# If true, makes remi's output more explicit
verbose: false

# Name for your project
project_name: {project_name}


# Inria username
username: {username}


# Location of the project on the remote computer
project_remote_path: {project_remote_path}


desktop:
  # Name of your Inria workstation
  hostname: {pc_name}

  ip_adress: {pc_name}.inrialpes.fr

  # Whether to use the singularity container when running jobs on the workstations.
  use_container: true

  # Desktop background jobs
  background:
    # Which backend to use (`screen` or `tmux`)
    backend: screen

    # Whether to keep the session alive after the job has ended.
    # It lets you attach to the session to see the program output.
    # If 'false', the session will be closed when the job is over and stdout/stderr will be
    # lost.
    # CAUTION: If true, you will have to manually re-attach and close the session.
    keep_session_alive: false


# Bastion used to ssh into Inria resources
bastion:
  enable: true
  hostname: ssh-gra.inria.fr
  username: {username}


# Singularity container options
singularity:
  # The name of the 'recipe' file (`.def`) to build the singularity container.
  def_file_name: container.def

  # The name of the singularity image.
  output_sif_name: container.sif

  # A dictionnary of binds for the singularity container.
  # If the value is empty (''), the mount point is the same as the path on the host.
  # By default, the project folder is bound within the singularity container: This configuration
  # then allows you to add extra locations.
  # Example:
  #     /path_on_host/my_data: /path_in_container/my_data
  bindings:

  # Whether to bind beegfs. (It will be available as `/beegfs/` in the container).
  bind_beegfs: false

  # A dictionnary of environment variables to pass to the container.
  # Example:
  #     FOO: bar
  #     TERM: xterm
  #     LONG: "This is a long sentence"
  #     NUMBER_OF_NEURONS: 56
  #     EMPTY:
  env_variables:

  # The HOMEDIR is mounted by default by singularity.
  # If you want to disable this behavior, set the following option to true.
  # Learn more: https://docs.sylabs.io/guides/3.1/user-guide/bind_paths_and_mounts.html#using-no-home-and-containall-flags
  no_home: false


# Oarsub options (for more details on `oarsub`, please refer to
# https://oar.imag.fr/docs/latest/user/commands/oarsub.html).
oarsub:

  # Job name
  job_name: {project_name}

  # Number of hosts requested.
  num_hosts: 1

  # Number of cpu cores requested.
  # If the value is 0, all the cores for the requested cpus will be used.
  num_cpu_cores: 0

  # Number of GPUs requested.
  # If the value is 0, no GPU will be requested (CPU only).
  num_gpus: 1

  # The maximum allowed duration for your job.
  walltime: '72:00:00'

  # The name of the requested cluster (perception, mistis, thoth...)
  cluster_name: perception

  # Optionnaly specify the id of a specific node (gpu3, node2...)
  host_id:

  # If the options above are too restricive for your use-case, you may
  # directly provide a property list that will be provided to `oarsub` with the
  # `-p` flag.
  custom_property_query:

  # Whether to schedule the job in the besteffort queue.
  besteffort: true

  # Whether to set the job as idempotent (see oarsub documentation for more details).
  idempotent: false

  # Template name for the log files.
  # By default the log files are named: YYYY-MM-DD_hh-mm-ss.JOB_ID.JOB_NAME.std[out, err]
  # Ex: 2022-06-12_14-47-52.7502202.bce_type2_EaConv1d.stdout
  #
  # You can use '%jobid%' and '%jobname%' to reference the job id and name.
  # '.stdout' and '.stdout' is appended at the end automatically.
  #
  # Example:
  #     log_file_name: 'oar_log_%jobid%_%jobname%'
  log_file_name:


gricad:
  username: {gricad_username}

  # The Gricad cluster (bigfoot, dahu, luke, froggy)
  prefered_cluster: {gricad_prefered_cluster}

  # The Gricad project you are a member of
  # see: https://gricad-doc.univ-grenoble-alpes.fr/en/services/perseus-ng/3_project/
  project_name: {gricad_project_name}

  # Location of the project on the remote computer
  project_remote_path: {gricad_project_remote_path}

  # Whether to use the singularity container when running jobs on Gricad
  use_container: true

  # The name of the singularity image.
  singularity_image: container.sif

  oarsub:

    # Job name
    job_name: {project_name}

    # Number of nodes requested.
    num_nodes: 1

    # Number of cpus requested (per requested node).
    # If the value is 0, all the cpus for the requested node will be used.
    num_cpus: 0

    # Number of cpu cores requested.
    # If the value is 0, all the cores for the requested cpus will be used.
    num_cpu_cores: 0

    # Number of GPUs requested.
    # If the value is 0, no GPU will be requested (CPU only).
    num_gpus: 1

    # GPU model (leave blank if you have no preference)
    # Possible values: 'A100', 'V100', 'T4'
    gpu_model: V100

    # The maximum allowed duration for your job.
    walltime: '48:00:00'

    # Template name for the log files.
    # By default the log files are named: YYYY-MM-DD_hh-mm-ss.JOB_ID.JOB_NAME.std[out, err]
    # Ex: 2022-06-12_14-47-52.7502202.bce_type2_EaConv1d.stdout
    #
    # You can use '%jobid%' and '%jobname%' to reference the job id and name.
    # '.stdout' and '.stdout' is appended at the end automatically.
    #
    # Example:
    #     log_file_name: 'oar_log_%jobid%_%jobname%'
    log_file_name:


# Remote servers
# Remote servers are applications that run on a remote computer and can be accessed from your local
# browser thanks to remi.
#
# Two such servers are supported right now:
# - Jupyter notebook
# - TensorBoard
remote_servers:
  # The command to run for opening the local browser (`<browser_cmd> <url>`)
  browser_cmd: firefox

  # Jupyter notebook
  jupyter:
    # The port (local and remote) for the server
    port: 8080

    # If true, automatically open the jupyter notebook in the local browser.
    open_browser: true

  # TensorBoard
  tensorboard:
    # The port (local and remote) for TensorBoard
    port: 9090

    # Directory from where to run tensorboard.
    logdir: 'output/'

    # If true, automatically open TensorBoard in the local browser.
    open_browser: true
"""


def create_default_project():
    """
    Generate the configuration file and the exclude file.
    """
    dot_remi: str = ".remi/"
    config_file: str = join(dot_remi, "config.yaml")

    if not isfile(config_file):
        print_info("Generating configuration file")
        cwd: str = basename(getcwd())
        project_name: str = prompt_user_value(
            question="Project_name",
            default_value=cwd,
        )
        username: str = prompt_user_value(question="Inria username")
        pc_name: str = prompt_user_value(question="Inria hostname (name of your desktop machine)")
        if gethostname() == pc_name:
            project_remote_path = getcwd()
        else:
            project_remote_path = "/".join(
                [
                    "/scratch",
                    pc_name,
                    username,
                    ".remi_projects",
                    project_name,
                ]
            )

        config_values: dict[str, Any] = {
            "project_name": project_name,
            "username": username,
            "project_remote_path": project_remote_path,
            "pc_name": pc_name,
        }

        # Gricad
        if prompt_user_yes_no(question="Configure Gricad ?"):
            config_values["gricad_username"]: str = prompt_user_value(question="Perseus username")

            config_values["gricad_project_name"]: str = prompt_user_value(
                question="Perseus project",
                default_value="pr-ml3ri",
            )
            config_values[
                "gricad_project_remote_path"
            ]: str = f"/bettik/{config_values['gricad_username']}/.remi_projects/{project_name}"

            config_values["gricad_prefered_cluster"]: str = prompt_user_value(
                question="Gricad cluster",
                default_value="bigfoot",
            )

        config_string: str = _config_file_template(**config_values)

    # Once the user has provided a config, create the `.remi/` directory
    if not isdir(dot_remi):
        print(f"Creating {dot_remi}")
        mkdir(dot_remi)

    # Then, dump the config to the config file if it doesn't already exists
    if not isfile(config_file):
        with open(config_file, "w") as file_stream:
            file_stream.write(config_string)

    else:
        print_warning(f"Config file (`{config_file}`) already exists: skipping.")

    exclude_file = join(dot_remi, "exclude.txt")

    # Create a .gitignore in `.remi/` to exclude everything but the config and exclude files.
    dot_gitignore_path: str = join(dot_remi, ".gitignore")
    if not isfile(dot_gitignore_path):
        with open(dot_gitignore_path, "w") as dot_gitignore:
            dot_gitignore.write("*\n")
            dot_gitignore.write("!config.yaml\n")
            dot_gitignore.write("!exclude.txt\n")

    if not isfile(exclude_file):
        print_info("Creating boilerplate exclude file")
        with open(str(exclude_file), "w") as file_stream:
            file_stream.write(
                "\n".join(
                    [
                        ".remi",
                        "output/",
                        "notebooks/",
                        ".git",
                        ".envrc",
                        "__pycache__",
                        ".ipynb_checkpoints",
                        "logs",
                        ".DS_Store",
                        ".*.swp",
                        "*.egg-info/",
                        "**/__pycache__/" ".idea",
                        ".mypy_cache/",
                        "venv/",
                        "*.sif",
                        "build-temp-*",
                        ".pytest_cache/",
                    ]
                )
            )
    else:
        print_warning(f"Exclude file (`{exclude_file}`) already exists: skipping.")

    print_info(
        "We have created a standard configurations file and exclude list specifying files"
        " and folders that shouldn't be copied to server."
    )
    print_info("You can edit them at `.remi/config.yaml` and `.remi/exclude.txt`")
