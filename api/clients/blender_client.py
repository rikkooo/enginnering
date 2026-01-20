"""
Blender Socket Client

Async client for communicating with the Blender socket server.
"""

from typing import Any, Dict, List, Optional
from .base_client import BaseSocketClient


class BlenderClient(BaseSocketClient):
    """
    Client for Blender socket server.
    
    Provides typed methods for common Blender operations.
    """
    
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9876,
        **kwargs
    ):
        super().__init__(host=host, port=port, **kwargs)
        
    # Primitives
    async def create_cube(
        self,
        location: List[float] = None,
        size: float = 2.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"size": size}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_cube", params)
        
    async def create_sphere(
        self,
        location: List[float] = None,
        radius: float = 1.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"radius": radius}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_sphere", params)
        
    async def create_cylinder(
        self,
        location: List[float] = None,
        radius: float = 1.0,
        depth: float = 2.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"radius": radius, "depth": depth}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_cylinder", params)
        
    async def create_cone(
        self,
        location: List[float] = None,
        radius1: float = 1.0,
        radius2: float = 0.0,
        depth: float = 2.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"radius1": radius1, "radius2": radius2, "depth": depth}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_cone", params)
        
    async def create_torus(
        self,
        location: List[float] = None,
        major_radius: float = 1.0,
        minor_radius: float = 0.25,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"major_radius": major_radius, "minor_radius": minor_radius}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_torus", params)
        
    async def create_plane(
        self,
        location: List[float] = None,
        size: float = 2.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"size": size}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("create_plane", params)
        
    # Objects
    async def list_objects(self) -> Dict[str, Any]:
        return await self.send_command("list_objects")
        
    async def get_object(self, name: str) -> Dict[str, Any]:
        return await self.send_command("get_object", {"name": name})
        
    async def delete_object(self, name: str) -> Dict[str, Any]:
        return await self.send_command("delete_object", {"name": name})
        
    async def transform_object(
        self,
        name: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None
    ) -> Dict[str, Any]:
        params = {"name": name}
        if location:
            params["location"] = location
        if rotation:
            params["rotation"] = rotation
        if scale:
            params["scale"] = scale
        return await self.send_command("transform_object", params)
        
    # Materials
    async def create_material(
        self,
        name: str,
        color: List[float] = None,
        metallic: float = 0.0,
        roughness: float = 0.5
    ) -> Dict[str, Any]:
        params = {"name": name, "metallic": metallic, "roughness": roughness}
        if color:
            params["color"] = color
        return await self.send_command("create_material", params)
        
    async def apply_material(self, object_name: str, material_name: str) -> Dict[str, Any]:
        return await self.send_command("apply_material", {
            "object_name": object_name,
            "material_name": material_name
        })
        
    # Scene
    async def get_scene_info(self) -> Dict[str, Any]:
        return await self.send_command("get_scene_info")
        
    async def clear_scene(self) -> Dict[str, Any]:
        return await self.send_command("clear_scene")
        
    async def add_camera(
        self,
        location: List[float] = None,
        rotation: List[float] = None,
        name: str = None
    ) -> Dict[str, Any]:
        params = {}
        if location:
            params["location"] = location
        if rotation:
            params["rotation"] = rotation
        if name:
            params["name"] = name
        return await self.send_command("add_camera", params)
        
    async def add_light(
        self,
        light_type: str = "POINT",
        location: List[float] = None,
        energy: float = 1000.0,
        name: str = None
    ) -> Dict[str, Any]:
        params = {"light_type": light_type, "energy": energy}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return await self.send_command("add_light", params)
        
    # Rendering
    async def render_image(
        self,
        output_path: str,
        resolution_x: int = 1920,
        resolution_y: int = 1080,
        engine: str = "CYCLES",
        samples: int = 128
    ) -> Dict[str, Any]:
        return await self.send_command("render_image", {
            "output_path": output_path,
            "resolution_x": resolution_x,
            "resolution_y": resolution_y,
            "engine": engine,
            "samples": samples
        })
        
    # Export
    async def export_model(
        self,
        filepath: str,
        format: str = "GLB",
        objects: List[str] = None
    ) -> Dict[str, Any]:
        params = {"filepath": filepath, "format": format}
        if objects:
            params["objects"] = objects
        return await self.send_command(f"export_{format.lower()}", params)
        
    # Code Execution
    async def execute_python(self, code: str) -> Dict[str, Any]:
        return await self.send_command("execute_python", {"code": code})
