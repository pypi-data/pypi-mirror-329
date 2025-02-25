from functools import partial
from typing import Any

import click

from ..commands.build import (
    build_requirements,
    check_requirements,
    clean_previous_installation,
    create_empty_venv,
    install_python_repository,
)
from ..commands.invenio import install_invenio_cfg
from ..commands.types import StepFunctions
from ..commands.ui import build_production_ui, collect_assets, install_npm_packages
from ..commands.utils import make_step, no_args, run_fixup
from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="build")
@command_sequence()
def build_command(*, config: OARepoConfig, **kwargs: Any) -> StepFunctions:
    """Builds the repository"""
    return build_command_internal(config=config, **kwargs)


def build_command_internal(*, config: OARepoConfig, **kwargs: Any) -> StepFunctions:
    return (
        no_args(
            partial(click.secho, "Building repository for production", fg="yellow"),
            name="display_message",
        ),
        make_step(
            clean_previous_installation,
            name="clean_previous_installation",
        ),
        make_step(
            create_empty_venv,
            name="create_empty_venv",
        ),
        run_fixup(
            check_requirements,
            build_requirements,
            fix=True,
            name="check_and_build_requirements",
        ),
        make_step(
            install_python_repository,
            name="install_python_repository",
        ),
        install_invenio_cfg,
        collect_assets,
        install_npm_packages,
        build_production_ui,
        no_args(partial(click.secho, "Successfully built the repository", fg="green")),
    )
