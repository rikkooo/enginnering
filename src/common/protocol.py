"""
JSON-RPC Protocol Implementation
================================
Defines the message format for communication between clients and servers.
Uses a simplified JSON-RPC 2.0 style protocol.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Dict


@dataclass
class Request:
    """
    Represents a JSON-RPC request message.
    
    Attributes:
        method: The method name to invoke
        params: Optional parameters for the method
        id: Optional request ID for correlation
    """
    method: str
    params: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    
    def to_json(self) -> str:
        """Serialize request to JSON string with newline delimiter."""
        data = {
            "method": self.method,
            "params": self.params,
        }
        if self.id is not None:
            data["id"] = self.id
        return json.dumps(data) + "\n"
    
    @classmethod
    def from_json(cls, json_str: str) -> "Request":
        """Parse a JSON string into a Request object."""
        data = json.loads(json_str.strip())
        return cls(
            method=data.get("method", ""),
            params=data.get("params", {}),
            id=data.get("id"),
        )


@dataclass
class Response:
    """
    Represents a successful JSON-RPC response message.
    
    Attributes:
        status: Always "success" for successful responses
        result: The result data from the method execution
        id: Optional request ID for correlation
    """
    result: Any
    id: Optional[str] = None
    status: str = "success"
    
    def to_json(self) -> str:
        """Serialize response to JSON string with newline delimiter."""
        data = {
            "status": self.status,
            "result": self.result,
        }
        if self.id is not None:
            data["id"] = self.id
        return json.dumps(data) + "\n"
    
    @classmethod
    def from_json(cls, json_str: str) -> "Response":
        """Parse a JSON string into a Response object."""
        data = json.loads(json_str.strip())
        return cls(
            status=data.get("status", "success"),
            result=data.get("result"),
            id=data.get("id"),
        )


@dataclass
class ErrorResponse:
    """
    Represents an error JSON-RPC response message.
    
    Attributes:
        status: Always "error" for error responses
        error: Error details including code and message
        id: Optional request ID for correlation
    """
    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    status: str = "error"
    
    def to_json(self) -> str:
        """Serialize error response to JSON string with newline delimiter."""
        data = {
            "status": self.status,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            },
        }
        if self.id is not None:
            data["id"] = self.id
        return json.dumps(data) + "\n"
    
    @classmethod
    def from_json(cls, json_str: str) -> "ErrorResponse":
        """Parse a JSON string into an ErrorResponse object."""
        data = json.loads(json_str.strip())
        error = data.get("error", {})
        return cls(
            status=data.get("status", "error"),
            code=error.get("code", "UNKNOWN"),
            message=error.get("message", "Unknown error"),
            details=error.get("details", {}),
            id=data.get("id"),
        )


def parse_message(json_str: str) -> Request | Response | ErrorResponse:
    """
    Parse a JSON string into the appropriate message type.
    
    Args:
        json_str: The JSON string to parse
        
    Returns:
        Request, Response, or ErrorResponse depending on content
    """
    data = json.loads(json_str.strip())
    
    if "method" in data:
        return Request.from_json(json_str)
    elif data.get("status") == "error":
        return ErrorResponse.from_json(json_str)
    else:
        return Response.from_json(json_str)
