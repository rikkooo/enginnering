"""
Function Executor

Execute AI function calls by routing to the appropriate API endpoints.
"""

import httpx
from typing import Any, Dict, Optional


class FunctionExecutor:
    """
    Execute AI function calls against the 3DM-API.
    
    Maps function names to API endpoints and handles responses.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=60.0)
        self._async_client: Optional[httpx.AsyncClient] = None
        
    def close(self):
        """Close the HTTP client."""
        self.client.close()
        if self._async_client:
            # Note: async client should be closed with await
            pass
            
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function call synchronously.
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            API response dictionary
        """
        endpoint, method, payload = self._map_function(function_name, arguments)
        
        if method == "GET":
            response = self.client.get(f"{self.base_url}{endpoint}")
        elif method == "POST":
            response = self.client.post(f"{self.base_url}{endpoint}", json=payload)
        elif method == "DELETE":
            response = self.client.delete(f"{self.base_url}{endpoint}")
        elif method == "PATCH":
            response = self.client.patch(f"{self.base_url}{endpoint}", json=payload)
        else:
            return {"status": "error", "error": f"Unknown method: {method}"}
            
        return response.json()
        
    async def execute_async(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function call asynchronously.
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            API response dictionary
        """
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(timeout=60.0)
            
        endpoint, method, payload = self._map_function(function_name, arguments)
        
        if method == "GET":
            response = await self._async_client.get(f"{self.base_url}{endpoint}")
        elif method == "POST":
            response = await self._async_client.post(f"{self.base_url}{endpoint}", json=payload)
        elif method == "DELETE":
            response = await self._async_client.delete(f"{self.base_url}{endpoint}")
        elif method == "PATCH":
            response = await self._async_client.patch(f"{self.base_url}{endpoint}", json=payload)
        else:
            return {"status": "error", "error": f"Unknown method: {method}"}
            
        return response.json()
        
    def _map_function(self, function_name: str, args: Dict[str, Any]) -> tuple:
        """
        Map function name and arguments to API endpoint.
        
        Returns:
            Tuple of (endpoint, method, payload)
        """
        app = args.get('application', 'blender')
        
        if function_name == "create_3d_primitive":
            ptype = args.get('primitive_type', 'cube')
            # Map primitive type to endpoint
            if app == 'freecad' and ptype == 'cube':
                ptype = 'box'
            endpoint = f"/api/v1/{app}/primitives/{ptype}"
            payload = {k: v for k, v in args.items() if k not in ['application', 'primitive_type']}
            return endpoint, "POST", payload
            
        elif function_name == "modify_object":
            action = args.get('action', 'transform')
            obj_name = args.get('object_name')
            
            if action == 'delete':
                return f"/api/v1/{app}/objects/{obj_name}", "DELETE", {}
            elif action == 'rename':
                # Use transform endpoint with rename
                payload = {"new_name": args.get('new_name')}
                return f"/api/v1/{app}/objects/{obj_name}", "PATCH", payload
            else:  # transform
                payload = {}
                if 'location' in args:
                    payload['location'] = args['location']
                if 'rotation' in args:
                    payload['rotation'] = args['rotation']
                if 'scale' in args:
                    payload['scale'] = args['scale']
                return f"/api/v1/{app}/objects/{obj_name}", "PATCH", payload
                
        elif function_name == "apply_material":
            # First create material, then apply
            obj_name = args.get('object_name')
            mat_name = args.get('material_name')
            payload = {
                "name": mat_name,
                "color": args.get('color'),
                "metallic": args.get('metallic', 0.0),
                "roughness": args.get('roughness', 0.5)
            }
            # Create material first
            self.client.post(f"{self.base_url}/api/v1/blender/materials", json=payload)
            # Then apply
            return "/api/v1/blender/materials/apply", "POST", {
                "object_name": obj_name,
                "material_name": mat_name
            }
            
        elif function_name == "boolean_operation":
            op = args.get('operation', 'union')
            payload = {
                "object1": args.get('object1'),
                "object2": args.get('object2'),
                "name": args.get('result_name', f"{op.title()}Result")
            }
            if op == 'subtract':
                payload = {
                    "base": args.get('object1'),
                    "tool": args.get('object2'),
                    "name": args.get('result_name', 'SubtractResult')
                }
            return f"/api/v1/freecad/boolean/{op}", "POST", payload
            
        elif function_name == "render_scene":
            payload = {
                "output_path": args.get('output_path'),
                "resolution_x": args.get('resolution_x', 1920),
                "resolution_y": args.get('resolution_y', 1080),
                "engine": args.get('engine', 'CYCLES'),
                "samples": args.get('samples', 128)
            }
            return "/api/v1/blender/render", "POST", payload
            
        elif function_name == "export_model":
            payload = {
                "filepath": args.get('filepath'),
                "format": args.get('format'),
                "objects": args.get('objects')
            }
            return f"/api/v1/{app}/export", "POST", payload
            
        elif function_name == "get_scene_info":
            if app == 'blender':
                return "/api/v1/blender/scene", "GET", {}
            else:
                return "/api/v1/freecad/objects", "GET", {}
                
        elif function_name == "execute_code":
            # Use WebSocket or direct endpoint
            payload = {"code": args.get('code')}
            return f"/api/v1/{app}/execute", "POST", payload
            
        elif function_name == "add_camera":
            payload = {
                "name": args.get('name'),
                "location": args.get('location'),
                "rotation": args.get('rotation')
            }
            return "/api/v1/blender/camera", "POST", payload
            
        elif function_name == "add_light":
            payload = {
                "name": args.get('name'),
                "light_type": args.get('light_type', 'POINT'),
                "location": args.get('location'),
                "energy": args.get('energy', 1000.0)
            }
            return "/api/v1/blender/light", "POST", payload
            
        else:
            return "/health", "GET", {}
