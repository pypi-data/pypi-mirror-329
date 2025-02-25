import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import click
import requirements
import tomli
import tomli_w
from requirements.parser import Requirement

from ..config import OARepoConfig
from .check import check_failed
from .utils import run_cmdline


def remove_virtualenv_from_env() -> dict[str, str | None]:
    current_env: dict[str, str | None] = dict(os.environ)
    virtual_env_dir = current_env.pop("VIRTUAL_ENV", None)
    if not virtual_env_dir:
        return current_env
    current_env.pop("PYTHONHOME", None)
    current_env.pop("PYTHON", None)
    path = current_env.pop("PATH", None)
    split_path = path.split(os.pathsep) if path else []
    split_path = [x for x in split_path if not x.startswith(virtual_env_dir)]
    current_env["PATH"] = os.pathsep.join(split_path)
    return current_env


def uv_environ(config: OARepoConfig) -> dict[str, str | None]:
    environ = remove_virtualenv_from_env()

    venv_path = config.venv_dir
    if venv_path.exists():
        environ["VIRTUAL_ENV"] = str(venv_path)
    return environ


def clean_previous_installation(config: OARepoConfig, **kwargs: Any):
    if config.venv_dir.exists():
        shutil.rmtree(config.venv_dir)


def create_empty_venv(config: OARepoConfig, **kwargs: Any):
    clean_previous_installation(config, **kwargs)
    run_cmdline(
        "uv",
        "venv",
        str(config.venv_dir),
        "--python=python3.12",
        "--seed",
        cwd=str(config.repository_dir),
        environ=uv_environ(config),
        no_environment=True,
        raise_exception=True,
    )
    run_uv_pip(
        config,
        "install",
        "-U",
        "setuptools",
        "pip",
        "wheel",
    )


def run_uv_pip(config: OARepoConfig, *args: str, subdir: str | None = None):
    cwd = config.repository_dir
    if subdir:
        cwd = cwd / subdir

    return run_cmdline(
        "uv",
        "pip",
        *args,
        cwd=str(cwd),
        environ=uv_environ(config),
        no_environment=True,
        raise_exception=True,
    )


def check_requirements(config: OARepoConfig, will_fix: bool = False, **kwargs: Any):
    reqs_file = config.repository_dir / "requirements.txt"
    if not reqs_file.exists():
        check_failed(f"Requirements file {reqs_file} does not exist", False)

    # if any pyproject.toml is newer than requirements.txt, we need to rebuild
    pyproject = config.repository_dir / "pyproject.toml"

    if pyproject.exists() and pyproject.stat().st_mtime > reqs_file.stat().st_mtime:
        check_failed(
            f"Requirements file {reqs_file} is out of date, {pyproject} has been modified",
            will_fix=will_fix,
        )


def build_requirements(config: OARepoConfig, **kwargs: Any):
    clean_previous_installation(config, **kwargs)
    create_empty_venv(config, **kwargs)

    temporary_project_dir = ".nrp/oarepo"
    create_oarepo_project_dir(config, temporary_project_dir)
    lock_python_repository(config, temporary_project_dir)
    oarepo_requirements = export_requirements(config, temporary_project_dir)

    lock_python_repository(config)
    all_requirements = export_requirements(config)

    oarepo_requirements = list(requirements.parse(oarepo_requirements))
    all_requirements = list(requirements.parse(all_requirements))

    # get the current version of oarepo
    oarepo_requirement = [x for x in oarepo_requirements if x.name == "oarepo"][0]

    # uv does not keep the extras in the generated requirements.txt, so adding these here for oarepo
    original_oarepo_dependency, _ = get_original_oarepo_dependency(config)
    if "[" in original_oarepo_dependency:
        oarepo_requirement.extras = (
            original_oarepo_dependency.split("[")[1].split("]")[0].split(",")
        )

    oarepo_requirement = Requirement(
        re.split("[><=]", original_oarepo_dependency)[0]
        + "=="
        + oarepo_requirement.line.split("==")[1]
    )

    # now make the difference of those two (we do not want to have oarepo dependencies in the result)
    # as oarepo will be installed to virtualenv separately (to handle system packages)
    oarepo_requirements_names = {x.name for x in oarepo_requirements}
    non_oarepo_requirements = [
        x for x in all_requirements if x.name not in oarepo_requirements_names
    ]

    # remove local packages
    non_oarepo_requirements = [
        x for x in non_oarepo_requirements if "file://" not in x.line
    ]

    # and generate final requirements
    resolved_requirements = "\n".join(
        [oarepo_requirement.line, *[x.line for x in non_oarepo_requirements]]
    )
    (config.repository_dir / "requirements.txt").write_text(resolved_requirements)


def create_oarepo_project_dir(config: OARepoConfig, output_directory: str):
    oarepo_dependency, original_pdm_file = get_original_oarepo_dependency(config)

    original_pdm_file["project"]["dependencies"] = [oarepo_dependency]

    output_path = config.repository_dir / output_directory
    output_path.mkdir(parents=True, exist_ok=True)

    (output_path / "pyproject.toml").write_text(tomli_w.dumps(original_pdm_file))


