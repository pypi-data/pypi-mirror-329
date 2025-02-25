import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

import click
import copier
import yaml

from ..commands.build import install_python_repository
from ..commands.model.compile import (
    add_model_to_i18n,
    add_requirements_and_entrypoints,
    compile_model_to_tempdir,
    copy_compiled_model,
    install_model_compiler,
)
from ..commands.types import StepFunctions
from ..commands.utils import make_step
from ..config import OARepoConfig
from ..config.model_config import ModelConfig
from .base import command_sequence, nrp_command


@nrp_command.group(name="model")
def model_group():
    """
    Model management commands
    """


@model_group.command(name="create", help="Create a new model")
@click.argument("model_name")
@click.option("--copy-model-config", help="Use a configuration file", type=click.Path())
@command_sequence(save=True)
def create_model_command(
    *,
    config: OARepoConfig,
    model_name: str,
    copy_model_config: Path | None = None,
    **kwargs: Any,
) -> StepFunctions:
    for model in config.models:
        if model.model_name == model_name:
            click.secho(f"Model {model_name} already exists", fg="red", err=True)
            return ()

    if copy_model_config:
        # if the config file is ready, just copy and add note to oarepo.yaml
        config.models.append(
            ModelConfig(
                model_name=model_name,
                model_description="",
                model_human_name=model_name,
            )
        )
        shutil.copy(copy_model_config, config.models_dir / f"{model_name}.yaml")
        return ()

    def generate_model(config: OARepoConfig, *args: Any, **kwargs: Any):
        template_path: str = os.environ.get(
            "NRP_MODEL_TEMPLATE", "gh:oarepo/nrp-model-copier"
        )
        assert config.repository
        initial_data: dict[str, str] = {
            "languages": ",".join(config.i18n.languages),
            "model_name": model_name,
        }
        copier.run_copy(
            template_path,
            config.repository_dir,
            initial_data,
            unsafe=True,
            vcs_ref="rdm-12",
        )
        answer_file = config.repository_dir / f".copier-answers-{model_name}.yml"
        with answer_file.open("r") as f:
            data: dict[str, str] = yaml.safe_load(f)
            config.add_model(
                ModelConfig(
                    model_human_name=data["model_human_name"].strip(),
                    model_name=model_name,
                    model_description=data["model_description"].strip(),
                )
            )

    return (generate_model,)


@model_group.command(name="compile", help="Compile a model")
@click.argument("model_name")
@click.option(
    "--reinstall-builder/--keep-builder",
    is_flag=True,
    help="Reinstall the model builder",
    default=True,
)
@command_sequence()
def compile_model_command(
    *, config: OARepoConfig, model_name: str, reinstall_builder: bool, **kwargs: Any
):
    model = config.get_model(model_name)
    # create a temporary directory using tempfile
    tempdir = str(Path(tempfile.mkdtemp()).resolve())

    if reinstall_builder:
        steps = [make_step(install_model_compiler, model=model)]
    else:
        steps = []

    return (
        *steps,
        make_step(compile_model_to_tempdir, model=model, tempdir=tempdir),
        make_step(copy_compiled_model, model=model, tempdir=tempdir),
        make_step(add_requirements_and_entrypoints, model=model, tempdir=tempdir),
        install_python_repository,
        make_step(add_model_to_i18n, model=model),
    )
