"""
Full Workflow Integration Tests

End-to-end tests for complete workflows.
"""

import pytest
import os


class TestBlenderWorkflow:
    """Test complete Blender workflow."""
    
    def test_create_scene_and_render(self, api_client):
        """Test creating a scene with objects and rendering."""
        # Create objects
        response = api_client.post("/api/v1/blender/primitives/cube", json={
            "size": 2.0, "name": "WorkflowCube", "location": [0, 0, 0]
        })
        assert response.status_code == 200
        assert response.json().get("status") == "success"
        
        response = api_client.post("/api/v1/blender/primitives/sphere", json={
            "radius": 1.0, "name": "WorkflowSphere", "location": [3, 0, 0]
        })
        assert response.status_code == 200
        assert response.json().get("status") == "success"
        
        # Get scene info
        response = api_client.get("/api/v1/blender/scene")
        assert response.status_code == 200
        
    def test_api_to_blender_response(self, api_client):
        """Test full API to Blender round trip."""
        # Create object
        response = api_client.post("/api/v1/blender/primitives/cube", json={
            "name": "RoundTripCube"
        })
        assert response.status_code == 200
        
        # Get object
        response = api_client.get("/api/v1/blender/objects/RoundTripCube")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # List objects
        response = api_client.get("/api/v1/blender/objects")
        assert response.status_code == 200


class TestFreeCADWorkflow:
    """Test complete FreeCAD workflow."""
    
    def test_create_parts_boolean_export(self, api_client):
        """Test creating parts, boolean ops, and export."""
        # Create box
        response = api_client.post("/api/v1/freecad/primitives/box", json={
            "length": 20, "width": 20, "height": 20, "name": "WFBox"
        })
        assert response.json()["status"] == "success"
        
        # Create sphere
        response = api_client.post("/api/v1/freecad/primitives/sphere", json={
            "radius": 12, "name": "WFSphere"
        })
        assert response.json()["status"] == "success"
        
        # Boolean subtract
        response = api_client.post("/api/v1/freecad/boolean/subtract", json={
            "base": "WFBox", "tool": "WFSphere", "name": "WFResult"
        })
        assert response.json()["status"] == "success"
        
        # Export to STEP
        response = api_client.post("/api/v1/freecad/export", json={
            "filepath": "/tmp/workflow_test.step", "format": "STEP"
        })
        assert response.json()["status"] == "success"
        
    def test_api_to_freecad_response(self, api_client):
        """Test full API to FreeCAD round trip."""
        # Create object
        response = api_client.post("/api/v1/freecad/primitives/box", json={
            "name": "FCRoundTrip", "length": 10, "width": 10, "height": 10
        })
        assert response.status_code == 200
        
        # Get object
        response = api_client.get("/api/v1/freecad/objects/FCRoundTrip")
        assert response.status_code == 200
        
        # List objects
        response = api_client.get("/api/v1/freecad/objects")
        assert response.status_code == 200


class TestCrossService:
    """Test cross-service operations."""
    
    def test_health_all_services(self, api_client):
        """Test health endpoints for all services."""
        response = api_client.get("/health")
        assert response.json()["status"] == "healthy"
        
        response = api_client.get("/health/blender")
        assert response.json()["status"] == "connected"
        
        response = api_client.get("/health/freecad")
        assert response.json()["status"] == "connected"
        
    def test_version_info(self, api_client):
        """Test version endpoint."""
        response = api_client.get("/version")
        data = response.json()
        assert "api_version" in data
