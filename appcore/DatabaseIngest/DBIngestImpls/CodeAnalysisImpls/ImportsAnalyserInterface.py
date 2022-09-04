from abc import ABC, abstractmethod
from typing import Dict


class ImportsAnalyserInterface(ABC):
    @abstractmethod
    def analyse_imports(self, data: Dict) -> None:
        pass
