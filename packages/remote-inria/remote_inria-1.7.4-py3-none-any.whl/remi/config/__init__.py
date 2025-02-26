"""
Configuration management for remi.
"""

import sys
from os.path import join, isfile, basename, abspath
from typing import Any
from abc import ABC
from dataclasses import dataclass
from socket import gethostname
import yaml

from ..user_interaction import print_error

_DOT_REMI_PATH: str = ".remi/"
_CONFIG_FILE_NAME: str = "config.yaml"

_CONFIG = None


class Singleton(type):
    """
    Implementation of the singleton pattern.
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


@dataclass
class Background:
    backend: str
    keep_session_alive: bool

    @classmethod
    def from_dict(cls, args_dict: dict[str, Any]) -> "Background":
        return cls(
            backend=args_dict.get("backend", "screen"),
            keep_session_alive=args_dict.get("keep_session_alive", False),
        )


@dataclass
class Desktop:
    hostname: str
    ip_adress: str
    use_container: bool
    background: Background

    @classmethod
    def from_dict(cls, args_dict: dict[str, Any]) -> "Desktop":
        background_dict: dict[str, Any] = args_dict.get("background", {})
        background: Background = Background.from_dict(args_dict=background_dict)
        assert background.backend in (
            "screen",
            "tmux",
        ), "`background.backend` should be one of `screen` or `tmux`."

        return cls(
            hostname=args_dict.get("hostname"),
            ip_adress=args_dict.get("ip_adress"),
            use_container=args_dict.get("use_container", True),
            background=background,
        )


@dataclass
class Bastion:
    enable: bool
    hostname: str
    username: str

    @classmethod
    def from_dict(cls, args_dict: dict[str, Any]) -> "Bastion":
        return cls(
            enable=args_dict.get("enable", True),
            hostname=args_dict.get("hostname"),
            username=args_dict.get("username"),
        )


@dataclass
class Oarsub:
    _default_walltime: str = "72:00:00"

    job_name: str = ""
    num_hosts: int = 1
    num_cpu_cores: int = 0
    num_gpus: int = 0
    walltime: str = _default_walltime
    cluster_name: str = ""
    host_id: str = ""
    custom_property_query: str = ""
    besteffort: bool = True
    idempotent: bool = False
    log_file_name: str = ""

    @classmethod
    def from_dict(cls, args_dict: dict[str, Any], default_job_name: str) -> "Oarsub":
        return cls(
            job_name=args_dict.get("job_name", default_job_name),
            num_hosts=args_dict.get("num_hosts", 1),
            num_cpu_cores=args_dict.get("num_cpu_cores", 0),
            num_gpus=args_dict.get("num_gpus", 1),
            walltime=args_dict.get("walltime", cls._default_walltime),
            cluster_name=args_dict.get("cluster_name", "perception"),
            host_id=args_dict.get("host_id", ""),
            custom_property_query=args_dict.get("custom_property_query", ""),
            besteffort=args_dict.get("besteffort", True),
            idempotent=args_dict.get("idempotent", False),
            log_file_name=args_dict.get("log_file_name", ""),
        )


@dataclass
class Singularity:
    def_file_name: str
    output_sif_name: str
    bindings: dict[str, str]
    bind_beegfs: bool
    env_variables: dict[str, str | int]
    no_home: bool

    @classmethod
    def from_dict(
        cls,
        args_dict: dict[str, Any],
    ) -> "Singularity":
        return cls(
            output_sif_name=args_dict.get("output_sif_name", "container.sif"),
            def_file_name=args_dict.get("def_file_name", "container.def"),
            bindings=args_dict.get("bindings", {}),
            bind_beegfs=args_dict.get("bind_beegfs", False),
            env_variables=args_dict.get("env_variables", {}),
            no_home=args_dict.get("no_home", False),
        )


@dataclass
class GricadOarsub(Oarsub):
    _default_walltime: str = "48:00:00"

    num_nodes: int = 1
    num_cpus: int = 0
    gpu_model: str = ""
    log_file_name: str = ""

    @classmethod
    def from_dict(
        cls,
        args_dict: dict[str, Any],
        default_job_name: str,
    ) -> "GricadOarsub":
        return cls(
            job_name=args_dict.get("job_name", default_job_name),
            num_nodes=args_dict.get("num_nodes", 1),
            num_cpus=args_dict.get("num_cpus", 0),
            num_cpu_cores=args_dict.get("num_cpu_cores", 0),
            num_gpus=args_dict.get("num_gpus", 1),
            gpu_model=args_dict.get("gpu_model", ""),
            walltime=args_dict.get("walltime", cls._default_walltime),
            log_file_name=args_dict.get("log_file_name", ""),
        )


@dataclass
class Gricad:
    username: str
    project_name: str
    prefered_cluster: str
    project_remote_path: str
    use_container: bool
    singularity_image: str
    oarsub: GricadOarsub

    @classmethod
    def from_dict(
        cls,
        args_dict: dict[str, Any],
        default_job_name: str,
    ) -> "Gricad":
        oarsub_dict: dict[str, Any] = args_dict.get("oarsub", {})
        oarsub: GricadOarsub = GricadOarsub.from_dict(
            args_dict=oarsub_dict,
            default_job_name=default_job_name,
        )

        return cls(
            username=args_dict.get("username"),
            project_name=args_dict.get("project_name"),
            project_remote_path=args_dict.get("project_remote_path"),
            prefered_cluster=args_dict.get("prefered_cluster", "bigfoot"),
            use_container=args_dict.get("use_container", True),
            singularity_image=args_dict.get("singularity_image", "container.sif"),
            oarsub=oarsub,
        )


@dataclass
class RemoteServer(ABC):
    port: int
    open_browser: bool


@dataclass
class TensorBoard(RemoteServer):
    logdir: str

    @classmethod
    def from_dict(cls, args_dict: dict[str, Any]) -> "TensorBoard":
        return cls(
            port=args_dict.get("port", 9090),
            logdir=args_dict.get("logdir", "output/"),
            open_browser=args_dict.get("open_browser", True),
        )


@dataclass
class Jupyter(RemoteServer):
    @classmethod
    def from_dict(cls, args_dict: dict[str, Any]) -> "Jupyter":
        return cls(
            port=args_dict.get("port", 8080), open_browser=args_dict.get("open_browser", True)
        )


@dataclass
class Aim(RemoteServer):
    repo: str

    @classmethod
    def from_dict(
        cls,
        args_dict: dict[str, Any],
    ) -> "Aim":
        return cls(
            port=args_dict.get("port", 43800),
            repo=args_dict.get("repo", "output/"),
            open_browser=args_dict.get("open_browser", True),
        )


@dataclass
class RemoteServers:
    browser_cmd: str
    jupyter: Jupyter
    tensorboard: TensorBoard
    aim: Aim


# pylint: disable=too-few-public-methods
class Config(metaclass=Singleton):
    """
    A class storing all the configuration.
    """

    def __init__(self) -> None:
        config_path: str = join(_DOT_REMI_PATH, _CONFIG_FILE_NAME)
        if not isfile(config_path):
            print_error(
                f"Configuration file (`{config_path}`) was not found ! Exiting."
                "\nYou might want to `cd` to your project or to run"
                " `remi init` if you have not done it yet."
            )
            sys.exit(1)

        with open(config_path, "r") as file_stream:
            config_dict: dict[str, Any] = yaml.load(file_stream.read(), yaml.FullLoader)

        self.initialize_from_dict(config_dict=config_dict)

    def initialize_from_dict(self, config_dict: dict[str, Any]) -> None:
        self.verbose: bool = config_dict.get("verbose", False)

        self.project_name: str = config_dict.get("project_name", basename(abspath(".")))
        self.username: str = config_dict.get("username", "")
        self.exclude_file: str = config_dict.get(
            "exclude_file", join(_DOT_REMI_PATH, "exclude.txt")
        )

        # Desktop
        self.desktop: Desktop = Desktop.from_dict(args_dict=config_dict.get("desktop"))

        self.project_remote_path: str = config_dict.get(
            "project_remote_path",
            "/".join(
                [
                    "/scratch",
                    self.desktop.hostname,
                    self.username,
                    ".remi_projects",
                    self.project_name,
                ]
            ),
        )
        self.working_from_inria: bool
        if gethostname() == self.desktop.hostname:
            self.working_from_inria = True
        else:
            self.working_from_inria = False
        self.output_path: str = "output/"
        self.notebooks_path: str = "notebooks/"
        self.oarsub_log_path: str = join(self.output_path, "oarsub_logs/")

        # Bastion
        self.bastion: Bastion = Bastion.from_dict(
            args_dict=config_dict.get("bastion"),
        )

        # Oarsub
        cluster_oarsub_dict: dict[str, Any] = config_dict.get("oarsub")
        self.oarsub: Oarsub = Oarsub.from_dict(
            args_dict=cluster_oarsub_dict,
            default_job_name=self.project_name,
        )

        # Singularity
        self.singularity: Singularity = Singularity.from_dict(
            args_dict=config_dict.get("singularity")
        )

        # Gricad
        if "gricad" in config_dict:
            self.gricad: Gricad = Gricad.from_dict(
                args_dict=config_dict.get("gricad", {}),
                default_job_name=self.project_name,
            )

        # Remote servers
        remote_servers_dict: dict[str, Any] = config_dict.get("remote_servers", {})

        # Jupyter:
        jupyter: Jupyter = Jupyter.from_dict(args_dict=remote_servers_dict.get("jupyter", {}))

        # TensorBoard:
        tensorboard: TensorBoard = TensorBoard.from_dict(
            args_dict=remote_servers_dict.get("tensorboard", {})
        )

        # Aim:
        aim: Aim = Aim.from_dict(args_dict=remote_servers_dict.get("aim", {}))

        self.remote_servers = RemoteServers(
            browser_cmd=remote_servers_dict.get("browser_cmd", "firefox"),
            jupyter=jupyter,
            tensorboard=tensorboard,
            aim=aim,
        )
