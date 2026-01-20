"""
Boolean Operation Models

Request models for boolean operations.
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class BooleanParams(BaseModel):
    """Parameters for boolean operations."""
    object1: str = Field(..., description="First object name")
    object2: str = Field(..., description="Second object name")
    operation: Literal["union", "subtract", "intersect"] = Field(..., description="Boolean operation")
    name: Optional[str] = Field(None, description="Result object name")
    delete_originals: bool = Field(False, description="Delete original objects")
    
    class Config:
        json_schema_extra = {
            "example": {
                "object1": "Box",
                "object2": "Sphere",
                "operation": "subtract",
                "name": "Result"
            }
        }


class UnionParams(BaseModel):
    """Parameters for boolean union."""
    object1: str = Field(..., description="First object name")
    object2: str = Field(..., description="Second object name")
    name: str = Field("Union", description="Result object name")
    delete_originals: bool = Field(False, description="Delete original objects")


class SubtractParams(BaseModel):
    """Parameters for boolean subtraction."""
    base: str = Field(..., description="Base object name")
    tool: str = Field(..., description="Tool object name (to subtract)")
    name: str = Field("Subtract", description="Result object name")
    delete_originals: bool = Field(False, description="Delete original objects")


class IntersectParams(BaseModel):
    """Parameters for boolean intersection."""
    object1: str = Field(..., description="First object name")
    object2: str = Field(..., description="Second object name")
    name: str = Field("Intersect", description="Result object name")
    delete_originals: bool = Field(False, description="Delete original objects")
