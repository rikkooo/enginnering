"""
Export Models

Request models for export operations.
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class ExportParams(BaseModel):
    """Parameters for exporting models."""
    filepath: str = Field(..., description="Output file path")
    format: Literal["GLB", "GLTF", "FBX", "OBJ", "STL", "STEP", "IGES", "BREP"] = Field(
        ..., description="Export format"
    )
    objects: Optional[List[str]] = Field(None, description="Object names (all if None)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filepath": "/tmp/model.glb",
                "format": "GLB",
                "objects": ["Cube", "Sphere"]
            }
        }


class BlenderExportParams(BaseModel):
    """Parameters for Blender export."""
    filepath: str = Field(..., description="Output file path")
    format: Literal["GLB", "GLTF", "FBX", "OBJ", "STL"] = Field("GLB", description="Export format")
    objects: Optional[List[str]] = Field(None, description="Object names (all if None)")


class FreeCADExportParams(BaseModel):
    """Parameters for FreeCAD export."""
    filepath: str = Field(..., description="Output file path")
    format: Literal["STEP", "IGES", "STL", "OBJ", "BREP"] = Field("STEP", description="Export format")
    objects: Optional[List[str]] = Field(None, description="Object names (all if None)")
