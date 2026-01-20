#!/bin/bash
# Health check for all 3DM-API services

echo "3DM-API Health Check"
echo "===================="

# Check Blender server
echo -n "Blender server (9876): "
if ss -tlnp | grep -q ":9876"; then
    echo "✓ Running"
else
    echo "✗ Not running"
fi

# Check FreeCAD server
echo -n "FreeCAD server (9877): "
if ss -tlnp | grep -q ":9877"; then
    echo "✓ Running"
else
    echo "✗ Not running"
fi

# Check FastAPI gateway
echo -n "FastAPI gateway (8000): "
if ss -tlnp | grep -q ":8000"; then
    echo "✓ Running"
    # Test health endpoint
    HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
    if [ -n "$HEALTH" ]; then
        echo "  Health: $HEALTH"
    fi
else
    echo "✗ Not running"
fi
