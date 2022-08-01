from abc import ABC, abstractmethod
from typing import Any


class DBIngestInterface(ABC):
    @abstractmethod
    def create_db_objects(self, data: Any) -> None:
        pass
