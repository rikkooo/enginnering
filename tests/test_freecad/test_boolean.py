"""
FreeCAD Boolean Tests

Tests for FreeCAD boolean operations.
"""

import pytest


class TestFreeCADBoolean:
    """Test FreeCAD boolean operations."""
    
    def test_boolean_union(self, api_client):
        """Test boolean union."""
        # Create two objects
        api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 10, "width": 10, "height": 10, "name": "UnionBox1"
        })
        api_client.post("/api/v1/freecad/primitives/sphere", json={
            "radius": 8, "name": "UnionSphere1"
        })
        
        # Perform union
        response = api_client.post("/api/v1/freecad/boolean/union", json={
            "object1": "UnionBox1",
            "object2": "UnionSphere1",
            "name": "UnionResult"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_boolean_subtract(self, api_client):
        """Test boolean subtraction."""
        # Create objects
        api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 15, "width": 15, "height": 15, "name": "SubBase"
        })
        api_client.post("/api/v1/freecad/primitives/sphere", json={
            "radius": 10, "name": "SubTool"
        })
        
        # Perform subtract
        response = api_client.post("/api/v1/freecad/boolean/subtract", json={
            "base": "SubBase",
            "tool": "SubTool",
            "name": "SubResult"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_boolean_intersect(self, api_client):
        """Test boolean intersection."""
        # Create objects
        api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 10, "width": 10, "height": 10, "name": "IntBox"
        })
        api_client.post("/api/v1/freecad/primitives/sphere", json={
            "radius": 8, "name": "IntSphere"
        })
        
        # Perform intersect
        response = api_client.post("/api/v1/freecad/boolean/intersect", json={
            "object1": "IntBox",
            "object2": "IntSphere",
            "name": "IntResult"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
