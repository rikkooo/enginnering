#!/bin/bash
# Start the FastAPI gateway

cd "$(dirname "$0")/.."

# Install dependencies if needed
pip install -q -r api/requirements.txt

# Start uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
