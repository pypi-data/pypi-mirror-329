from math import ceil

from fastapi import HTTPException, Request, Response
from pydantic import StrictInt
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from archipy.adapters.redis import AsyncRedisAdapter


class FastAPIRestRateLimitHandler:
    def __init__(
        self,
        calls_count: StrictInt = 1,
        milliseconds: StrictInt = 0,
        seconds: StrictInt = 0,
        minutes: StrictInt = 0,
        hours: StrictInt = 0,
        days: StrictInt = 0,
    ):
        self.calls_count = calls_count
        # Calculate total time in milliseconds directly for better readability
        self.milliseconds = (
            milliseconds + 1000 * seconds + 60 * 1000 * minutes + 60 * 60 * 1000 * hours + 24 * 60 * 60 * 1000 * days
        )
        self.redis_client = AsyncRedisAdapter()

    async def _check(self, key: str) -> int:
        # Use await for getting value from Redis as it's asynchronous
        current_request = await self.redis_client.get(key)
        if current_request is None:
            await self.redis_client.set(key, 1, px=self.milliseconds)
            return 0

        current_request = int(current_request)
        if current_request < self.calls_count:
            await self.redis_client.incrby(key)
            return 0

        ttl = await self.redis_client.pttl(key)
        if ttl == -1:
            await self.redis_client.delete(key)
        return ttl

    async def __call__(self, request: Request, response: Response):
        rate_key = await self._get_identifier(request)
        key = f"RateLimitHandler:{rate_key}:{request.scope['path']}:{request.method}"
        pexpire = await self._check(key)  # Awaiting the function since it is an async call
        if pexpire != 0:
            await self._create_callback(pexpire)

    @staticmethod
    async def _get_identifier(request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        ip = forwarded.split(",")[0] if forwarded else request.client.host
        return f"{ip}:{request.scope['path']}"

    @staticmethod
    async def _create_callback(pexpire: int):
        expire = ceil(pexpire / 1000)
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Too Many Requests",
            headers={"Retry-After": str(expire)},
        )
