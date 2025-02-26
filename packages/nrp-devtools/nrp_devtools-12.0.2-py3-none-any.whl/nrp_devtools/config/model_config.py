import dataclasses

from caseconverter import kebabcase


@dataclasses.dataclass
class ModelConfig:
    model_name: str
    model_description: str
    model_human_name: str

    @property
    def api_prefix(self):
        return kebabcase(self.model_name)

    @property
    def model_config_file(self):
        return f"{self.model_name}.yaml"
