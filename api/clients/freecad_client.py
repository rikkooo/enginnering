"""
FreeCAD Socket Client

Async client for communicating with the FreeCAD socket server.
"""

from typing import Any, Dict, List, Optional
from .base_client import BaseSocketClient


class FreeCADClient(BaseSocketClient):
    """
    Client for FreeCAD socket server.
    
    Provides typed methods for common FreeCAD operations.
    """
    
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9877,
        **kwargs
    ):
        super().__init__(host=host, port=port, **kwargs)
        
    # Documents
    async def new_document(self, name: str = "Unnamed") -> Dict[str, Any]:
        return await self.send_command("new_document", {"name": name})
        
    async def list_documents(self) -> Dict[str, Any]:
        return await self.send_command("list_documents")
        
    async def get_active_document(self) -> Dict[str, Any]:
        return await self.send_command("get_active_document")
        
    # Primitives
    async def create_box(
        self,
        length: float = 10.0,
        width: float = 10.0,
        height: float = 10.0,
        position: List[float] = None,
        name: str = "Box"
    ) -> Dict[str, Any]:
        params = {"length": length, "width": width, "height": height, "name": name}
        if position:
            params["position"] = position
        return await self.send_command("create_box", params)
        
    async def create_sphere(
        self,
        radius: float = 5.0,
        position: List[float] = None,
        name: str = "Sphere"
    ) -> Dict[str, Any]:
        params = {"radius": radius, "name": name}
        if position:
            params["position"] = position
        return await self.send_command("create_sphere", params)
        
    async def create_cylinder(
        self,
        radius: float = 5.0,
        height: float = 10.0,
        position: List[float] = None,
        name: str = "Cylinder"
    ) -> Dict[str, Any]:
        params = {"radius": radius, "height": height, "name": name}
        if position:
            params["position"] = position
        return await self.send_command("create_cylinder", params)
        
    async def create_cone(
        self,
        radius1: float = 5.0,
        radius2: float = 0.0,
        height: float = 10.0,
        position: List[float] = None,
        name: str = "Cone"
    ) -> Dict[str, Any]:
        params = {"radius1": radius1, "radius2": radius2, "height": height, "name": name}
        if position:
            params["position"] = position
        return await self.send_command("create_cone", params)
        
    async def create_torus(
        self,
        radius1: float = 10.0,
        radius2: float = 2.0,
        position: List[float] = None,
        name: str = "Torus"
    ) -> Dict[str, Any]:
        params = {"radius1": radius1, "radius2": radius2, "name": name}
        if position:
            params["position"] = position
        return await self.send_command("create_torus", params)
        
    # Objects
    async def list_objects(self) -> Dict[str, Any]:
        return await self.send_command("list_objects")
        
    async def get_object(self, name: str) -> Dict[str, Any]:
        return await self.send_command("get_object", {"name": name})
        
    async def delete_object(self, name: str) -> Dict[str, Any]:
        return await self.send_command("delete_object", {"name": name})
        
    # Boolean Operations
    async def boolean_union(
        self,
        object1: str,
        object2: str,
        name: str = "Union"
    ) -> Dict[str, Any]:
        return await self.send_command("boolean_union", {
            "object1": object1,
            "object2": object2,
            "name": name
        })
        
    async def boolean_subtract(
        self,
        base: str,
        tool: str,
        name: str = "Subtract"
    ) -> Dict[str, Any]:
        return await self.send_command("boolean_subtract", {
            "base": base,
            "tool": tool,
            "name": name
        })
        
    async def boolean_intersect(
        self,
        object1: str,
        object2: str,
        name: str = "Intersect"
    ) -> Dict[str, Any]:
        return await self.send_command("boolean_intersect", {
            "object1": object1,
            "object2": object2,
            "name": name
        })
        
    # Export
    async def export_step(
        self,
        filepath: str,
        objects: List[str] = None
    ) -> Dict[str, Any]:
        params = {"filepath": filepath}
        if objects:
            params["objects"] = objects
        return await self.send_command("export_step", params)
        
    async def export_stl(
        self,
        filepath: str,
        objects: List[str] = None
    ) -> Dict[str, Any]:
        params = {"filepath": filepath}
        if objects:
            params["objects"] = objects
        return await self.send_command("export_stl", params)
        
    # Code Execution
    async def execute_python(self, code: str) -> Dict[str, Any]:
        return await self.send_command("execute_python", {"code": code})
