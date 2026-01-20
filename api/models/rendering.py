"""
Rendering Models

Request models for rendering operations.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class RenderParams(BaseModel):
    """Parameters for rendering an image."""
    output_path: str = Field(..., description="Output file path")
    resolution_x: int = Field(1920, ge=1, description="Horizontal resolution")
    resolution_y: int = Field(1080, ge=1, description="Vertical resolution")
    engine: Literal["CYCLES", "EEVEE", "WORKBENCH"] = Field("CYCLES", description="Render engine")
    samples: int = Field(128, ge=1, description="Number of samples")
    
    class Config:
        json_schema_extra = {
            "example": {
                "output_path": "/tmp/render.png",
                "resolution_x": 1920,
                "resolution_y": 1080,
                "engine": "CYCLES",
                "samples": 128
            }
        }


class CameraParams(BaseModel):
    """Parameters for adding a camera."""
    location: Optional[list] = Field(None, description="XYZ position")
    rotation: Optional[list] = Field(None, description="XYZ rotation (radians)")
    name: Optional[str] = Field(None, description="Camera name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [7, -7, 5], "rotation": [1.1, 0, 0.8], "name": "MainCamera"}
        }


class LightParams(BaseModel):
    """Parameters for adding a light."""
    light_type: Literal["POINT", "SUN", "SPOT", "AREA"] = Field("POINT", description="Light type")
    location: Optional[list] = Field(None, description="XYZ position")
    energy: float = Field(1000.0, ge=0, description="Light energy/power")
    name: Optional[str] = Field(None, description="Light name")
    
    class Config:
        json_schema_extra = {
            "example": {"light_type": "SUN", "location": [5, 5, 10], "energy": 5.0}
        }
