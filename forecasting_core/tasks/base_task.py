from abc import ABC, abstractmethod
from typing import Dict


class Task(ABC):
    name = None

    def __init__(self, config: Dict):
        self.config = config

    @abstractmethod
    def _load_inputs(self, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _save_results(self, **kwargs):
        pass
