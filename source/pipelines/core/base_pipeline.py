import logging
from abc import ABC, abstractmethod
from typing import Tuple, Dict
from source.tasks.base_task import Task
from source.utils.timing import timing


logger = logging.getLogger(__name__)


class Pipeline(ABC):
    name: str = None
    _tasks: Tuple[Task, bool] = ()

    def __init__(self, config: Dict):
        self.config = config
        self.tasks = (task(self.config) for task in self._tasks)
        self._parameters = {}

    @timing
    def _run_task(self, task: Task):
        logger.info(f"[START] Task: `{task.name}`")
        output = task.run()
        logger.info(f"[END] Task: `{task.name}`")
        return output

    @timing
    def run(self):
        for task, is_active in self._tasks:
            if not is_active:
                continue

            task = task(**self._parameters)
            output = self._run_task(task)

            if output:
                self._parameters.update(**output)
        return output

    @property
    def parameters(self):
        return self._parameters

    @abstractmethod
    def get_tasks(self, config):
        raise NotImplementedError()
