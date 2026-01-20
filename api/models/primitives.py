"""
Primitive Models

Request models for creating 3D primitives.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class CubeParams(BaseModel):
    """Parameters for creating a Blender cube."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    size: float = Field(2.0, gt=0, description="Size of the cube")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "size": 2.0, "name": "MyCube"}
        }


class SphereParams(BaseModel):
    """Parameters for creating a sphere."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    radius: float = Field(1.0, gt=0, description="Sphere radius")
    segments: int = Field(32, ge=3, description="Number of segments")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "radius": 1.0, "name": "MySphere"}
        }


class CylinderParams(BaseModel):
    """Parameters for creating a cylinder."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    radius: float = Field(1.0, gt=0, description="Cylinder radius")
    depth: float = Field(2.0, gt=0, description="Cylinder height/depth")
    vertices: int = Field(32, ge=3, description="Number of vertices")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "radius": 1.0, "depth": 2.0, "name": "MyCylinder"}
        }


class ConeParams(BaseModel):
    """Parameters for creating a cone."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    radius1: float = Field(1.0, ge=0, description="Bottom radius")
    radius2: float = Field(0.0, ge=0, description="Top radius (0 for point)")
    depth: float = Field(2.0, gt=0, description="Cone height")
    vertices: int = Field(32, ge=3, description="Number of vertices")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "radius1": 1.0, "radius2": 0.0, "depth": 2.0}
        }


class TorusParams(BaseModel):
    """Parameters for creating a torus."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    major_radius: float = Field(1.0, gt=0, description="Major radius (ring)")
    minor_radius: float = Field(0.25, gt=0, description="Minor radius (tube)")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "major_radius": 1.0, "minor_radius": 0.25}
        }


class PlaneParams(BaseModel):
    """Parameters for creating a plane."""
    location: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    size: float = Field(2.0, gt=0, description="Size of the plane")
    name: Optional[str] = Field(None, description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"location": [0, 0, 0], "size": 2.0, "name": "MyPlane"}
        }


class BoxParams(BaseModel):
    """Parameters for creating a FreeCAD box."""
    length: float = Field(10.0, gt=0, description="Length (X dimension)")
    width: float = Field(10.0, gt=0, description="Width (Y dimension)")
    height: float = Field(10.0, gt=0, description="Height (Z dimension)")
    position: Optional[List[float]] = Field(None, description="XYZ position [x, y, z]")
    name: str = Field("Box", description="Object name")
    
    class Config:
        json_schema_extra = {
            "example": {"length": 10.0, "width": 10.0, "height": 10.0, "name": "MyBox"}
        }
