# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
"""Custom exceptions for the Luminary Cloud SDK."""

import grpc


class SDKException(Exception):
    """Base exception for all Luminary SDK exceptions."""

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"

    def _render_traceback_(self) -> list[str]:
        """Custom traceback for IPython"""
        return [self.message]


class RpcError(SDKException):
    """Raised when an RPC error occurs."""

    code: grpc.StatusCode

    def __init__(self, message: str, code: grpc.StatusCode) -> None:
        super().__init__(message)
        self.code = code


class AuthenticationError(RpcError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, grpc.StatusCode.UNAUTHENTICATED)

    def _render_traceback_(self) -> list[str]:
        return ["Authentication failed; please check your credentials and try again."]


class InvalidRequestError(RpcError):
    """Raised when the request is invalid."""

    def __init__(self, message: str = "Invalid request") -> None:
        super().__init__(message, grpc.StatusCode.INVALID_ARGUMENT)


class PermissionDeniedError(RpcError):
    """Raised when the user does not have permission to access the resource."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message, grpc.StatusCode.PERMISSION_DENIED)


class NotFoundError(RpcError):
    """Raised when the resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, grpc.StatusCode.NOT_FOUND)


class AlreadyExistsError(RpcError):
    """Raised when the resource already exists."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message, grpc.StatusCode.ALREADY_EXISTS)


class FailedPreconditionError(RpcError):
    """Raised when the resource is not in the correct state to perform the operation."""

    def __init__(self, message: str = "Failed precondition") -> None:
        super().__init__(message, grpc.StatusCode.FAILED_PRECONDITION)
