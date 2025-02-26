"""
Command line interface for remi.
"""

import sys
from os.path import isdir
import click

from .user_interaction import print_error
from .cli_utils import OrderedGroup

from . import setup_commands, file_transfer, remote_compute, remote_servers


@click.group(cls=OrderedGroup)
@click.pass_context
def remi(ctx) -> None:
    """
    RemI: Remote Inria.

    Documentation:  https://remote-inria.gitlabpages.inria.fr/
    Source code:    https://gitlab.inria.fr/remote-inria/remi
    """
    if ctx.invoked_subcommand != "init":
        if not isdir(".remi/"):
            print_error(
                "RemI directory (`.remi/`) was not found ! Exiting."
                "\nYou might want to `cd` to your project or to run"
                " `remi init` if you have not done it yet."
            )
            sys.exit(1)


# Setup
remi.add_command(setup_commands.init)
remi.add_command(setup_commands.setup)
remi.add_command(setup_commands.update)

# File transfer
remi.add_command(file_transfer.clean)
remi.add_command(file_transfer.pull)
remi.add_command(file_transfer.push)

# Remote desktop
remi.add_command(remote_compute.desktop.desktop)

# Cluster
remi.add_command(remote_compute.singularity.build_container)
remi.add_command(remote_compute.clusters.inria_cluster.cluster)

# GriCAD
remi.add_command(remote_compute.clusters.gricad.gricad)

# SSH tunnel
remi.add_command(remote_servers.remote_server.ssh_bridge)

# Jupyter notebook
remi.add_command(remote_servers.jupyter.jupyter)

# TensorBoard
remi.add_command(remote_servers.tensorboard.tensorboard)

# Aim
remi.add_command(remote_servers.aim.aim)
