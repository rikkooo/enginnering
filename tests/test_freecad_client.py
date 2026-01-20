#!/usr/bin/env python3
"""
FreeCAD Socket Server Test Client

Simple test client for validating FreeCAD server functionality.
"""

import socket
import json
import argparse
import sys
from typing import Any, Optional


class FreeCADTestClient:
    """Simple socket client for testing FreeCAD server."""
    
    def __init__(self, host: str = 'localhost', port: int = 9877):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.request_id = 0
        
    def connect(self) -> bool:
        """Connect to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30.0)
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected")
            
    def send_command(self, method: str, params: dict = None) -> dict:
        """Send a JSON-RPC command and return the response."""
        if not self.socket:
            raise RuntimeError("Not connected")
            
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        message = json.dumps(request) + "\n"
        self.socket.sendall(message.encode('utf-8'))
        
        # Receive response
        buffer = ""
        while '\n' not in buffer:
            data = self.socket.recv(4096)
            if not data:
                raise RuntimeError("Connection closed")
            buffer += data.decode('utf-8')
            
        response_str = buffer.split('\n')[0]
        return json.loads(response_str)
        
    # Convenience methods
    def ping(self) -> dict:
        return self.send_command("ping")
        
    def get_version(self) -> dict:
        return self.send_command("get_version")
        
    def list_methods(self) -> dict:
        return self.send_command("list_methods")
        
    def new_document(self, name: str = "TestDoc") -> dict:
        return self.send_command("new_document", {"name": name})
        
    def create_box(self, length: float = 10, width: float = 10, height: float = 10, 
                   name: str = "Box") -> dict:
        return self.send_command("create_box", {
            "length": length, "width": width, "height": height, "name": name
        })
        
    def create_sphere(self, radius: float = 5, name: str = "Sphere") -> dict:
        return self.send_command("create_sphere", {"radius": radius, "name": name})
        
    def create_cylinder(self, radius: float = 5, height: float = 10, 
                        name: str = "Cylinder") -> dict:
        return self.send_command("create_cylinder", {
            "radius": radius, "height": height, "name": name
        })
        
    def list_objects(self) -> dict:
        return self.send_command("list_objects")
        
    def boolean_union(self, obj1: str, obj2: str, name: str = "Union") -> dict:
        return self.send_command("boolean_union", {
            "object1": obj1, "object2": obj2, "name": name
        })
        
    def boolean_subtract(self, base: str, tool: str, name: str = "Subtract") -> dict:
        return self.send_command("boolean_subtract", {
            "base": base, "tool": tool, "name": name
        })
        
    def export_step(self, filepath: str, objects: list = None) -> dict:
        return self.send_command("export_step", {
            "filepath": filepath, "objects": objects
        })
        
    def export_stl(self, filepath: str, objects: list = None) -> dict:
        return self.send_command("export_stl", {
            "filepath": filepath, "objects": objects
        })


def run_tests(client: FreeCADTestClient):
    """Run integration tests."""
    print("\n" + "=" * 50)
    print("Running Tests")
    print("=" * 50 + "\n")
    
    tests_passed = 0
    tests_failed = 0
    
    def test(name: str, func, expected_status: str = "success"):
        nonlocal tests_passed, tests_failed
        print(f"[Test] {name}...")
        try:
            result = func()
            status = result.get("status", "success" if "result" in result else "error")
            if status == expected_status or "result" in result:
                print(f"  Result: {result}")
                print("  ✓ Passed\n")
                tests_passed += 1
                return result
            else:
                print(f"  Result: {result}")
                print("  ✗ Failed\n")
                tests_failed += 1
                return None
        except Exception as e:
            print(f"  Error: {e}")
            print("  ✗ Failed\n")
            tests_failed += 1
            return None
    
    # Test 1: Ping
    test("Ping", client.ping)
    
    # Test 2: Get Version
    test("Get Version", client.get_version)
    
    # Test 3: List Methods
    result = test("List Methods", client.list_methods)
    if result and "result" in result:
        methods = result["result"]
        print(f"  Available methods: {methods[:5]}...\n")
    
    # Test 4: New Document
    test("New Document", lambda: client.new_document("TestDoc"))
    
    # Test 5: Create Box
    test("Create Box", lambda: client.create_box(10, 10, 10, "TestBox"))
    
    # Test 6: Create Sphere
    test("Create Sphere", lambda: client.create_sphere(5, "TestSphere"))
    
    # Test 7: Create Cylinder
    test("Create Cylinder", lambda: client.create_cylinder(3, 15, "TestCylinder"))
    
    # Test 8: List Objects
    result = test("List Objects", client.list_objects)
    if result and "result" in result:
        objects = result["result"].get("objects", [])
        print(f"  Objects: {[o['name'] for o in objects]}\n")
    
    # Test 9: Boolean Union
    test("Boolean Union", lambda: client.boolean_union("TestBox", "TestSphere", "UnionResult"))
    
    # Test 10: Boolean Subtract
    test("Boolean Subtract", lambda: client.boolean_subtract("TestCylinder", "TestSphere", "SubtractResult"))
    
    # Test 11: Export STEP
    test("Export STEP", lambda: client.export_step("/tmp/test_export.step"))
    
    # Test 12: Export STL
    test("Export STL", lambda: client.export_stl("/tmp/test_export.stl"))
    
    # Summary
    print("=" * 50)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 50)
    
    return tests_failed == 0


def main():
    parser = argparse.ArgumentParser(description='FreeCAD Test Client')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=9877, help='Server port')
    args = parser.parse_args()
    
    client = FreeCADTestClient(host=args.host, port=args.port)
    
    if not client.connect():
        sys.exit(1)
        
    try:
        success = run_tests(client)
        sys.exit(0 if success else 1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
