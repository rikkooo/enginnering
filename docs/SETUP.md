# Setup Guide

Complete installation and setup instructions for 3DM-API.

## Prerequisites

- **Python 3.10+**
- **Blender 4.0+** (for Blender operations)
- **FreeCAD 1.0+** (for CAD operations)
- **Linux** (tested on Ubuntu 22.04+)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rikkooo/enginnering.git
cd enginnering
```

### 2. Install Python Dependencies

```bash
pip install -r api/requirements.txt
pip install -r tests/requirements.txt
```

### 3. Install Blender

**Ubuntu/Debian (snap):**
```bash
sudo snap install blender --classic
```

**Verify installation:**
```bash
blender --version
```

### 4. Install FreeCAD

**Ubuntu/Debian (snap):**
```bash
sudo snap install freecad
```

**Verify installation:**
```bash
/snap/bin/freecad.cmd -c "import FreeCAD; print(FreeCAD.Version())"
```

## Starting Services

### Option 1: Start All Services

```bash
./scripts/start_all.sh
```

This starts:
- Blender server on port 9876
- FreeCAD server on port 9877
- FastAPI gateway on port 8000

### Option 2: Start Services Individually

**Blender Server:**
```bash
blender -b -P src/blender/scripts/start_server.py -- --port 9876
```

**FreeCAD Server:**
```bash
/snap/bin/freecad.cmd -c "exec(open('src/freecad/scripts/start_server.py').read())"
```

**FastAPI Gateway:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Verify Installation

### Health Check

```bash
./scripts/health_check.sh
```

Or manually:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/blender
curl http://localhost:8000/health/freecad
```

### API Documentation

Open in browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` to customize:
- `TDM_API_PORT` - API gateway port (default: 8000)
- `TDM_BLENDER_PORT` - Blender server port (default: 9876)
- `TDM_FREECAD_PORT` - FreeCAD server port (default: 9877)

## Stopping Services

```bash
./scripts/stop_all.sh
```

## Troubleshooting

### Blender won't start
- Ensure Blender is installed: `which blender`
- Check if port 9876 is in use: `ss -tlnp | grep 9876`

### FreeCAD won't start
- Ensure FreeCAD snap is installed: `snap list | grep freecad`
- Check snap connections: `snap connections freecad`

### API returns connection errors
- Verify backend servers are running: `./scripts/health_check.sh`
- Check server logs: `cat /tmp/blender_server.log`
