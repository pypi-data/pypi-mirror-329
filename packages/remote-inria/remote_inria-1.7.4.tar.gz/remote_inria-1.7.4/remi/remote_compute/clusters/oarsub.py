"""
Utility functions for interacting with oarsub.
"""

from datetime import datetime
from os.path import join

from ...config import Config, Oarsub
from ...user_interaction import to_bold, print_info


def print_cluster_request_prop(
    property_name: str,
    value: str,
) -> None:
    num_dots: int = 25 - len(property_name)
    to_print: str = "\t" + to_bold(property_name + ":") + "." * num_dots + str(value)
    print_info(to_print)


def _print_cluster_request(
    oarsub_config: Oarsub,
    host_id: str,
    job_name: str,
) -> None:
    print_info(to_bold("Cluster request:"))
    print_cluster_request_prop(
        property_name="Job name",
        value=job_name,
    )
    print_cluster_request_prop(
        property_name="Number of hosts",
        value=oarsub_config.num_hosts,
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
    print_cluster_request_prop(
        property_name="Walltime",
        value=oarsub_config.walltime,
    )
    print_cluster_request_prop(
        property_name="Cluster name",
        value=oarsub_config.cluster_name,
    )
    if host_id != "":
        print_cluster_request_prop(
            property_name="Host ID",
            value=host_id,
        )
    if oarsub_config.custom_property_query:
        print_cluster_request_prop(
            property_name="Custom property query",
            value=oarsub_config.custom_property_query,
        )
    print_cluster_request_prop(
        property_name="Besteffort",
        value=oarsub_config.besteffort,
    )
    print_cluster_request_prop(
        property_name="Idempotent",
        value=oarsub_config.idempotent,
    )


def get_oarsub_cmd_prefix(
    host_id: str,
    job_name: str,
) -> list[str]:
    # Get the oarsub config
    oarsub_config: Oarsub = Config().oarsub

    # Oarsub command
    oarsub_cmd: list[str] = ["oarsub"]

    # Name the job
    oarsub_cmd += ["--name", job_name]

    # Resource list
    resource_list: str = f"/host={oarsub_config.num_hosts}"
    if oarsub_config.num_cpu_cores > 0:
        resource_list += f"/core={oarsub_config.num_cpu_cores}"

    if oarsub_config.num_gpus > 0:
        resource_list += f"/gpudevice={oarsub_config.num_gpus}"

    if oarsub_config.walltime != "":
        resource_list += f",walltime={oarsub_config.walltime}"

    oarsub_cmd += ["-l", resource_list]

    # Check that the cluster name is valid
    assert oarsub_config.cluster_name in [
        "beagle",
        "cp",
        "kinovis",
        "mistis",
        "nanod",
        "perception",
        "thoth",
    ], f"Unknown cluster name: {oarsub_config.cluster_name}"

    # Property list
    property_list: str
    # Using directly the provided property query, ignoring other options.
    if oarsub_config.custom_property_query:
        property_list = '"' + oarsub_config.custom_property_query + '"'

    # Using the other config settings.
    else:
        property_list = f"\"cluster='{oarsub_config.cluster_name}'"

        if host_id:
            assert 4 <= len(host_id) <= 5
            assert host_id.startswith("gpu") or host_id.startswith("node")
            cluster_host_name: str = f"{host_id}-{oarsub_config.cluster_name}.inrialpes.fr"

            property_list += f" AND host='{cluster_host_name}'"

        property_list += '"'
    oarsub_cmd += ["-p", property_list]

    if oarsub_config.besteffort:
        oarsub_cmd += ["-t", "besteffort"]

    if oarsub_config.idempotent:
        oarsub_cmd += ["-t", "idempotent"]

    _print_cluster_request(
        oarsub_config=oarsub_config,
        job_name=job_name,
        host_id=host_id,
    )

    return oarsub_cmd


def add_standard_output_params(
    oarsub_log_path: str,
    base_name: str = "",
) -> list[str]:
    time_stamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not base_name:
        base_name = f"OAR.{time_stamp}.%jobid%.%jobname%"

    return [
        "--stdout",
        join(oarsub_log_path, f"{base_name}.stdout"),
        "--stderr",
        join(oarsub_log_path, f"{base_name}.stderr"),
    ]
