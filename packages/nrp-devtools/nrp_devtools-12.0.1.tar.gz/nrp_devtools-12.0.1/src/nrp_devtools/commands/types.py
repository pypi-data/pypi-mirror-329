from typing import Any, Protocol

from ..config import OARepoConfig


class StepFunction(Protocol):
    def __call__(self, config: OARepoConfig, **kwargs: Any) -> None: ...


StepFunctions = tuple[StepFunction, ...] | list[StepFunction]
