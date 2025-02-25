import functools
from collections.abc import Callable, Generator

from cosimtlk.simulation.entities import Entity


class GenericProcess(Entity):
    def __init__(
        self,
        name: str,
        priority: int,
        func: Callable,
        *,
        scheduler: Callable,
        **kwargs,
    ):
        """A generic entity that can schedule the given function.

        Args:
            name: Name of the controller for identification purposes.
            priority: Priority of the controller in task scheduling.
            func: The function to be scheduled.
            scheduler: A scheduler function that returns a generator such as 'every' or 'cron' from utils.
        """
        super().__init__(name, priority)
        self.scheduler = scheduler
        self._func = func
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def processes(self) -> list[Callable[[], Generator]]:
        decorated = self.scheduler(self._func)
        return [functools.partial(decorated, self)]
