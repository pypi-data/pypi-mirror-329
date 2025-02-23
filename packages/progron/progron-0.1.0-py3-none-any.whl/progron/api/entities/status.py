from enum import StrEnum


class TaskStatus(StrEnum):
    STARTED = "started"
    PROCESSING = "processing"
    FINISHED = "finished"
    CANCELLED = "cancelled"
