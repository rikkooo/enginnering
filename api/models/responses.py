"""
Response Models

Response models for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ObjectInfo(BaseModel):
    """Information about a 3D object."""
    name: str = Field(..., description="Object name")
    type: str = Field(..., description="Object type (MESH, CURVE, etc.)")
    location: Optional[List[float]] = Field(None, description="XYZ position")
    dimensions: Optional[List[float]] = Field(None, description="Object dimensions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cube",
                "type": "MESH",
                "location": [0.0, 0.0, 0.0],
                "dimensions": [2.0, 2.0, 2.0]
            }
        }


class SceneInfo(BaseModel):
    """Information about the scene."""
    name: str = Field(..., description="Scene name")
    object_count: int = Field(..., description="Number of objects")
    objects: List[ObjectInfo] = Field(default_factory=list, description="List of objects")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Scene",
                "object_count": 2,
                "objects": [
                    {"name": "Cube", "type": "MESH", "location": [0, 0, 0]},
                    {"name": "Camera", "type": "CAMERA", "location": [7, -7, 5]}
                ]
            }
        }


class HealthStatus(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    api_version: str = Field(..., description="API version")
    blender_connected: Optional[bool] = Field(None, description="Blender server status")
    freecad_connected: Optional[bool] = Field(None, description="FreeCAD server status")


class VersionInfo(BaseModel):
    """Version information response."""
    api_version: str
    blender_version: Optional[str] = None
    freecad_version: Optional[str] = None
