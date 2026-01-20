"""
Blender Primitives Tests

Tests for Blender primitive creation endpoints.
"""

import pytest


class TestBlenderPrimitives:
    """Test Blender primitive creation."""
    
    def test_create_cube(self, api_client):
        """Test creating a cube."""
        response = api_client.post("/api/v1/blender/primitives/cube", json={
            "size": 2.0,
            "name": "TestCube"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
        
    def test_create_sphere(self, api_client):
        """Test creating a sphere."""
        response = api_client.post("/api/v1/blender/primitives/sphere", json={
            "radius": 1.5,
            "name": "TestSphere"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_cylinder(self, api_client):
        """Test creating a cylinder."""
        response = api_client.post("/api/v1/blender/primitives/cylinder", json={
            "radius": 1.0,
            "depth": 3.0,
            "name": "TestCylinder"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_with_location(self, api_client):
        """Test creating primitive with custom location."""
        response = api_client.post("/api/v1/blender/primitives/cube", json={
            "size": 1.0,
            "location": [5, 5, 5],
            "name": "LocatedCube"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        result = data.get("result", {})
        if "location" in result:
            assert result["location"] == [5.0, 5.0, 5.0]
            
    def test_create_cone(self, api_client):
        """Test creating a cone."""
        response = api_client.post("/api/v1/blender/primitives/cone", json={
            "radius1": 1.0,
            "radius2": 0.0,
            "depth": 2.0,
            "name": "TestCone"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_torus(self, api_client):
        """Test creating a torus."""
        response = api_client.post("/api/v1/blender/primitives/torus", json={
            "major_radius": 1.0,
            "minor_radius": 0.25,
            "name": "TestTorus"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_create_plane(self, api_client):
        """Test creating a plane."""
        response = api_client.post("/api/v1/blender/primitives/plane", json={
            "size": 5.0,
            "name": "TestPlane"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
