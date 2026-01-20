"""
Blender Materials Tests

Tests for Blender material operations.
"""

import pytest


class TestBlenderMaterials:
    """Test Blender material operations."""
    
    def test_create_material(self, api_client):
        """Test creating a material."""
        response = api_client.post("/api/v1/blender/materials", json={
            "name": "TestMaterial",
            "color": [1.0, 0.0, 0.0, 1.0],
            "metallic": 0.5,
            "roughness": 0.3
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_apply_material(self, api_client):
        """Test applying material to object."""
        # First create an object
        api_client.post("/api/v1/blender/primitives/cube", json={
            "name": "MatTestCube"
        })
        
        # Create material
        api_client.post("/api/v1/blender/materials", json={
            "name": "ApplyTestMat",
            "color": [0.0, 1.0, 0.0, 1.0]
        })
        
        # Apply material
        response = api_client.post("/api/v1/blender/materials/apply", json={
            "object_name": "MatTestCube",
            "material_name": "ApplyTestMat"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
    def test_material_with_metallic(self, api_client):
        """Test creating metallic material."""
        response = api_client.post("/api/v1/blender/materials", json={
            "name": "MetalMaterial",
            "color": [0.8, 0.8, 0.8, 1.0],
            "metallic": 1.0,
            "roughness": 0.1
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
