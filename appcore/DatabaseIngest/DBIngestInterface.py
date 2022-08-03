from abc import ABC, abstractmethod
from typing import Any


class DBIngestInterface(ABC):
    @abstractmethod
    def run(self, data: Any) -> None:
        pass
