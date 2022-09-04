from abc import ABC, abstractmethod
from typing import Dict


class LanguageTypeCheckerInterface(ABC):
    @abstractmethod
    def can_analyse_file(self, data: Dict) -> bool:
        pass
