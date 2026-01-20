"""
Material Models

Request models for material operations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class MaterialParams(BaseModel):
    """Parameters for creating a material."""
    name: str = Field(..., description="Material name")
    color: Optional[List[float]] = Field(None, description="RGBA color [r, g, b, a]")
    metallic: float = Field(0.0, ge=0.0, le=1.0, description="Metallic value")
    roughness: float = Field(0.5, ge=0.0, le=1.0, description="Roughness value")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "RedMetal",
                "color": [1.0, 0.0, 0.0, 1.0],
                "metallic": 0.8,
                "roughness": 0.2
            }
        }


class ApplyMaterialParams(BaseModel):
    """Parameters for applying a material to an object."""
    object_name: str = Field(..., description="Target object name")
    material_name: str = Field(..., description="Material name to apply")
    
    class Config:
        json_schema_extra = {
            "example": {"object_name": "Cube", "material_name": "RedMetal"}
        }
