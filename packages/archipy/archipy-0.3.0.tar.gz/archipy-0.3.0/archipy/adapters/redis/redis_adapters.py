from collections.abc import Awaitable, Callable, Iterable, Iterator, Mapping
from typing import Any, Union, override

from redis.asyncio.client import Pipeline as AsyncPipeline, PubSub as AsyncPubSub, Redis as AsyncRedis
from redis.client import Pipeline, PubSub, Redis

from archipy.adapters.redis.redis_ports import (
    AsyncRedisPort,
    RedisAbsExpiryType,
    RedisExpiryType,
    RedisIntegerResponseType,
    RedisKeyType,
    RedisListResponseType,
    RedisPatternType,
    RedisPort,
    RedisResponseType,
    RedisSetType,
)
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import RedisConfig


class RedisAdapter(RedisPort):
    def __init__(self, redis_config: RedisConfig | None = None) -> None:
        configs: RedisConfig = BaseConfig.global_config().REDIS if redis_config is None else redis_config
        self._set_clients(configs)

    def _set_clients(self, configs: RedisConfig) -> None:
        if redis_master_host := configs.MASTER_HOST:
            self.client: Redis = self._get_client(redis_master_host, configs)
        if redis_slave_host := configs.SLAVE_HOST:
            self.read_only_client: Redis = self._get_client(redis_slave_host, configs)
        else:
            self.read_only_client = self.client

    @staticmethod
    def _get_client(host: str, configs: RedisConfig) -> Redis:
        return Redis(
            host=host,
            port=configs.PORT,
            db=configs.DATABASE,
            password=configs.PASSWORD,
            decode_responses=configs.DECODE_RESPONSES,
            health_check_interval=configs.HEALTH_CHECK_INTERVAL,
        )

    @override
    def pttl(self, name: bytes | str) -> RedisResponseType:
        return self.read_only_client.pttl(name)

    @override
    def incrby(self, name: RedisKeyType, amount: int = 1) -> RedisResponseType:
        return self.client.incrby(name, amount)

    @override
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
        return self.client.set(name, value, ex, px, nx, xx, keepttl, get, exat, pxat)

    @override
    def get(self, key: str) -> RedisResponseType:
        return self.read_only_client.get(key)

    @override
    def mget(
        self,
        keys: RedisKeyType | Iterable[RedisKeyType],
        *args: bytes | str,
    ) -> RedisResponseType:
        return self.read_only_client.mget(keys, *args)

    @override
    def mset(self, mapping: Mapping[RedisKeyType, bytes | str | float]) -> RedisResponseType:
        return self.client.mset(mapping)

    @override
    def keys(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        return self.read_only_client.keys(pattern, **kwargs)

    @override
    def getset(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return self.client.getset(key, value)

    @override
    def getdel(self, key: bytes | str) -> RedisResponseType:
        return self.client.getdel(key)

    @override
    def exists(self, *names: bytes | str) -> RedisResponseType:
        return self.read_only_client.exists(*names)

    @override
    def delete(self, *names: bytes | str) -> RedisResponseType:
        return self.client.delete(*names)

    @override
    def append(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return self.client.append(key, value)

    @override
    def ttl(self, name: bytes | str) -> RedisResponseType:
        return self.read_only_client.ttl(name)

    @override
    def type(self, name: bytes | str) -> RedisResponseType:
        return self.read_only_client.type(name)

    @override
    def llen(self, name: str) -> RedisIntegerResponseType:
        return self.read_only_client.llen(name)

    @override
    def lpop(self, name: str, count: int | None = None) -> Any:
        return self.client.lpop(name, count)

    @override
    def lpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return self.client.lpush(name, *values)

    @override
    def lrange(self, name: str, start: int, end: int) -> RedisListResponseType:
        return self.read_only_client.lrange(name, start, end)

    @override
    def lrem(self, name: str, count: int, value: str) -> RedisIntegerResponseType:
        return self.client.lrem(name, count, value)

    @override
    def lset(self, name: str, index: int, value: str) -> bool:
        return self.client.lset(name, index, value)

    @override
    def rpop(self, name: str, count: int | None = None) -> Any:
        return self.client.rpop(name, count)

    @override
    def rpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return self.client.rpush(name, *values)

    @override
    def scan(
        self,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> RedisResponseType:
        return self.read_only_client.scan(cursor, match, count, _type, **kwargs)

    @override
    def scan_iter(
        self,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> Iterator:
        return self.read_only_client.scan_iter(match, count, _type, **kwargs)

    @override
    def sscan(
        self,
        name: RedisKeyType,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> RedisResponseType:
        return self.read_only_client.sscan(name, cursor, match, count)

    @override
    def sscan_iter(
        self,
        name: RedisKeyType,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> Iterator:
        return self.read_only_client.sscan_iter(name, match, count)

    @override
    def sadd(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return self.client.sadd(name, *values)

    @override
    def scard(self, name: str) -> RedisIntegerResponseType:
        return self.client.scard(name)

    @override
    def sismember(self, name: str, value: str) -> Awaitable[bool] | bool:
        return self.read_only_client.sismember(name, value)

    @override
    def smembers(self, name: str) -> Union[Awaitable[set], set]:
        return self.read_only_client.smembers(name)

    @override
    def spop(self, name: str, count: int | None = None) -> bytes | float | int | str | list | None:
        return self.client.spop(name, count)

    @override
    def srem(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return self.client.srem(name, *values)

    @override
    def sunion(self, keys: RedisKeyType, *args: bytes | str) -> set:
        return self.client.sunion(keys, *args)

    @override
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
        return self.client.zadd(name, mapping, nx, xx, ch, incr, gt, lt)

    @override
    def zcard(self, name: bytes | str) -> RedisResponseType:
        return self.client.zcard(name)

    @override
    def zcount(self, name: RedisKeyType, min: float | str, max: float | str) -> RedisResponseType:
        return self.client.zcount(name, min, max)

    @override
    def zpopmax(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        return self.client.zpopmax(name, count)

    @override
    def zpopmin(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        return self.client.zpopmin(name, count)

    @override
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
        return self.read_only_client.zrange(
            name,
            start,
            end,
            desc,
            withscores,
            score_cast_func,
            byscore,
            bylex,
            offset,
            num,
        )

    @override
    def zrevrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        return self.read_only_client.zrevrange(name, start, end, withscores, score_cast_func)

    @override
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
        return self.read_only_client.zrangebyscore(name, min, max, start, num, withscores, score_cast_func)

    @override
    def zrank(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return self.read_only_client.zrank(name, value)

    @override
    def zrem(self, name: RedisKeyType, *values: bytes | str | float) -> RedisResponseType:
        return self.client.zrem(name, *values)

    @override
    def zscore(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return self.read_only_client.zscore(name, value)

    @override
    def hdel(self, name: str, *keys: str | bytes) -> RedisIntegerResponseType:
        return self.client.hdel(name, *keys)

    @override
    def hexists(self, name: str, key: str) -> Awaitable[bool] | bool:
        return self.read_only_client.hexists(name, key)

    @override
    def hget(self, name: str, key: str) -> Awaitable[str | None] | str | None:
        return self.read_only_client.hget(name, key)

    @override
    def hgetall(self, name: str) -> Awaitable[dict] | dict:
        return self.read_only_client.hgetall(name)

    @override
    def hkeys(self, name: str) -> RedisListResponseType:
        return self.read_only_client.hkeys(name)

    @override
    def hlen(self, name: str) -> RedisIntegerResponseType:
        return self.read_only_client.hlen(name)

    @override
    def hset(
        self,
        name: str,
        key: str | bytes | None = None,
        value: str | bytes | None = None,
        mapping: dict | None = None,
        items: list | None = None,
    ) -> RedisIntegerResponseType:
        return self.client.hset(name, key, value, mapping, items)

    @override
    def hmget(self, name: str, keys: list, *args: str | bytes) -> RedisListResponseType:
        return self.read_only_client.hmget(name, keys, *args)

    @override
    def hvals(self, name: str) -> RedisListResponseType:
        return self.read_only_client.hvals(name)

    @override
    def publish(self, channel: RedisKeyType, message: bytes | str, **kwargs: Any) -> RedisResponseType:
        return self.client.publish(channel, message, **kwargs)

    @override
    def pubsub_channels(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        return self.client.pubsub_channels(pattern, **kwargs)

    @override
    def zincrby(self, name: RedisKeyType, amount: float, value: bytes | str | float) -> RedisResponseType:
        return self.client.zincrby(name, amount, value)

    @override
    def pubsub(self, **kwargs: Any) -> PubSub:
        return self.client.pubsub(**kwargs)

    @override
    def get_pipeline(self, transaction: Any = True, shard_hint: Any = None) -> Pipeline:
        return self.client.pipeline(transaction, shard_hint)

    @override
    def ping(self) -> RedisResponseType:
        return self.client.ping()


class AsyncRedisAdapter(AsyncRedisPort):
    def __init__(self, redis_config: RedisConfig | None = None) -> None:
        configs: RedisConfig = BaseConfig.global_config().REDIS if redis_config is None else redis_config
        self._set_clients(configs)

    def _set_clients(self, configs: RedisConfig) -> None:
        if redis_master_host := configs.MASTER_HOST:
            self.client: AsyncRedis = self._get_client(redis_master_host, configs)
        if redis_slave_host := configs.SLAVE_HOST:
            self.read_only_client: AsyncRedis = self._get_client(redis_slave_host, configs)
        else:
            self.read_only_client = self.client

    @staticmethod
    def _get_client(host: str, configs: RedisConfig) -> AsyncRedis:
        return AsyncRedis(
            host=host,
            port=configs.PORT,
            db=configs.DATABASE,
            password=configs.PASSWORD,
            decode_responses=configs.DECODE_RESPONSES,
            health_check_interval=configs.HEALTH_CHECK_INTERVAL,
        )

    @override
    async def pttl(self, name: bytes | str) -> RedisResponseType:
        return await self.read_only_client.pttl(name)

    @override
    async def incrby(self, name: RedisKeyType, amount: int = 1) -> RedisResponseType:
        return await self.client.incrby(name, amount)

    @override
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
        return await self.client.set(name, value, ex, px, nx, xx, keepttl, get, exat, pxat)

    @override
    async def get(self, key: str) -> RedisResponseType:
        return await self.read_only_client.get(key)

    @override
    async def mget(
        self,
        keys: RedisKeyType | Iterable[RedisKeyType],
        *args: bytes | str,
    ) -> RedisResponseType:
        return await self.read_only_client.mget(keys, *args)

    @override
    async def mset(self, mapping: Mapping[RedisKeyType, bytes | str | float]) -> RedisResponseType:
        return await self.client.mset(mapping)

    @override
    async def keys(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        return await self.read_only_client.keys(pattern, **kwargs)

    @override
    async def getset(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return await self.client.getset(key, value)

    @override
    async def getdel(self, key: bytes | str) -> RedisResponseType:
        return await self.client.getdel(key)

    @override
    async def exists(self, *names: bytes | str) -> RedisResponseType:
        return await self.read_only_client.exists(*names)

    @override
    async def delete(self, *names: bytes | str) -> RedisResponseType:
        return await self.client.delete(*names)

    @override
    async def append(self, key: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return await self.client.append(key, value)

    @override
    async def ttl(self, name: bytes | str) -> RedisResponseType:
        return await self.read_only_client.ttl(name)

    @override
    async def type(self, name: bytes | str) -> RedisResponseType:
        return await self.read_only_client.type(name)

    @override
    async def llen(self, name: str) -> RedisIntegerResponseType:
        return await self.read_only_client.llen(name)

    @override
    async def lpop(self, name: str, count: int | None = None) -> Any:
        return await self.client.lpop(name, count)

    @override
    async def lpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return await self.client.lpush(name, *values)

    @override
    async def lrange(self, name: str, start: int, end: int) -> RedisListResponseType:
        return await self.read_only_client.lrange(name, start, end)

    @override
    async def lrem(self, name: str, count: int, value: str) -> RedisIntegerResponseType:
        return await self.client.lrem(name, count, value)

    async def lset(self, name: str, index: int, value: str) -> bool:
        return await self.client.lset(name, index, value)

    @override
    async def rpop(self, name: str, count: int | None = None) -> Any:
        return await self.client.rpop(name, count)

    @override
    async def rpush(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return await self.client.rpush(name, *values)

    @override
    async def scan(
        self,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> RedisResponseType:
        return await self.read_only_client.scan(cursor, match, count, _type, **kwargs)

    @override
    async def scan_iter(
        self,
        match: bytes | str | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: Any,
    ) -> Iterator:
        return await self.read_only_client.scan_iter(match, count, _type, **kwargs)

    @override
    async def sscan(
        self,
        name: RedisKeyType,
        cursor: int = 0,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> RedisResponseType:
        return await self.read_only_client.sscan(name, cursor, match, count)

    @override
    async def sscan_iter(
        self,
        name: RedisKeyType,
        match: bytes | str | None = None,
        count: int | None = None,
    ) -> Iterator:
        return await self.read_only_client.sscan_iter(name, match, count)

    @override
    async def sadd(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return await self.client.sadd(name, *values)

    @override
    async def scard(self, name: str) -> RedisIntegerResponseType:
        return await self.client.scard(name)

    @override
    async def sismember(self, name: str, value: str) -> Awaitable[bool] | bool:
        return await self.read_only_client.sismember(name, value)

    @override
    async def smembers(self, name: str) -> Union[Awaitable[set], set]:
        return await self.read_only_client.smembers(name)

    @override
    async def spop(self, name: str, count: int | None = None) -> bytes | float | int | str | list | None:
        return await self.client.spop(name, count)

    @override
    async def srem(self, name: str, *values: bytes | str | float) -> RedisIntegerResponseType:
        return await self.client.srem(name, *values)

    @override
    async def sunion(self, keys: RedisKeyType, *args: bytes | str) -> set:
        return await self.client.sunion(keys, *args)

    @override
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
        return await self.client.zadd(name, mapping, nx, xx, ch, incr, gt, lt)

    @override
    async def zcard(self, name: bytes | str) -> RedisResponseType:
        return await self.client.zcard(name)

    @override
    async def zcount(self, name: RedisKeyType, min: float | str, max: float | str) -> RedisResponseType:
        return await self.client.zcount(name, min, max)

    @override
    async def zpopmax(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        return await self.client.zpopmax(name, count)

    @override
    async def zpopmin(self, name: RedisKeyType, count: int | None = None) -> RedisResponseType:
        return await self.client.zpopmin(name, count)

    @override
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
        return await self.read_only_client.zrange(
            name,
            start,
            end,
            desc,
            withscores,
            score_cast_func,
            byscore,
            bylex,
            offset,
            num,
        )

    @override
    async def zrevrange(
        self,
        name: RedisKeyType,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: Union[type, Callable] = float,
    ) -> RedisResponseType:
        return await self.read_only_client.zrevrange(name, start, end, withscores, score_cast_func)

    @override
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
        return await self.read_only_client.zrangebyscore(name, min, max, start, num, withscores, score_cast_func)

    @override
    async def zrank(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return await self.read_only_client.zrank(name, value)

    @override
    async def zrem(self, name: RedisKeyType, *values: bytes | str | float) -> RedisResponseType:
        return await self.client.zrem(name, *values)

    @override
    async def zscore(self, name: RedisKeyType, value: bytes | str | float) -> RedisResponseType:
        return await self.read_only_client.zscore(name, value)

    @override
    async def hdel(self, name: str, *keys: str | bytes) -> RedisIntegerResponseType:
        return await self.client.hdel(name, *keys)

    @override
    async def hexists(self, name: str, key: str) -> Awaitable[bool] | bool:
        return await self.read_only_client.hexists(name, key)

    @override
    async def hget(self, name: str, key: str) -> Awaitable[str | None] | str | None:
        return await self.read_only_client.hget(name, key)

    @override
    async def hgetall(self, name: str) -> Awaitable[dict] | dict:
        return await self.read_only_client.hgetall(name)

    @override
    async def hkeys(self, name: str) -> RedisListResponseType:
        return await self.read_only_client.hkeys(name)

    @override
    async def hlen(self, name: str) -> RedisIntegerResponseType:
        return await self.read_only_client.hlen(name)

    @override
    async def hset(
        self,
        name: str,
        key: str | bytes | None = None,
        value: str | bytes | None = None,
        mapping: dict | None = None,
        items: list | None = None,
    ) -> RedisIntegerResponseType:
        return await self.client.hset(name, key, value, mapping, items)

    @override
    async def hmget(self, name: str, keys: list, *args: str | bytes) -> RedisListResponseType:
        return await self.read_only_client.hmget(name, keys, *args)

    @override
    async def hvals(self, name: str) -> RedisListResponseType:
        return await self.read_only_client.hvals(name)

    @override
    async def publish(self, channel: RedisKeyType, message: bytes | str, **kwargs: Any) -> RedisResponseType:
        return await self.client.publish(channel, message, **kwargs)

    @override
    async def pubsub_channels(self, pattern: RedisPatternType = "*", **kwargs: Any) -> RedisResponseType:
        return await self.client.pubsub_channels(pattern, **kwargs)

    @override
    async def zincrby(self, name: RedisKeyType, amount: float, value: bytes | str | float) -> RedisResponseType:
        return await self.client.zincrby(name, amount, value)

    @override
    async def pubsub(self, **kwargs: Any) -> AsyncPubSub:
        return await self.client.pubsub(**kwargs)

    @override
    async def get_pipeline(self, transaction: Any = True, shard_hint: Any = None) -> AsyncPipeline:
        return await self.client.pipeline(transaction, shard_hint)

    @override
    async def ping(self) -> RedisResponseType:
        return await self.client.ping()
