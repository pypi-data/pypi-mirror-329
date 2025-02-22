import abc
from collections.abc import Callable
from typing import Any

import grpc

from archipy.models.dtos import BaseDTO


def _get_factory_and_method(
    rpc_handler: grpc.RpcMethodHandler,
) -> tuple[Callable, Callable]:
    if rpc_handler.unary_unary:
        return grpc.unary_unary_rpc_method_handler, rpc_handler.unary_unary
    elif rpc_handler.unary_stream:
        return grpc.unary_stream_rpc_method_handler, rpc_handler.unary_stream
    elif rpc_handler.stream_unary:
        return grpc.stream_unary_rpc_method_handler, rpc_handler.stream_unary
    elif rpc_handler.stream_stream:
        return grpc.stream_stream_rpc_method_handler, rpc_handler.stream_stream
    else:  # pragma: no cover
        raise RuntimeError("RPC handler implementation does not exist")


class MethodName(BaseDTO):
    full_name: str
    package: str
    service: str
    method: str


def parse_method_name(method_name: str) -> MethodName:
    method_full_name = method_name.replace("/", "", 1)
    package_and_service, method = method_full_name.split("/")
    *maybe_package, service = package_and_service.rsplit(".", maxsplit=1)
    package = maybe_package[0] if maybe_package else ""
    return MethodName(full_name=method_full_name, package=package, service=service, method=method)


class BaseGrpcServerInterceptor(grpc.ServerInterceptor, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def intercept(self, method: Callable, request: Any, context: grpc.ServicerContext) -> Any:
        return method(request, context)

    def intercept_service(self, continuation, handler_call_details):
        next_handler = continuation(handler_call_details)
        if next_handler is None:
            return
        handler_factory, next_handler_method = _get_factory_and_method(next_handler)

        def invoke_intercept_method(request, context):
            context.method_name_model = parse_method_name(handler_call_details.method)
            return self.intercept(next_handler_method, request, context)

        return handler_factory(
            invoke_intercept_method,
            request_deserializer=next_handler.request_deserializer,
            response_serializer=next_handler.response_serializer,
        )
