from abc import abstractmethod
from typing import Protocol

from src.progron.api.entities.key import TrackerValue, TrackerKey


class ProgressTracker(Protocol):

    @abstractmethod
    async def track(self, value: TrackerValue) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> TrackerValue | None:
        raise NotImplementedError


class ProgressTrackerFactory(Protocol):
    @abstractmethod
    async def __call__(self, key: TrackerKey, **kwargs) -> ProgressTracker:
        raise NotImplementedError
