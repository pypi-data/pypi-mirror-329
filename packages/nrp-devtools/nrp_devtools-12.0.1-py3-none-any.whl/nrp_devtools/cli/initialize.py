import dataclasses
import os
import sys
from pathlib import Path

import click
import copier
import yaml

from ..commands.utils import run_cmdline
from ..config import OARepoConfig
from ..config.repository_config import RepositoryConfig
from ..x509 import generate_selfsigned_cert
from .base import command_sequence, nrp_command


@nrp_command.command(name="initialize")
@click.option(
    "--initial-config",
    default=None,
    help="Initial configuration file",
    type=click.Path(exists=True),
)
@click.option(
    "--no-input",
    default=None,
    help="Do not ask for input, use the initial config only",
    is_flag=True,
)
@command_sequence(
    repository_dir_as_argument=True, repository_dir_must_exist=False, save=True
)
def initialize_command(
    *,
    repository_dir: Path,
    config: OARepoConfig,
    verbose: bool,
    initial_config: Path,
    no_input: bool,
):
    """
    Initialize a new nrp project. Note: the project directory must be empty.
    """
    if repository_dir.exists() and len(list(repository_dir.iterdir())) > 0:
        click.secho(
            f"Project directory {repository_dir} must be empty", fg="red", err=True
        )
        sys.exit(1)

    def initialize_step(config: OARepoConfig):
        if initial_config:
            config.load(Path(initial_config))

        template_path = os.environ.get("NRP_APP_TEMPLATE", "gh:oarepo/nrp-app-copier")
        initial_data = (
            dataclasses.asdict(config.repository) if config.repository else {}
        )
        repository_name = repository_dir.name
        initial_data.setdefault("repository_name", repository_name)
        copier.run_copy(
            template_path, repository_dir, initial_data, unsafe=True, vcs_ref="rdm-12"
        )
        answer_file = repository_dir / ".copier-answers.yml"
        with answer_file.open("r") as f:
            data: dict[str, str] = yaml.safe_load(f)
            config.repository = RepositoryConfig(
                repository_human_name=data["repository_human_name"].strip(),
                repository_name=repository_name,
                repository_description=data["repository_description"].strip(),
            )
            config.i18n.languages = ["en"] + [
                x.strip() for x in data["languages"].strip().split(",") if x.strip()
            ]

    def generate_certificate_step(config: OARepoConfig):
        # generate the certificate
        cert, key = generate_selfsigned_cert("localhost", ["127.0.0.1"])
        (config.repository_dir / "docker" / "development.crt").write_bytes(cert)
        (config.repository_dir / "docker" / "development.key").write_bytes(key)

    def link_variables_step(config: OARepoConfig):
        # link the variables
        (config.repository_dir / "docker" / ".env").symlink_to(
            config.repository_dir / "variables"
        )

    def mark_nrp_executable_step(config: OARepoConfig):
        # mark the nrp command executable
        (config.repository_dir / "nrp").chmod(0o755)

    def set_up_i18n_step(config: OARepoConfig):
        # set up the i18n
        config.i18n.babel_source_paths = [
            "common",
            "ui",
        ]
        config.i18n.i18next_source_paths = ["ui"]

    def commit_to_git_step(config: OARepoConfig):
        run_cmdline("git", "init", cwd=str(config.repository_dir), raise_exception=True)
        run_cmdline(
            "git", "add", ".", cwd=str(config.repository_dir), raise_exception=True
        )
        run_cmdline(
            "git",
            "commit",
            "-am",
            "Initial commit",
            cwd=str(config.repository_dir),
            raise_exception=True,
        )

    def show_next_steps_step(config: OARepoConfig):
        click.secho(
            """
Your repository is now initialized. 

To test it out, start the repository in development mode
via ./nrp develop and head to https://127.0.0.1:5000/
to check that everything has been installed correctly.

Then add metadata models via ./nrp model create <model_name>,
edit the model and compile it via ./nrp model compile <model_name>.

To generate a default UI for the model, run ./nrp ui detail <model_name>.
""",
            fg="green",
        )

    return (
        initialize_step,
        generate_certificate_step,
        link_variables_step,
        mark_nrp_executable_step,
        set_up_i18n_step,
        commit_to_git_step,
        show_next_steps_step,
    )
