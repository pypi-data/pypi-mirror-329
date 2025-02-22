from abc import abstractmethod
from collections.abc import Awaitable, Callable, Iterable, Iterator, Mapping
from datetime import datetime, timedelta
from typing import Any, Union

# Define generic type variables for better type hinting
RedisAbsExpiryType = int | datetime
RedisExpiryType = int | timedelta
RedisIntegerResponseType = Awaitable[int] | int
RedisKeyType = bytes | str
RedisListResponseType = Awaitable[list] | list
RedisPatternType = bytes | str
RedisResponseType = Awaitable[Any] | Any
RedisSetType = int | bytes | str | float


class RedisPort:
    @abstractmethod
    def ping(self) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def pttl(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def incrby(self, name: RedisKeyType, amount: int = 1) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def set(
        self,
        name: RedisKeyType,
        value: RedisSetType,
        ex: RedisExpiryType | None = None,
        px: RedisExpiryType | None = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False,
        get: bool = False,
        exat: RedisAbsExpiryType | None = None,
        pxat: RedisAbsExpiryType | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def mget(
        self,
        keys: RedisKeyType | Iterable[RedisKeyType],
        *args: bytes | str,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def mset(self, mapping: Mapping[RedisKeyType, bytes | str | float]) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def keys(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def getset(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def getdel(self, key: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def exists(self, *names: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *names: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def append(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def ttl(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def type(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def llen(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def lpop(self, name: str, count: int | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def lpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def lrange(self, name: str, start: int, end: int) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    def lrem(self, name: str, count: int, value: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def lset(self, name: str, index: int, value: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rpop(self, name: str, count: int | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def rpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def scan(
        self,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def scan_iter(
        self,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    def sscan(
        self,
        name: RedisKeyType,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def sscan_iter(
        self,
        name: RedisKeyType,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    def sadd(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def scard(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def sismember(self, name: str, value: str) -> Awaitable[bool] | bool:
        raise NotImplementedError

    @abstractmethod
    def smembers(self, name: str) -> Union[Awaitable[set], set]:
        raise NotImplementedError

    @abstractmethod
    def spop(self, name: str, count: int | None = None) -> bytes | float | int | str | list | None:
        raise NotImplementedError

    @abstractmethod
    def srem(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def sunion(self, keys: RedisKeyType, *args: bytes | str) -> set:
        raise NotImplementedError

    @abstractmethod
    def zadd(
        self,
        name: RedisKeyType,
        mapping: Mapping[RedisKeyType, bytes | str | float],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zcard(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zcount(self, name: RedisKeyType, min: float | str, max: float | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zpopmax(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zpopmin(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        desc: bool = False,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
        byscore: bool = False,
        bylex: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zrevrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zrangebyscore(
        self,
        name: RedisKeyType,
        min: float | str,
        max: float | str,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zrank(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zrem(self, name: RedisKeyType, *values: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zscore(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def hdel(self, name: str, *keys: str | bytes) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def hexists(self, name: str, key: str) -> Awaitable[bool] | bool:
        raise NotImplementedError

    @abstractmethod
    def hget(self, name: str, key: str) -> Awaitable[str | None] | str | None:
        raise NotImplementedError

    @abstractmethod
    def hgetall(self, name: str) -> Awaitable[dict] | dict:
        raise NotImplementedError

    @abstractmethod
    def hkeys(self, name: str) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    def hlen(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def hset(
        self,
        name: str,
        key: str | bytes | None = None,
        value: str | bytes | None = None,
        mapping: dict | None = None,
        items: list | None = None,
    ) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    def hmget(self, name: str, keys: list, *args: str | bytes) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    def hvals(self, name: str) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    def publish(self, channel: RedisKeyType, message: bytes | str, **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def pubsub_channels(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def zincrby(self, name: RedisKeyType, amount: float, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    def pubsub(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_pipeline(self, transaction: Any = True, shard_hint: Any = None) -> Any:
        raise NotImplementedError


class AsyncRedisPort:
    @abstractmethod
    async def ping(self) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def pttl(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def incrby(self, name: RedisKeyType, amount: int = 1) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def set(
        self,
        name: RedisKeyType,
        value: RedisSetType,
        ex: RedisExpiryType | None = None,
        px: RedisExpiryType | None = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False,
        get: bool = False,
        exat: RedisAbsExpiryType | None = None,
        pxat: RedisAbsExpiryType | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def mget(
        self,
        keys: RedisKeyType | Iterable[RedisKeyType],
        *args: bytes | str,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def mset(self, mapping: Mapping[RedisKeyType, bytes | str | float]) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def keys(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def getset(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def getdel(self, key: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, *names: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *names: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def append(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def ttl(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def type(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def llen(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def lpop(self, name: str, count: int | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def lpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def lrange(self, name: str, start: int, end: int) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    async def lrem(self, name: str, count: int, value: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def lset(self, name: str, index: int, value: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def rpop(self, name: str, count: int | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def rpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def scan(
        self,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def scan_iter(
        self,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    async def sscan(
        self,
        name: RedisKeyType,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def sscan_iter(
        self,
        name: RedisKeyType,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    async def sadd(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def scard(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def sismember(self, name: str, value: str) -> Awaitable[bool] | bool:
        raise NotImplementedError

    @abstractmethod
    async def smembers(self, name: str) -> Union[Awaitable[set], set]:
        raise NotImplementedError

    @abstractmethod
    async def spop(self, name: str, count: int | None = None) -> bytes | float | int | str | list | None:
        raise NotImplementedError

    @abstractmethod
    async def srem(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def sunion(self, keys: RedisKeyType, *args: bytes | str) -> set:
        raise NotImplementedError

    @abstractmethod
    async def zadd(
        self,
        name: RedisKeyType,
        mapping: Mapping[RedisKeyType, bytes | str | float],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zcard(self, name: bytes | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zcount(self, name: RedisKeyType, min: float | str, max: float | str) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zpopmax(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zpopmin(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        desc: bool = False,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
        byscore: bool = False,
        bylex: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zrevrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zrangebyscore(
        self,
        name: RedisKeyType,
        min: float | str,
        max: float | str,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zrank(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zrem(self, name: RedisKeyType, *values: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zscore(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hdel(self, name: str, *keys: str | bytes) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hexists(self, name: str, key: str) -> Awaitable[bool] | bool:
        raise NotImplementedError

    @abstractmethod
    async def hget(self, name: str, key: str) -> Awaitable[str | None] | str | None:
        raise NotImplementedError

    @abstractmethod
    async def hgetall(self, name: str) -> Awaitable[dict] | dict:
        raise NotImplementedError

    @abstractmethod
    async def hkeys(self, name: str) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hlen(self, name: str) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hset(
        self,
        name: str,
        key: str | bytes | None = None,
        value: str | bytes | None = None,
        mapping: dict | None = None,
        items: list | None = None,
    ) -> RedisIntegerResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hmget(self, name: str, keys: list, *args: str | bytes) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    async def hvals(self, name: str) -> RedisListResponseType:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, channel: RedisKeyType, message: bytes | str, **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def pubsub_channels(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def zincrby(self, name: RedisKeyType, amount: float, value: bytes | str | float) -> RedisResponseType:
        raise NotImplementedError

    @abstractmethod
    async def pubsub(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_pipeline(self, transaction: Any = True, shard_hint: Any = None) -> Any:
        raise NotImplementedError
