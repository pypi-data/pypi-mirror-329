from pathlib import Path

from nrp_devtools.commands.pyproject import PyProject
from nrp_devtools.commands.utils import capitalize_name, run_cookiecutter
from nrp_devtools.config import OARepoConfig


def create_page_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    if (config.ui_dir / ui_config.name).exists():
        return

    capitalized_name = capitalize_name(ui_config.name)

    run_cookiecutter(
        config.ui_dir,
        template=Path(__file__).parent.parent.parent / "templates" / "ui_page",
        extra_context={
            "name": ui_config.name,
            "endpoint": ui_config.endpoint,
            "capitalized_name": capitalized_name,
            "template_name": capitalized_name + "Page",
        },
    )


def register_page_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    pyproject = PyProject(config.repository_dir / "pyproject.toml")

    pyproject.add_entry_point(
        "invenio_base.blueprints",
        f"ui_{ui_config.name}",
        f"ui.{ui_config.name}:create_blueprint",
    )

    pyproject.save()
