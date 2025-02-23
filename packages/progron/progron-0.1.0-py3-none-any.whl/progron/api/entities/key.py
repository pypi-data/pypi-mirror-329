from dataclasses import dataclass

from src.progron.api.entities.status import TaskStatus


@dataclass(frozen=True)
class TrackerKey:
    user_id: int
    chat_id: int


@dataclass
class TrackerValue:
    progress: int
    status: TaskStatus
