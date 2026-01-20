"""
Integration Test Fixtures

Pytest fixtures for integration tests.
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
    with httpx.Client(base_url=API_BASE, timeout=60.0, proxy=None) as client:
        yield client


@pytest.fixture
def services_available(api_client):
    """Check if all services are available."""
    try:
        health = api_client.get("/health").json()
        blender = api_client.get("/health/blender").json()
        freecad = api_client.get("/health/freecad").json()
        return (
            health.get("status") == "healthy" and
            blender.get("status") == "connected" and
            freecad.get("status") == "connected"
        )
    except:
        return False


@pytest.fixture(autouse=True)
def skip_if_services_unavailable(request, services_available):
    """Skip integration tests if services are not available."""
    if not services_available:
        pytest.skip("Required services not available")
