#!/bin/bash
# Start all 3DM-API services

cd "$(dirname "$0")/.."

echo "Starting 3DM-API Services..."
echo "=============================="

# Start Blender server
echo "Starting Blender server on port 9876..."
nohup blender -b -P src/blender/scripts/start_server.py -- --port 9876 > /tmp/blender_server.log 2>&1 &
BLENDER_PID=$!
echo "Blender PID: $BLENDER_PID"

# Start FreeCAD server
echo "Starting FreeCAD server on port 9877..."
nohup /snap/bin/freecad.cmd -c "exec(open('src/freecad/scripts/start_server.py').read())" > /tmp/freecad_server.log 2>&1 &
FREECAD_PID=$!
echo "FreeCAD PID: $FREECAD_PID"

# Wait for servers to start
sleep 5

# Start FastAPI gateway
echo "Starting FastAPI gateway on port 8000..."
pip install -q -r api/requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Cleanup on exit
trap "kill $BLENDER_PID $FREECAD_PID 2>/dev/null" EXIT
