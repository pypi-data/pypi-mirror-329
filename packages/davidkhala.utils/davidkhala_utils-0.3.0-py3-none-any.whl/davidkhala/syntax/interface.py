from abc import ABC, abstractmethod
from typing import Any


class Serializable(ABC):

    @abstractmethod
    def as_dict(self) -> dict:
        ...


class Delegate:
    client: Any

    def __getattr__(self, name):
        # Delegate unknown attributes/methods to the wrapped instance
        return getattr(self.client, name)
