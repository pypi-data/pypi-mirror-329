import logging
from collections.abc import Callable
from functools import partial
from typing import Any

from psycopg.errors import DeadlockDetected, SerializationFailure
from sqlalchemy.exc import OperationalError

from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter, SessionManagerAdapter
from archipy.models.exceptions import AbortedException, DeadlockDetectedException

_in_atomic_block = "in_sqlalchemy_atomic_block"


def sqlalchemy_atomic(function: Callable | None = None) -> Callable | partial:
    return _atomic(function) if function else partial(_atomic)


def _atomic(function: Callable) -> Callable:
    def wrapper(*args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        session_manager = SessionManagerAdapter()
        session = session_manager.get_session()
        is_nested_atomic_block = session.info.get(_in_atomic_block)
        if not is_nested_atomic_block:
            session.info[_in_atomic_block] = True
        try:
            if session.in_transaction():
                result = function(*args, **kwargs)
                if not is_nested_atomic_block:
                    session.commit()
                return result
            else:
                with session.begin():
                    result = function(*args, **kwargs)
                    return result
        except (SerializationFailure, DeadlockDetected) as exception:
            session.rollback()
            raise AbortedException() from exception
        except OperationalError as exception:
            if hasattr(exception, "orig") and isinstance(exception.orig, SerializationFailure):
                session.rollback()
                raise DeadlockDetectedException() from exception
            else:
                raise exception
        except Exception as exception:
            logging.debug(f"Exception occurred in atomic block, rollback will be initiated, ex:{exception}")
            session.rollback()
            raise exception
        finally:
            if not session.in_transaction():
                session.close()
                session_manager.remove_session()

    return wrapper


def async_sqlalchemy_atomic(function: Callable | None = None) -> Callable | partial:
    return _async_atomic(function) if function else partial(_async_atomic)


def _async_atomic(function: Callable) -> Callable:
    async def async_wrapper(*args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        session_manager = AsyncSessionManagerAdapter()
        session = session_manager.get_session()
        is_nested_atomic_block = session.info.get(_in_atomic_block)
        if not is_nested_atomic_block:
            session.info[_in_atomic_block] = True
        try:
            if session.in_transaction():
                result = await function(*args, **kwargs)
                if not is_nested_atomic_block:
                    await session.commit()
                return result
            else:
                async with session.begin():
                    result = await function(*args, **kwargs)
                    return result
        except (SerializationFailure, DeadlockDetected) as exception:
            await session.rollback()
            raise AbortedException() from exception
        except OperationalError as exception:
            if hasattr(exception, "orig") and isinstance(exception.orig, SerializationFailure):
                await session.rollback()
                raise DeadlockDetectedException() from exception
            else:
                raise exception
        except Exception as exception:
            logging.debug(f"Exception occurred in atomic block, rollback will be initiated, ex:{exception}")
            await session.rollback()
            raise exception
        finally:
            if not session.in_transaction():
                await session.close()
                await session_manager.remove_session()

    return async_wrapper
