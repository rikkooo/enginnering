"""
FreeCAD REST Endpoints

REST API endpoints for FreeCAD operations.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional

from ..config import settings
from ..clients import FreeCADClient
from ..models.primitives import BoxParams, SphereParams, CylinderParams, ConeParams, TorusParams
from ..models.boolean import UnionParams, SubtractParams, IntersectParams
from ..models.export import FreeCADExportParams

router = APIRouter(prefix="/api/v1/freecad", tags=["FreeCAD"])


async def get_client() -> FreeCADClient:
    """Get a FreeCAD client instance."""
    client = FreeCADClient(
        host=settings.freecad_host,
        port=settings.freecad_port,
        timeout=settings.freecad_timeout
    )
    return client


def extract_result(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract result from response or raise HTTPException on error."""
    if "error" in response:
        error = response["error"]
        raise HTTPException(
            status_code=500,
            detail={"code": error.get("code", "ERROR"), "message": error.get("message", "Unknown error")}
        )
    return response.get("result", response)


# Documents

@router.get("/documents")
async def list_documents() -> Dict[str, Any]:
    """List all open documents."""
    client = await get_client()
    try:
        response = await client.list_documents()
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/documents")
async def new_document(name: str = "Unnamed") -> Dict[str, Any]:
    """Create a new document."""
    client = await get_client()
    try:
        response = await client.new_document(name)
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Primitives

@router.post("/primitives/box")
async def create_box(params: BoxParams) -> Dict[str, Any]:
    """Create a box primitive."""
    client = await get_client()
    try:
        response = await client.create_box(
            length=params.length,
            width=params.width,
            height=params.height,
            position=params.position,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/sphere")
async def create_sphere(params: SphereParams) -> Dict[str, Any]:
    """Create a sphere primitive."""
    client = await get_client()
    try:
        response = await client.create_sphere(
            radius=params.radius,
            position=params.location,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/cylinder")
async def create_cylinder(params: CylinderParams) -> Dict[str, Any]:
    """Create a cylinder primitive."""
    client = await get_client()
    try:
        response = await client.create_cylinder(
            radius=params.radius,
            height=params.depth,
            position=params.location,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/cone")
async def create_cone(params: ConeParams) -> Dict[str, Any]:
    """Create a cone primitive."""
    client = await get_client()
    try:
        response = await client.create_cone(
            radius1=params.radius1,
            radius2=params.radius2,
            height=params.depth,
            position=params.location,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/torus")
async def create_torus(params: TorusParams) -> Dict[str, Any]:
    """Create a torus primitive."""
    client = await get_client()
    try:
        response = await client.create_torus(
            radius1=params.major_radius,
            radius2=params.minor_radius,
            position=params.location,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Objects

@router.get("/objects")
async def list_objects() -> Dict[str, Any]:
    """List all objects in the active document."""
    client = await get_client()
    try:
        response = await client.list_objects()
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.get("/objects/{name}")
async def get_object(name: str) -> Dict[str, Any]:
    """Get information about a specific object."""
    client = await get_client()
    try:
        response = await client.get_object(name)
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.delete("/objects/{name}")
async def delete_object(name: str) -> Dict[str, Any]:
    """Delete an object by name."""
    client = await get_client()
    try:
        response = await client.delete_object(name)
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Boolean Operations

@router.post("/boolean/union")
async def boolean_union(params: UnionParams) -> Dict[str, Any]:
    """Perform boolean union of two objects."""
    client = await get_client()
    try:
        response = await client.boolean_union(
            object1=params.object1,
            object2=params.object2,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/boolean/subtract")
async def boolean_subtract(params: SubtractParams) -> Dict[str, Any]:
    """Perform boolean subtraction (base - tool)."""
    client = await get_client()
    try:
        response = await client.boolean_subtract(
            base=params.base,
            tool=params.tool,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/boolean/intersect")
async def boolean_intersect(params: IntersectParams) -> Dict[str, Any]:
    """Perform boolean intersection of two objects."""
    client = await get_client()
    try:
        response = await client.boolean_intersect(
            object1=params.object1,
            object2=params.object2,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Export

@router.post("/export")
async def export_model(params: FreeCADExportParams) -> Dict[str, Any]:
    """Export objects to file."""
    client = await get_client()
    try:
        if params.format == "STEP":
            response = await client.export_step(params.filepath, params.objects)
        elif params.format == "STL":
            response = await client.export_stl(params.filepath, params.objects)
        else:
            # Generic export via command
            response = await client.send_command(f"export_{params.format.lower()}", {
                "filepath": params.filepath,
                "objects": params.objects
            })
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()
