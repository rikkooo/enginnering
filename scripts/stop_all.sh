#!/bin/bash
# Stop all 3DM-API services

echo "Stopping 3DM-API Services..."

# Stop FastAPI
pkill -f "uvicorn api.main:app" 2>/dev/null && echo "Stopped FastAPI" || echo "FastAPI not running"

# Stop Blender server
pkill -f "blender.*start_server" 2>/dev/null && echo "Stopped Blender server" || echo "Blender server not running"

# Stop FreeCAD server
pkill -f "FreeCADCmd" 2>/dev/null && echo "Stopped FreeCAD server" || echo "FreeCAD server not running"

echo "All services stopped."
