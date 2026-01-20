# 🛠️ 3DM-API: Blender & FreeCAD Local API

> AI-powered 3D modeling through efficient local APIs — no MCP overhead

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 Overview

**3DM-API** is a unified local API system for controlling **Blender** and **FreeCAD** programmatically. Designed for AI agent integration, it enables creating, manipulating, and rendering 3D shapes through simple REST/WebSocket calls.

### Why Local APIs Instead of MCP?

| Aspect | MCP Servers | 3DM-API (Local) |
|--------|-------------|-----------------|
| **Latency** | Higher (LLM reasoning layer) | Lower (direct calls) |
| **Determinism** | LLM may vary | Fully deterministic |
| **Complexity** | MCP client + server + tools | Simple REST/WebSocket |
| **Performance** | Protocol overhead | Minimal overhead |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI AGENT                                 │
│              (Claude, GPT, Local LLM, Your Code)                │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP REST + WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    3DM-API GATEWAY                               │
│                   FastAPI + WebSocket                            │
│                     Port 8000                                    │
└───────────────┬─────────────────────────────┬───────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌─────────────────────────────────┐
│      BLENDER ENGINE       │   │       FREECAD ENGINE            │
│    (Headless Instance)    │   │     (Headless Instance)         │
│      Socket :9876         │   │       Socket :9877              │
└───────────────────────────┘   └─────────────────────────────────┘
```

---

## ✨ Features

### Blender Integration
- 🔷 **Mesh Primitives** — Cube, Sphere, Cylinder, Cone, Torus, Plane
- 🎨 **Materials** — Create, apply, modify colors and properties
- 💡 **Lighting** — Point, Sun, Spot lights
- 📷 **Cameras** — Setup and positioning
- 🖼️ **Rendering** — Cycles & EEVEE engines
- 📦 **Export** — GLB, FBX, OBJ, STL

### FreeCAD Integration
- 🔷 **Part Primitives** — Box, Sphere, Cylinder, Cone, Torus
- ⚙️ **Boolean Operations** — Union, Subtract, Intersect
- 📐 **Parametric Modeling** — Precise dimensions
- 📦 **Export** — STEP, IGES, STL, BREP

### API Features
- 🚀 **REST Endpoints** — Simple HTTP calls for common operations
- 🔌 **WebSocket** — Real-time code execution and streaming
- 📚 **Auto Documentation** — Swagger UI at `/docs`
- 🤖 **AI Ready** — OpenAI & Anthropic function schemas included

---

## 📁 Project Structure

```
eng/
├── plan/                        # Planning documents
│   ├── BLENDER_FREECAD_API_RESEARCH.md
│   ├── MASTER_PLAN.md
│   ├── STAGE_1_PLAN.md         # Blender Socket Addon
│   ├── STAGE_2_PLAN.md         # FreeCAD Socket Server
│   ├── STAGE_3_PLAN.md         # FastAPI Gateway
│   ├── STAGE_4_PLAN.md         # AI Integration & Testing
│   └── WSTODO_STAGE*.txt       # Task tracking files
│
├── src/                         # Source code
│   ├── blender/                 # Blender addon ✅
│   │   ├── addon/              # Socket server addon
│   │   └── scripts/            # Startup scripts
│   ├── freecad/                 # FreeCAD server (Stage 2)
│   └── common/                  # Shared utilities ✅
│
├── api/                         # FastAPI gateway (Stage 3)
│
├── tests/                       # Test suite ✅
│
├── ai/                          # AI schemas & examples (coming soon)
│
├── docs/                        # Documentation (coming soon)
│
├── README.md                    # This file
└── CHANGELOG.md                 # Version history
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Blender 4.0+ (5.0.1 tested)
- FreeCAD 0.21+ (Stage 2)

### Installation

```bash
# Clone the repository
git clone https://github.com/rikkooo/enginnering.git
cd enginnering

# Start Blender server (headless)
blender -b -P src/blender/scripts/start_server.py -- --port 9876
```

### Usage Example

```python
import requests

# Create a cube in Blender
response = requests.post("http://localhost:8000/api/v1/blender/primitives/cube", json={
    "location": [0, 0, 0],
    "size": 2,
    "name": "MyCube"
})
print(response.json())

# Create a box in FreeCAD
response = requests.post("http://localhost:8000/api/v1/freecad/primitives/box", json={
    "length": 10,
    "width": 10,
    "height": 10,
    "name": "MyBox"
})
print(response.json())

# Render the Blender scene
response = requests.post("http://localhost:8000/api/v1/blender/render", json={
    "output": "/tmp/render.png",
    "engine": "CYCLES"
})
print(response.json())
```

---

## 📋 Roadmap

| Stage | Description | Status |
|-------|-------------|--------|
| **1** | Blender Socket Addon | ✅ Complete |
| **2** | FreeCAD Socket Server | ✅ Complete |
| **3** | FastAPI Gateway | 📝 Planned |
| **4** | AI Integration & Testing | 📝 Planned |

See detailed plans in the `plan/` folder.

---

## 🤖 AI Integration

The project includes ready-to-use function schemas for:

- **OpenAI** — Function calling format
- **Anthropic** — Tool use format

Example with OpenAI:

```python
from openai import OpenAI
import json

client = OpenAI()

# Load function schemas
with open("ai/schemas/openai_functions.json") as f:
    functions = json.load(f)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Create a red cube at position (1, 2, 3)"}],
    functions=functions,
    function_call="auto"
)
```

---

## 📖 Documentation

- [Research Report](plan/BLENDER_FREECAD_API_RESEARCH.md) — Full technical analysis
- [Master Plan](plan/MASTER_PLAN.md) — Project roadmap
- [API Reference](docs/API.md) — Endpoint documentation (coming soon)
- [Setup Guide](docs/SETUP.md) — Installation instructions (coming soon)

---

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Blender](https://www.blender.org/) — Open source 3D creation suite
- [FreeCAD](https://www.freecad.org/) — Open source parametric CAD
- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- Inspired by [blender-mcp](https://github.com/ahujasid/blender-mcp) and [blender-remote](https://github.com/igamenovoer/blender-remote)

---

<p align="center">
  Made with ❤️ for the AI + 3D community
</p>
