import time
from collections.abc import Callable
from typing import Any, ClassVar

import grpc

from archipy.configs.base_config import BaseConfig
from archipy.helpers.interceptors.grpc.base.base_grpc_server_interceptor import BaseGrpcServerInterceptor
from archipy.helpers.utils.base_utils import BaseUtils


class GrpcServerMetricInterceptor(BaseGrpcServerInterceptor):
    from prometheus_client import Histogram

    # TODO: remove unnecessary buckets
    ZERO_TO_ONE_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 1000 for i in range(0, 1000, 5)]
    ONE_TO_FIVE_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 100 for i in range(100, 500, 20)]
    FIVE_TO_THIRTY_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 100 for i in range(500, 3000, 50)]
    TOTAL_BUCKETS = (
        ZERO_TO_ONE_SECONDS_BUCKETS + ONE_TO_FIVE_SECONDS_BUCKETS + FIVE_TO_THIRTY_SECONDS_BUCKETS + [float("inf")]
    )

    RESPONSE_TIME_SECONDS = Histogram(
        "response_time_seconds",
        "Time spent processing request",
        labelnames=("package", "service", "method", "status_code"),
        buckets=TOTAL_BUCKETS,
    )

    def intercept(self, method: Callable, request: Any, context: grpc.ServicerContext):
        try:
            if not BaseConfig.global_config().PROMETHEUS.IS_ENABLED:
                return method(request, context)

            method_name_model = context.method_name_model
            start_time = time.time()
            result = method(request, context)
            self.RESPONSE_TIME_SECONDS.labels(
                package=method_name_model.package,
                service=method_name_model.service,
                method=method_name_model.method,
                status_code=context.code().name if context.code() else "OK",
            ).observe(time.time() - start_time)
            return result

        except Exception as exception:
            BaseUtils.capture_exception(exception)
