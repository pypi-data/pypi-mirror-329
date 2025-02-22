import abc
from collections.abc import Callable, Iterator, Sequence
from typing import Any, NamedTuple

import grpc


class _ClientCallDetailsFields(NamedTuple):
    method: str
    timeout: float | None
    metadata: Sequence[tuple[str, str | bytes]] | None
    credentials: grpc.CallCredentials | None
    wait_for_ready: bool | None
    compression: grpc.Compression | None


class ClientCallDetails(_ClientCallDetailsFields, grpc.ClientCallDetails):
    """Describes an RPC to be invoked.
    See https://grpc.github.io/grpc/python/grpc.html#grpc.ClientCallDetails
    """


class ClientInterceptorReturnType(grpc.Call, grpc.Future):
    """Return type for the ClientInterceptor.intercept method."""


def _swap_args(fn: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
    def new_fn(x, y):
        return fn(y, x)

    return new_fn


class BaseGrpcClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> ClientInterceptorReturnType:
        return method(request_or_iterator, call_details)

    def intercept_unary_unary(self, continuation: Callable, call_details: grpc.ClientCallDetails, request: Any):
        return self.intercept(_swap_args(continuation), request, call_details)

    def intercept_unary_stream(self, continuation: Callable, call_details: grpc.ClientCallDetails, request: Any):
        return self.intercept(_swap_args(continuation), request, call_details)

    def intercept_stream_unary(
        self,
        continuation: Callable,
        call_details: grpc.ClientCallDetails,
        request_iterator: Iterator[Any],
    ):
        return self.intercept(_swap_args(continuation), request_iterator, call_details)

    def intercept_stream_stream(
        self,
        continuation: Callable,
        call_details: grpc.ClientCallDetails,
        request_iterator: Iterator[Any],
    ):
        return self.intercept(_swap_args(continuation), request_iterator, call_details)


class _AsyncClientCallDetailsFields(NamedTuple):
    method: str
    timeout: float | None
    metadata: Sequence[tuple[str, str | bytes]] | None
    credentials: grpc.CallCredentials | None
    wait_for_ready: bool | None


class AsyncClientCallDetails(_AsyncClientCallDetailsFields, grpc.aio.ClientCallDetails):
    """Describes an RPC to be invoked.
    See https://grpc.github.io/grpc/python/grpc.html#grpc.ClientCallDetails
    """


class AsyncClientInterceptorReturnType(grpc.aio.Call, grpc.Future):
    """Return type for the ClientInterceptor.intercept method."""


class BaseAsyncGrpcClientInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
    grpc.aio.StreamUnaryClientInterceptor,
    grpc.aio.StreamStreamClientInterceptor,
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.aio.ClientCallDetails,
    ) -> AsyncClientInterceptorReturnType:
        return await method(request_or_iterator, call_details)

    async def intercept_unary_unary(
        self,
        continuation: Callable,
        call_details: grpc.aio.ClientCallDetails,
        request: Any,
    ):
        return await self.intercept(_swap_args(continuation), request, call_details)

    async def intercept_unary_stream(
        self,
        continuation: Callable,
        call_details: grpc.aio.ClientCallDetails,
        request: Any,
    ):
        return await self.intercept(_swap_args(continuation), request, call_details)

    async def intercept_stream_unary(
        self,
        continuation: Callable,
        call_details: grpc.aio.ClientCallDetails,
        request_iterator: Iterator[Any],
    ):
        return await self.intercept(_swap_args(continuation), request_iterator, call_details)

    async def intercept_stream_stream(
        self,
        continuation: Callable,
        call_details: grpc.aio.ClientCallDetails,
        request_iterator: Iterator[Any],
    ):
        return await self.intercept(_swap_args(continuation), request_iterator, call_details)
