"""
FreeCAD Primitives Tests

Tests for FreeCAD primitive creation endpoints.
"""

import pytest


class TestFreeCADPrimitives:
    """Test FreeCAD primitive creation."""
    
    def test_create_box(self, api_client):
        """Test creating a box."""
        response = api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "name": "TestBox"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_sphere(self, api_client):
        """Test creating a sphere."""
        response = api_client.post("/api/v1/freecad/primitives/sphere", json={
            "radius": 5.0,
            "name": "TestSphere"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_cylinder(self, api_client):
        """Test creating a cylinder."""
        response = api_client.post("/api/v1/freecad/primitives/cylinder", json={
            "radius": 3.0,
            "depth": 10.0,
            "name": "TestCylinder"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_with_dimensions(self, api_client):
        """Test creating box with specific dimensions."""
        response = api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 20.0,
            "width": 15.0,
            "height": 5.0,
            "name": "DimensionBox"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        result = data.get("result", {})
        dims = result.get("dimensions", {})
        if dims:
            assert dims.get("length") == 20.0
            assert dims.get("width") == 15.0
            assert dims.get("height") == 5.0
