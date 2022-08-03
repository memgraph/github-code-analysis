from abc import ABC, abstractmethod
from typing import Dict


class QueryResponseInterface(ABC):
    @staticmethod
    @abstractmethod
    def query_response(query: Dict) -> None:
        pass
