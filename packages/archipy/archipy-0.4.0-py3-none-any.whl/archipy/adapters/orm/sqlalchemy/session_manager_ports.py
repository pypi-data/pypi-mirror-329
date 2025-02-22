from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class SessionManagerPort:
    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError

    @abstractmethod
    def remove_session(self) -> None:
        raise NotImplementedError


class AsyncSessionManagerPort:
    @abstractmethod
    def get_session(self) -> AsyncSession:
        raise NotImplementedError

    @abstractmethod
    async def remove_session(self) -> None:
        raise NotImplementedError
