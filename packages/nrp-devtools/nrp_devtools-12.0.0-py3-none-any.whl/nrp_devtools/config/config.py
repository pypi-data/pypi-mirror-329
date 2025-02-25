import dataclasses
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Any, List, Optional, cast

import dacite
import yaml
from yaml.representer import SafeRepresenter

from .i18n_config import I18NConfig
from .model_config import ModelConfig
from .repository_config import RepositoryConfig
from .ui_config import UIConfig

serialization_config = dacite.Config()
serialization_config.type_hooks = {  # type: ignore
    Path: lambda x: Path(x),
}


def Enum_representer(dumper: Any, data: Any):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.value)


def Set_representer(dumper: Any, data: Any):
    return dumper.represent_sequence(
        "tag:yaml.org,2002:seq", list(data), flow_style=True
    )


SafeRepresenter.add_multi_representer(Enum, Enum_representer)
SafeRepresenter.add_representer(set, Set_representer)


class UnknownSentinel:
    pass


UNKNOWN = (
    UnknownSentinel()
)  # marker for unknown default value in get_model which will emit KeyError


@dataclasses.dataclass
class OARepoConfig:
    repository_dir: Path
    repository: Optional[RepositoryConfig] = None
    models: List[ModelConfig] = dataclasses.field(default_factory=list)
    uis: List[UIConfig] = dataclasses.field(default_factory=list)
    i18n: I18NConfig = dataclasses.field(default_factory=I18NConfig)

    python = "python3"
    python_version = ">=3.12,<3.13"

    overrides = {}  # untyped so that it is not generated as a member of the dataclass

    @property
    def venv_dir(self):
        return self.repository_dir / ".venv"

    @property
    def ui_dir(self):
        assert self.repository
        return self.repository_dir / "ui"

    @property
    def shared_dir(self):
        assert self.repository
        return self.repository_dir / "common"

    @property
    def models_dir(self):
        assert self.repository
        return self.repository_dir / "models"

    @property
    def invenio_instance_path(self):
        return self.venv_dir / "var" / "instance"

    @property
    def invenio_command(self):
        return self.venv_dir / "bin" / "invenio"

    @property
    def theme_dir_name(self):
        return "semantic-ui"

    def add_model(self, model: ModelConfig):
        self.models.append(model)

    def get_model(
        self, model_name: str, default: ModelConfig | UnknownSentinel = UNKNOWN
    ) -> ModelConfig:
        for model in self.models:
            if model.model_name == model_name:
                return model
        if default is not UNKNOWN:
            return cast(ModelConfig, default)
        known_models = ", ".join(sorted([model.model_name for model in self.models]))
        raise KeyError(
            f"Model {model_name} not found. Known models are: {known_models}"
        )

    def add_ui(self, ui: UIConfig):
        self.uis.append(ui)

    def get_ui(
        self, ui_name: str, default: UIConfig | UnknownSentinel = UNKNOWN
    ) -> UIConfig:
        for ui in self.uis:
            if ui.name == ui_name:
                return ui
        if default is not UNKNOWN:
            return cast(UIConfig, default)
        known_uis = ", ".join(sorted([ui.name for ui in self.uis]))
        raise KeyError(f"UI {ui_name} not found. Known UIs are: {known_uis}")

    @property
    def config_file(self):
        return self.repository_dir / "oarepo.yaml"

    def load(self, extra_config: Path | None = None):
        if extra_config:
            config_file = extra_config
        else:
            config_file = self.config_file
            if not config_file.exists():
                return

        with open(config_file) as f:
            config_data = yaml.safe_load(f)

        loaded = dacite.from_dict(
            type(self),
            {"repository_dir": self.repository_dir, **config_data},
            serialization_config,
        )

        self.models = loaded.models
        self.uis = loaded.uis
        self.repository = loaded.repository
        self.i18n = loaded.i18n

    def save(self):
        if self.config_file.exists():
            previous_config_data = self.config_file.read_text().strip()
        else:
            previous_config_data = None

        io = StringIO()
        dict_data = dataclasses.asdict(self)
        dict_data.pop("repository_dir")
        yaml.safe_dump(dict_data, io)
        current_data = io.getvalue().strip()

        if previous_config_data != current_data:
            self.config_file.write_text(current_data)

    @classmethod
    def global_environment(cls):
        return {
            "PIP_EXTRA_INDEX_URL": "https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple",
            "UV_EXTRA_INDEX_URL": "https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple",
        }
