"""
Blender REST Endpoints

REST API endpoints for Blender operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional

from ..config import settings
from ..clients import BlenderClient
from ..models.primitives import CubeParams, SphereParams, CylinderParams, ConeParams, TorusParams, PlaneParams
from ..models.materials import MaterialParams, ApplyMaterialParams
from ..models.rendering import RenderParams, CameraParams, LightParams
from ..models.export import BlenderExportParams

router = APIRouter(prefix="/api/v1/blender", tags=["Blender"])


async def get_client() -> BlenderClient:
    """Get a Blender client instance."""
    client = BlenderClient(
        host=settings.blender_host,
        port=settings.blender_port,
        timeout=settings.blender_timeout
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


# Primitives

@router.post("/primitives/cube")
async def create_cube(params: CubeParams) -> Dict[str, Any]:
    """Create a cube mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_cube(
            location=params.location,
            size=params.size,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/sphere")
async def create_sphere(params: SphereParams) -> Dict[str, Any]:
    """Create a sphere mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_sphere(
            location=params.location,
            radius=params.radius,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/cylinder")
async def create_cylinder(params: CylinderParams) -> Dict[str, Any]:
    """Create a cylinder mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_cylinder(
            location=params.location,
            radius=params.radius,
            depth=params.depth,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/cone")
async def create_cone(params: ConeParams) -> Dict[str, Any]:
    """Create a cone mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_cone(
            location=params.location,
            radius1=params.radius1,
            radius2=params.radius2,
            depth=params.depth,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/torus")
async def create_torus(params: TorusParams) -> Dict[str, Any]:
    """Create a torus mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_torus(
            location=params.location,
            major_radius=params.major_radius,
            minor_radius=params.minor_radius,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/primitives/plane")
async def create_plane(params: PlaneParams) -> Dict[str, Any]:
    """Create a plane mesh primitive."""
    client = await get_client()
    try:
        response = await client.create_plane(
            location=params.location,
            size=params.size,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Objects

@router.get("/objects")
async def list_objects() -> Dict[str, Any]:
    """List all objects in the scene."""
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


@router.patch("/objects/{name}")
async def transform_object(
    name: str,
    location: Optional[List[float]] = None,
    rotation: Optional[List[float]] = None,
    scale: Optional[List[float]] = None
) -> Dict[str, Any]:
    """Transform an object (location, rotation, scale)."""
    client = await get_client()
    try:
        response = await client.transform_object(name, location, rotation, scale)
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Materials

@router.post("/materials")
async def create_material(params: MaterialParams) -> Dict[str, Any]:
    """Create a new material."""
    client = await get_client()
    try:
        response = await client.create_material(
            name=params.name,
            color=params.color,
            metallic=params.metallic,
            roughness=params.roughness
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/materials/apply")
async def apply_material(params: ApplyMaterialParams) -> Dict[str, Any]:
    """Apply a material to an object."""
    client = await get_client()
    try:
        response = await client.apply_material(params.object_name, params.material_name)
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Scene

@router.get("/scene")
async def get_scene_info() -> Dict[str, Any]:
    """Get scene information."""
    client = await get_client()
    try:
        response = await client.get_scene_info()
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.delete("/scene")
async def clear_scene() -> Dict[str, Any]:
    """Clear all objects from the scene."""
    client = await get_client()
    try:
        response = await client.clear_scene()
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/camera")
async def add_camera(params: CameraParams) -> Dict[str, Any]:
    """Add a camera to the scene."""
    client = await get_client()
    try:
        response = await client.add_camera(
            location=params.location,
            rotation=params.rotation,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


@router.post("/light")
async def add_light(params: LightParams) -> Dict[str, Any]:
    """Add a light to the scene."""
    client = await get_client()
    try:
        response = await client.add_light(
            light_type=params.light_type,
            location=params.location,
            energy=params.energy,
            name=params.name
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Rendering

@router.post("/render")
async def render_image(params: RenderParams) -> Dict[str, Any]:
    """Render the scene to an image."""
    client = await get_client()
    try:
        response = await client.render_image(
            output_path=params.output_path,
            resolution_x=params.resolution_x,
            resolution_y=params.resolution_y,
            engine=params.engine,
            samples=params.samples
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()


# Export

@router.post("/export")
async def export_model(params: BlenderExportParams) -> Dict[str, Any]:
    """Export the scene or selected objects."""
    client = await get_client()
    try:
        response = await client.export_model(
            filepath=params.filepath,
            format=params.format,
            objects=params.objects
        )
        return {"status": "success", "result": extract_result(response)}
    finally:
        await client.disconnect()
