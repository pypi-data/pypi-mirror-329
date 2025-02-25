import json
import shutil
from pathlib import Path
from typing import Any

from nrp_devtools.config.config import OARepoConfig

from ..utils import run_cmdline
from .less import register_less_components


def load_watched_paths(
    paths_json: str | Path, extra_paths: list[str] | None = None
) -> dict[str, str]:
    watched_paths: dict[str, str] = {}
    with open(paths_json) as f:
        for target, paths in json.load(f).items():
            if target.startswith("@"):
                continue
            for pth in paths:
                watched_paths[pth] = target
    for e in extra_paths or []:
        source, target = e.split("=", maxsplit=1)
        watched_paths[source] = target
    return watched_paths


def collect_assets(config: OARepoConfig, **kwargs: Any):
    invenio_instance_path = config.invenio_instance_path
    shutil.rmtree(invenio_instance_path / "assets", ignore_errors=True)
    shutil.rmtree(invenio_instance_path / "static", ignore_errors=True)
    Path(invenio_instance_path / "assets").mkdir(parents=True)
    Path(invenio_instance_path / "static").mkdir(parents=True)
    register_less_components(config, invenio_instance_path)
    run_cmdline(
        config.invenio_command,
        "oarepo",
        "assets",
        "collect",
        f"{invenio_instance_path}/watch.list.json",
        environ={
            "INVENIO_INSTANCE_PATH": str(config.invenio_instance_path),
            "FLASK_DEBUG": None,
        },
    )

    run_cmdline(
        config.invenio_command,
        "webpack",
        "clean",
        "create",
        # during create, if FLASK_DEBUG is set, invenio links directories, instead of copying
        # disabling this as it brings problems if directories overlap (the case with templates)
        environ={
            "INVENIO_INSTANCE_PATH": str(config.invenio_instance_path),
            "FLASK_DEBUG": None,
        },
    )

    # "invenio collect" does collect assets, but links them instead of copying,
    # so it can not be used here. So instead we use our own copying mechanism,
    # the same that is used in nrp develop.
    from .link_assets import copy_assets_to_webpack_build_dir

    copy_assets_to_webpack_build_dir(config)


def install_npm_packages(config: OARepoConfig, **kwargs: Any):
    run_cmdline(
        config.invenio_command,
        "webpack",
        "install",
        environ={"INVENIO_INSTANCE_PATH": str(config.invenio_instance_path)},
    )
