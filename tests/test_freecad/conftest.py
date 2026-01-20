"""
FreeCAD Test Fixtures

Pytest fixtures for FreeCAD tests.
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
def freecad_available(api_client):
    """Check if FreeCAD server is available."""
    try:
        response = api_client.get("/health/freecad")
        return response.json().get("status") == "connected"
    except:
        return False


@pytest.fixture(autouse=True)
def skip_if_freecad_unavailable(request, freecad_available):
    """Skip test if FreeCAD is not available."""
    if not freecad_available and "freecad" in request.node.name:
        pytest.skip("FreeCAD server not available")