def get_original_oarepo_dependency(config: OARepoConfig):
    original_pyproject_file = tomli.loads(
        (config.repository_dir / "pyproject.toml").read_text()
    )
    dependencies = original_pyproject_file["project"]["dependencies"]
    oarepo_dependency = [
        x
        for x in dependencies
        if re.match(
            r"^\s*oarepo\s*(\[[^\]]+\])?\s*[><=]+.*", x
        )  # take only oarepo package, discard others
    ][0]
    return oarepo_dependency, original_pyproject_file


def lock_python_repository(config: OARepoConfig, subdir: str | None = None):
    pyproject_toml = Path("pyproject.toml")
    requirements_txt = Path("requirements.txt")
    if subdir:
        pyproject_toml = Path(subdir) / "pyproject.toml"
        requirements_txt = Path(subdir) / "requirements.txt"

    if requirements_txt.exists():
        requirements_txt.unlink()

    run_uv_pip(
        config,
        "compile",
        "--prerelease",
        "allow",
        str(pyproject_toml),
        "-o",
        str(requirements_txt),
    )


def export_requirements(config: OARepoConfig, subdir: str | None = None):
    if subdir:
        return (Path(subdir) / "requirements.txt").read_text()
    return (config.repository_dir / "requirements.txt").read_text()


def install_python_repository(config: OARepoConfig, **kwargs: Any):
    # convert the partial requirements to the real ones

    local_requirements = config.repository_dir / "requirements-resolved-local.txt"
    if local_requirements.exists():
        local_requirements.unlink()

    requirements_file = "requirements.txt"

    editable_requirements = config.repository_dir / ".editable-requirements.txt"
    if editable_requirements.exists():
        requirements_file = "requirements-with-editable.txt"
        merge_editable_requirements(
            config.repository_dir / "requirements.txt",
            editable_requirements,
            config.repository_dir / "requirements-with-editable.txt",
        )

    run_uv_pip(
        config,
        "compile",
        "--prerelease",
        "allow",
        requirements_file,
        "-o",
        str(local_requirements),
    )

    # install the real ones
    run_uv_pip(
        config,
        "install",
        "-r",
        str(local_requirements),
        "--config-settings",
        "editable_mode=compat",
    )
    run_uv_pip(
        config, "install", "-e", ".", "--config-settings", "editable_mode=compat"
    )

    if local_requirements.exists():
        local_requirements.unlink()

    # if editable_requirements.exists():
    #     (config.repository_dir / "requirements-with-editable.txt").unlink()


def merge_editable_requirements(
    requirements_txt: Path, editable_requirements_txt: Path, output_file: Path
):
    reqs = list(requirements.parse(requirements_txt.read_text()))
    editable_requirements = dict(
        [
            x.split("=", maxsplit=1)
            for x in editable_requirements_txt.read_text().split("\n")
            if x.strip()
        ]
    )

    for req in reqs:
        if req.name in editable_requirements:
            req.line = "-e " + editable_requirements[req.name]

    resolved_requirements = "\n".join(req.line for req in reqs)
    output_file.write_text(resolved_requirements)


def check_virtualenv(config: OARepoConfig, will_fix: bool = False, **kwargs: Any):
    if not config.venv_dir.exists():
        click.secho(
            f"Virtualenv directory {config.venv_dir} does not exist",
            fg="red",
            err=True,
        )
        sys.exit(1)

    try:
        run_cmdline(
            str(config.venv_dir / "bin" / "python"),
            "--version",
            raise_exception=True,
        )
    except:  # noqa
        check_failed(
            f"Virtualenv directory {config.venv_dir} does not contain a python installation",
            will_fix=will_fix,
        )

    try:
        run_cmdline(
            str(config.venv_dir / "bin" / "pip"),
            "list",
            raise_exception=True,
            grab_stdout=True,
        )
    except:  # noqa
        check_failed(
            f"Virtualenv directory {config.venv_dir} does not contain a pip installation",
            will_fix=will_fix,
        )


def fix_virtualenv(config: OARepoConfig, **kwargs: Any):
    create_empty_venv(config)


def check_requirements(config: OARepoConfig, will_fix: bool = False, **kwargs: Any):
    reqs_file = config.repository_dir / "requirements.txt"
    if not reqs_file.exists():
        check_failed(f"Requirements file {reqs_file} does not exist", False)

    # if any pyproject.toml is newer than requirements.txt, we need to rebuild
    pyproject = config.repository_dir / "pyproject.toml"

    if pyproject.exists() and pyproject.stat().st_mtime > reqs_file.stat().st_mtime:
        check_failed(
            f"Requirements file {reqs_file} is out of date, {pyproject} has been modified",
            will_fix=will_fix,
        )


def check_invenio_callable(config: OARepoConfig, will_fix: bool = False, **kwargs: Any):
    try:
        run_cmdline(
            str(config.venv_dir / "bin" / "invenio"),
            "oarepo",
            "version",
            raise_exception=True,
            grab_stdout=True,
        )
    except:
        check_failed(
            f"Virtualenv directory {config.venv_dir} does not contain a callable invenio installation",
            will_fix=will_fix,
        )
