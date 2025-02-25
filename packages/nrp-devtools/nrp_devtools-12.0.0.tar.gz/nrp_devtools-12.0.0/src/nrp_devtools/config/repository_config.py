import dataclasses
import typing

if typing.TYPE_CHECKING:
    pass


@dataclasses.dataclass
class RepositoryConfig:
    """Configuration of the repository"""

    repository_human_name: str
    repository_name: str
    repository_description: str

    @property
    def repository_package(self) -> str:
        return self.repository_name.replace("-", "_")
