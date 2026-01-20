"""
Health and Status Endpoints

Endpoints for checking API and backend service health.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any

from ..config import settings
from ..clients import BlenderClient, FreeCADClient
from ..models.responses import HealthStatus, VersionInfo

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthStatus)
async def health_check() -> Dict[str, Any]:
    """
    Check API health status.
    
    Returns basic health information about the API.
    """
    return {
        "status": "healthy",
        "api_version": settings.api_version,
        "blender_connected": None,
        "freecad_connected": None
    }


@router.get("/health/blender")
async def blender_health() -> Dict[str, Any]:
    """
    Check Blender server health.
    
    Attempts to ping the Blender socket server.
    """
    client = BlenderClient(
        host=settings.blender_host,
        port=settings.blender_port,
        timeout=5.0
    )
    try:
        connected = await client.ping()
        if connected:
            version_response = await client.get_version()
            version = version_response.get("result", {}).get("blender_version", "unknown")
        else:
            version = None
        return {
            "status": "connected" if connected else "disconnected",
            "host": settings.blender_host,
            "port": settings.blender_port,
            "version": version
        }
    except Exception as e:
        return {
            "status": "error",
            "host": settings.blender_host,
            "port": settings.blender_port,
            "error": str(e)
        }
    finally:
        await client.disconnect()


@router.get("/health/freecad")
async def freecad_health() -> Dict[str, Any]:
    """
    Check FreeCAD server health.
    
    Attempts to ping the FreeCAD socket server.
    """
    client = FreeCADClient(
        host=settings.freecad_host,
        port=settings.freecad_port,
        timeout=5.0
    )
    try:
        connected = await client.ping()
        if connected:
            version_response = await client.get_version()
            version = version_response.get("result", {}).get("freecad_version", "unknown")
        else:
            version = None
        return {
            "status": "connected" if connected else "disconnected",
            "host": settings.freecad_host,
            "port": settings.freecad_port,
            "version": version
        }
    except Exception as e:
        return {
            "status": "error",
            "host": settings.freecad_host,
            "port": settings.freecad_port,
            "error": str(e)
        }
    finally:
        await client.disconnect()


@router.get("/version", response_model=VersionInfo)
async def get_version() -> Dict[str, Any]:
    """
    Get version information for API and backends.
    """
    result = {"api_version": settings.api_version}
    
    # Get Blender version
    blender_client = BlenderClient(
        host=settings.blender_host,
        port=settings.blender_port,
        timeout=5.0
    )
    try:
        if await blender_client.ping():
            response = await blender_client.get_version()
            result["blender_version"] = response.get("result", {}).get("blender_version")
    except:
        pass
    finally:
        await blender_client.disconnect()
        
    # Get FreeCAD version
    freecad_client = FreeCADClient(
        host=settings.freecad_host,
        port=settings.freecad_port,
        timeout=5.0
    )
    try:
        if await freecad_client.ping():
            response = await freecad_client.get_version()
            result["freecad_version"] = response.get("result", {}).get("freecad_version")
    except:
        pass
    finally:
        await freecad_client.disconnect()
        
    return result
