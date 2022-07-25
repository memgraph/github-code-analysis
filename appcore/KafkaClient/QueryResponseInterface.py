from abc import ABC, abstractmethod


class QueryResponseInterface(ABC):
    @staticmethod
    @abstractmethod
    def query_response(query: dict) -> None:
        pass
