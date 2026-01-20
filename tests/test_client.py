#!/usr/bin/env python3
"""
Simple Test Client for 3DM-API Blender Server
==============================================
A basic socket client for testing the Blender server.

Usage:
    python test_client.py
    python test_client.py --host localhost --port 9876
"""

import socket
import json
import argparse
from typing import Any, Optional


class BlenderTestClient:
    """Simple test client for the Blender socket server."""
    
    def __init__(self, host: str = 'localhost', port: int = 9876):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Connect to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(30.0)
        print(f"Connected to {self.host}:{self.port}")
    
    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected")
    
    def send_command(self, method: str, params: dict = None, request_id: str = None) -> dict:
        """
        Send a command to the server and return the response.
        
        Args:
            method: The method name to call
            params: Optional parameters
            request_id: Optional request ID
            
        Returns:
            The response dictionary
        """
        if self.socket is None:
            raise RuntimeError("Not connected")
        
        request = {
            "method": method,
            "params": params or {},
        }
        if request_id:
            request["id"] = request_id
        
        # Send request
        message = json.dumps(request) + "\n"
        self.socket.send(message.encode('utf-8'))
        
        # Receive response
        buffer = ""
        while '\n' not in buffer:
            data = self.socket.recv(4096)
            if not data:
                raise RuntimeError("Connection closed")
            buffer += data.decode('utf-8')
        
        response_str = buffer.split('\n')[0]
        return json.loads(response_str)
    
    def ping(self) -> dict:
        """Send a ping command."""
        return self.send_command("ping")
    
    def get_version(self) -> dict:
        """Get Blender version info."""
        return self.send_command("get_version")
    
    def list_methods(self) -> dict:
        """List available methods."""
        return self.send_command("list_methods")
    
    def create_cube(self, location=None, size=2.0, name=None) -> dict:
        """Create a cube."""
        params = {"size": size}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return self.send_command("create_cube", params)
    
    def create_sphere(self, location=None, radius=1.0, name=None) -> dict:
        """Create a sphere."""
        params = {"radius": radius}
        if location:
            params["location"] = location
        if name:
            params["name"] = name
        return self.send_command("create_sphere", params)
    
    def list_objects(self) -> dict:
        """List all objects."""
        return self.send_command("list_objects")
    
    def delete_object(self, name: str) -> dict:
        """Delete an object."""
        return self.send_command("delete_object", {"name": name})
    
    def create_material(self, name: str, color=None) -> dict:
        """Create a material."""
        params = {"name": name}
        if color:
            params["color"] = color
        return self.send_command("create_material", params)
    
    def apply_material(self, object_name: str, material_name: str) -> dict:
        """Apply a material to an object."""
        return self.send_command("apply_material", {
            "object_name": object_name,
            "material_name": material_name
        })
    
    def render_image(self, output_path: str) -> dict:
        """Render to an image."""
        return self.send_command("render_image", {"output_path": output_path})
    
    def export_gltf(self, filepath: str) -> dict:
        """Export to GLTF/GLB."""
        return self.send_command("export_gltf", {"filepath": filepath})
    
    def clear_scene(self) -> dict:
        """Clear the scene."""
        return self.send_command("clear_scene")
    
    def get_scene_info(self) -> dict:
        """Get scene information."""
        return self.send_command("get_scene_info")


def run_tests(client: BlenderTestClient):
    """Run a series of tests."""
    print("\n" + "=" * 50)
    print("Running Tests")
    print("=" * 50)
    
    # Test 1: Ping
    print("\n[Test 1] Ping...")
    result = client.ping()
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Ping failed"
    print("  ✓ Passed")
    
    # Test 2: Get Version
    print("\n[Test 2] Get Version...")
    result = client.get_version()
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Get version failed"
    print("  ✓ Passed")
    
    # Test 3: List Methods
    print("\n[Test 3] List Methods...")
    result = client.list_methods()
    print(f"  Methods: {result.get('result', {}).get('methods', [])[:5]}...")
    assert result.get("status") == "success", "List methods failed"
    print("  ✓ Passed")
    
    # Test 4: Clear Scene
    print("\n[Test 4] Clear Scene...")
    result = client.clear_scene()
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Clear scene failed"
    print("  ✓ Passed")
    
    # Test 5: Create Cube
    print("\n[Test 5] Create Cube...")
    result = client.create_cube(location=[0, 0, 0], size=2, name="TestCube")
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Create cube failed"
    print("  ✓ Passed")
    
    # Test 6: Create Sphere
    print("\n[Test 6] Create Sphere...")
    result = client.create_sphere(location=[3, 0, 0], radius=1, name="TestSphere")
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Create sphere failed"
    print("  ✓ Passed")
    
    # Test 7: List Objects
    print("\n[Test 7] List Objects...")
    result = client.list_objects()
    print(f"  Objects: {result.get('result', {}).get('objects', [])}")
    assert result.get("status") == "success", "List objects failed"
    print("  ✓ Passed")
    
    # Test 8: Create Material
    print("\n[Test 8] Create Material...")
    result = client.create_material("RedMaterial", color=[1, 0, 0, 1])
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Create material failed"
    print("  ✓ Passed")
    
    # Test 9: Apply Material
    print("\n[Test 9] Apply Material...")
    result = client.apply_material("TestCube", "RedMaterial")
    print(f"  Result: {result}")
    assert result.get("status") == "success", "Apply material failed"
    print("  ✓ Passed")
    
    # Test 10: Get Scene Info
    print("\n[Test 10] Get Scene Info...")
    result = client.get_scene_info()
    print(f"  Scene: {result.get('result', {}).get('scene_name')}")
    print(f"  Object count: {result.get('result', {}).get('object_count')}")
    assert result.get("status") == "success", "Get scene info failed"
    print("  ✓ Passed")
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description='3DM-API Test Client')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=9876, help='Server port')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    args = parser.parse_args()
    
    client = BlenderTestClient(host=args.host, port=args.port)
    
    try:
        client.connect()
        
        if args.interactive:
            print("Interactive mode. Type 'help' for commands, 'quit' to exit.")
            while True:
                try:
                    cmd = input("> ").strip()
                    if cmd == 'quit':
                        break
                    elif cmd == 'help':
                        print("Commands: ping, version, methods, cube, sphere, list, clear, scene, quit")
                    elif cmd == 'ping':
                        print(client.ping())
                    elif cmd == 'version':
                        print(client.get_version())
                    elif cmd == 'methods':
                        print(client.list_methods())
                    elif cmd == 'cube':
                        print(client.create_cube())
                    elif cmd == 'sphere':
                        print(client.create_sphere(location=[3, 0, 0]))
                    elif cmd == 'list':
                        print(client.list_objects())
                    elif cmd == 'clear':
                        print(client.clear_scene())
                    elif cmd == 'scene':
                        print(client.get_scene_info())
                    else:
                        print(f"Unknown command: {cmd}")
                except KeyboardInterrupt:
                    break
        else:
            run_tests(client)
            
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {args.host}:{args.port}")
        print("Make sure the Blender server is running:")
        print("  blender -b -P src/blender/scripts/start_server.py")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
