from collections.abc import Callable
from typing import Any

import elasticapm
import grpc
from elasticapm.conf.constants import TRACEPARENT_HEADER_NAME

from archipy.configs.base_config import BaseConfig
from archipy.helpers.interceptors.grpc.base.base_grpc_client_interceptor import (
    AsyncClientCallDetails,
    BaseAsyncGrpcClientInterceptor,
    BaseGrpcClientInterceptor,
    ClientCallDetails,
)


class GrpcClientTraceInterceptor(BaseGrpcClientInterceptor):
    def intercept(self, method: Callable, request_or_iterator: Any, call_details: grpc.ClientCallDetails):
        if not BaseConfig.global_config().ELASTIC_APM.ENABLED:
            return method(request_or_iterator, call_details)
        if not (trace_parent_id := elasticapm.get_trace_parent_header()):
            return method(request_or_iterator, call_details)
        new_details = ClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=[(TRACEPARENT_HEADER_NAME, f"{trace_parent_id}")],
            credentials=call_details.credentials,
            wait_for_ready=call_details.wait_for_ready,
            compression=call_details.compression,
        )
        return method(request_or_iterator, new_details)


class AsyncGrpcClientTraceInterceptor(BaseAsyncGrpcClientInterceptor):
    async def intercept(self, method: Callable, request_or_iterator: Any, call_details: grpc.aio.ClientCallDetails):
        if not BaseConfig.global_config().ELASTIC_APM.ENABLED:
            return await method(request_or_iterator, call_details)
        if not (trace_parent_id := elasticapm.get_trace_parent_header()):
            return await method(request_or_iterator, call_details)
        new_details = AsyncClientCallDetails(
            method=call_details.method,
            timeout=call_details.timeout,
            metadata=[(TRACEPARENT_HEADER_NAME, f"{trace_parent_id}")],
            credentials=call_details.credentials,
            wait_for_ready=call_details.wait_for_ready,
        )
        return await method(request_or_iterator, new_details)
