"""
CLI utilities for the cluster commands.
"""

import click

from ...config import Config


argument_oar_job_id: click.argument = click.argument(
    "oar-job-id",
    type=int,
    nargs=1,
)

argument_oar_job_id_list: click.argument = click.argument(
    "oar-job-ids",
    type=int,
    nargs=-1,
)
