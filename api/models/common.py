"""
Common Pydantic Models

Shared models used across the API.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union


class Vector3(BaseModel):
    """3D vector for positions, rotations, scales."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
        
    class Config:
        json_schema_extra = {
            "example": {"x": 0.0, "y": 0.0, "z": 0.0}
        }


class Color(BaseModel):
    """RGBA color."""
    r: float = Field(1.0, ge=0.0, le=1.0)
    g: float = Field(1.0, ge=0.0, le=1.0)
    b: float = Field(1.0, ge=0.0, le=1.0)
    a: float = Field(1.0, ge=0.0, le=1.0)
    
    def to_list(self) -> List[float]:
        return [self.r, self.g, self.b, self.a]
        
    class Config:
        json_schema_extra = {
            "example": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0}
        }


class APIError(BaseModel):
    """API error details."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    status: str = "success"
    result: Optional[Any] = None
    error: Optional[APIError] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "result": {"object_id": "Cube", "type": "MESH"}
            }
        }
