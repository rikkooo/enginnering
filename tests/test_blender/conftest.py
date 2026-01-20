"""
Blender Test Fixtures

Pytest fixtures for Blender tests.
"""

import pytest
import httpx
import os

API_BASE = "http://localhost:8000"

# Disable proxy for local tests
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('ALL_PROXY', None)
os.environ.pop('all_proxy', None)


@pytest.fixture
def api_client():
    """HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE, timeout=30.0, proxy=None) as client:
        yield client


@pytest.fixture
def blender_available(api_client):
    """Check if Blender server is available."""
    try:
        response = api_client.get("/health/blender")
        return response.json().get("status") == "connected"
    except:
        return False


@pytest.fixture(autouse=True)
def skip_if_blender_unavailable(request, blender_available):
    """Skip test if Blender is not available."""
    if not blender_available and "blender" in request.node.name:
        pytest.skip("Blender server not available")
