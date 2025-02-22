from collections.abc import Callable
from typing import Any

import elasticapm
import grpc

from archipy.configs.base_config import BaseConfig
from archipy.helpers.interceptors.grpc.base.base_grpc_server_interceptor import BaseGrpcServerInterceptor
from archipy.helpers.utils.base_utils import BaseUtils


class GrpcServerTraceInterceptor(BaseGrpcServerInterceptor):
    def intercept(self, method: Callable, request: Any, context: grpc.ServicerContext):
        try:
            if BaseConfig.global_config().ELASTIC_APM.ENABLED:
                method_name_model = context.method_name_model
                client = elasticapm.get_client()
                metadata_dict = dict(context.invocation_metadata())
                if parent := elasticapm.trace_parent_from_headers(metadata_dict):
                    client.begin_transaction(transaction_type="request", trace_parent=parent)
                    try:
                        result = method(request, context)
                        client.end_transaction(name=method_name_model.full_name, result="success")
                        return result
                    except Exception as e:
                        client.end_transaction(name=method_name_model.full_name, result="failure")
                        raise e
                else:
                    client.begin_transaction(transaction_type="request")
                    try:
                        result = method(request, context)
                        client.end_transaction(name=method_name_model.full_name, result="success")
                        return result
                    except Exception as e:
                        client.end_transaction(name=method_name_model.full_name, result="failure")
                        raise e
            else:
                return method(request, context)
        except Exception as exception:
            BaseUtils.capture_exception(exception)
