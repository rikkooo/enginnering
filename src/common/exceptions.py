"""
Custom Exceptions for 3DM-API
=============================
Defines exception classes for error handling across the system.
"""


class TDMAPIError(Exception):
    """Base exception for all 3DM-API errors."""
    
    def __init__(self, message: str, code: str = "TDMAPI_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for JSON serialization."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class ConnectionError(TDMAPIError):
    """Raised when connection to server fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="CONNECTION_ERROR", details=details)


class CommandError(TDMAPIError):
    """Raised when a command execution fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="COMMAND_ERROR", details=details)


class ValidationError(TDMAPIError):
    """Raised when request validation fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class TimeoutError(TDMAPIError):
    """Raised when an operation times out."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="TIMEOUT_ERROR", details=details)


class MethodNotFoundError(TDMAPIError):
    """Raised when requested method is not found."""
    
    def __init__(self, method: str):
        super().__init__(
            message=f"Method not found: {method}",
            code="METHOD_NOT_FOUND",
            details={"method": method}
        )


class ObjectNotFoundError(TDMAPIError):
    """Raised when a requested object is not found."""
    
    def __init__(self, object_name: str):
        super().__init__(
            message=f"Object not found: {object_name}",
            code="OBJECT_NOT_FOUND",
            details={"object_name": object_name}
        )


class MaterialNotFoundError(TDMAPIError):
    """Raised when a requested material is not found."""
    
    def __init__(self, material_name: str):
        super().__init__(
            message=f"Material not found: {material_name}",
            code="MATERIAL_NOT_FOUND",
            details={"material_name": material_name}
        )


class RenderError(TDMAPIError):
    """Raised when rendering fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="RENDER_ERROR", details=details)


class ExportError(TDMAPIError):
    """Raised when export operation fails."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="EXPORT_ERROR", details=details)


class ServerError(TDMAPIError):
    """Raised when server encounters an internal error."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="SERVER_ERROR", details=details)
