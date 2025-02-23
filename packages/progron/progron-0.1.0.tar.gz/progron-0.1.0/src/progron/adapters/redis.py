from typing import Callable, Any

from adaptix import Retort
from redis.asyncio import Redis, ConnectionPool

from progron.api.entities.key import TrackerKey, TrackerValue
from progron.api.protocols.tracker import ProgressTrackerFactory, ProgressTracker
from progron.utils.json import mjson_decode, mjson_encode

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class RedisProgressTracker(ProgressTracker):
    def __init__(
            self,
            storage: Redis,
            key: TrackerKey,
            json_loads: _JsonLoads = mjson_decode,
            json_dumps: _JsonDumps = mjson_encode,
            data_ttl: int = 60,
            retort: Retort = Retort()
    ):
        self.storage = storage
        self.key = key
        self.json_dumps = json_dumps
        self.json_loads = json_loads
        self.data_ttl = data_ttl
        self.retort = retort

    async def track(self, value: TrackerValue) -> None:
        key = self.build_key()
        await self.storage.set(key, self.json_dumps(self.retort.dump(value)), ex=self.data_ttl)

    async def get(self) -> TrackerValue | None:
        value = await self.storage.get(self.build_key())
        if value:
            return self.retort.load(self.json_loads(value), TrackerValue)

    def build_key(self) -> str:
        return f"track:{self.key.user_id}:{self.key.chat_id}"


class RedisProgressTrackerFactory(ProgressTrackerFactory):
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    async def __call__(self, key: TrackerKey, **kwargs) -> RedisProgressTracker:
        return RedisProgressTracker(
            storage=Redis(connection_pool=self.pool),
            key=key,
            **kwargs
        )
