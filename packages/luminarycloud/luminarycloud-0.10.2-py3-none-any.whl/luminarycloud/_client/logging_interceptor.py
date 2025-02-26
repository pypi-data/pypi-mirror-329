# Copyright 2023 Luminary Cloud, Inc. All Rights Reserved.
import logging
from collections.abc import Callable
from typing import Any

import grpc
from .. import __version__
from grpc import (
    ClientCallDetails,
    UnaryUnaryClientInterceptor,
)
from grpc._interceptor import _ClientCallDetails

from .._version import __version__

logger = logging.getLogger(__name__)


class LoggingInterceptor(UnaryUnaryClientInterceptor):
    """
    A client interceptor that logs gRPC method calls and appends the SDK version
    to the request metadata.
    """

    def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, Any], grpc.Call],
        client_call_details: ClientCallDetails,
        request: Any,
    ) -> grpc.Call:

        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        # will look like: x-client-version: python-sdk-v0.1.0
        metadata.append(("x-client-version", f"python-sdk-v{__version__}"))

        client_call_details = _ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
            client_call_details.compression,
        )

        logger.debug(
            f"[SDK v{__version__}] Sending unary-unary gRPC request: {client_call_details.method}."
        )
        try:
            call = continuation(client_call_details, request)
            call.result()
        except grpc.RpcError:
            logger.debug("Error occurred during gRPC request", exc_info=True)
            raise
        return call
