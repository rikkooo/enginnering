# Blender & FreeCAD API Control Research Report

**Date:** January 20, 2026  
**Objective:** Develop local APIs for AI-assisted 3D modeling and rendering with Blender and FreeCAD

---

## Executive Summary

This report analyzes approaches for programmatically controlling **Blender** and **FreeCAD** through local APIs, enabling AI agents to create and render 3D shapes. We evaluate existing solutions (MCP servers) for inspiration while recommending a more efficient **local REST/WebSocket API architecture** that avoids MCP overhead.

### Key Recommendations

| Aspect | Recommendation |
|--------|----------------|
| **Architecture** | FastAPI + WebSocket hybrid for both apps |
| **Communication** | JSON-RPC over WebSocket (real-time) + REST endpoints (simple ops) |
| **Execution Mode** | Headless/background mode for automation |
| **Protocol** | Custom lightweight protocol inspired by MCP but without its overhead |

---

## Part 1: Blender API Capabilities

### 1.1 Native Python API (`bpy`)

Blender has a **comprehensive Python API** (`bpy` module) that provides access to virtually all functionality:

```python
import bpy

# Create primitives
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=2)
bpy.ops.mesh.primitive_sphere_add(location=(3, 0, 0), radius=1)
bpy.ops.mesh.primitive_cylinder_add(location=(6, 0, 0), radius=1, depth=2)

# Modify objects
obj = bpy.context.active_object
obj.scale = (1.5, 1.5, 1.5)
obj.rotation_euler = (0.5, 0.3, 0)

# Apply materials
mat = bpy.data.materials.new(name="RedMaterial")
mat.diffuse_color = (1, 0, 0, 1)
obj.data.materials.append(mat)

# Render
bpy.context.scene.render.filepath = "/tmp/render.png"
bpy.ops.render.render(write_still=True)
```

### 1.2 Headless Mode

Blender can run **without GUI** using the `-b` (background) flag:

```bash
# Run script headlessly
blender -b -P my_script.py

# Render a scene headlessly
blender -b scene.blend -o //output -F PNG -f 1

# With custom arguments
blender -b -P script.py -- --custom-arg value
```

**Key capabilities in headless mode:**
- Full Python API access
- All rendering engines (Cycles, EEVEE)
- Import/export all formats (OBJ, FBX, GLTF, STL)
- No display required (ideal for servers/Docker)

### 1.3 Remote Control Options

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| **Socket Server** | TCP socket inside Blender addon | Real-time, bidirectional | Requires addon installation |
| **HTTP Server** | Flask/FastAPI inside Blender | Standard REST interface | Limited by Blender's threading |
| **File-based** | Watch folder for commands | Simple | Slow, no real-time feedback |
| **blender-remote** | Existing package | Ready to use | MCP-oriented design |

### 1.4 Existing Solutions Analysis

#### blender-mcp (ahujasid)
- **Architecture:** Blender addon (socket server) + MCP server (Python)
- **Protocol:** JSON over TCP sockets
- **Features:** Object manipulation, materials, scene inspection, code execution
- **Limitation:** MCP overhead, designed for LLM integration only

#### blender-remote (igamenovoer)
- **Architecture:** Python client + Blender addon
- **Features:** Background/GUI modes, GLB export, scene management
- **API Example:**
```python
from blender_remote.client import BlenderMCPClient
from blender_remote.scene_manager import BlenderSceneManager

client = BlenderMCPClient()
scene_manager = BlenderSceneManager(client)
scene_manager.add_cube(location=(0, 0, 0), name="MyCube")
```

#### blenderless (oqton)
- **Purpose:** Easy headless rendering
- **Approach:** Python wrapper around Blender CLI
- **Use case:** Batch rendering, thumbnails, GIF animations

---

## Part 2: FreeCAD API Capabilities

### 2.1 Native Python API

FreeCAD is **built from scratch to be Python-controlled**. Two main modules:

- **`FreeCAD` (App):** Core functionality, documents, objects
- **`FreeCADGui` (Gui):** GUI elements (not available in headless mode)

```python
import FreeCAD
import Part

# Create a new document
doc = FreeCAD.newDocument("MyDoc")

# Create primitives using Part module
box = Part.makeBox(10, 10, 10)
sphere = Part.makeSphere(5)
cylinder = Part.makeCylinder(3, 10)

# Add to document
obj = doc.addObject("Part::Feature", "MyBox")
obj.Shape = box

# Boolean operations
fused = box.fuse(sphere)
cut = box.cut(cylinder)

# Export
Part.export([obj], "/tmp/output.step")
doc.saveAs("/tmp/model.FCStd")
```

### 2.2 Part Module - Shape Creation Functions

| Function | Description |
|----------|-------------|
| `Part.makeBox(l, w, h)` | Create box |
| `Part.makeSphere(radius)` | Create sphere |
| `Part.makeCylinder(r, h)` | Create cylinder |
| `Part.makeCone(r1, r2, h)` | Create cone |
| `Part.makeTorus(r1, r2)` | Create torus |
| `Part.makePlane(l, w)` | Create plane |
| `Part.makePolygon(points)` | Create polygon from points |
| `Part.makeHelix(pitch, height, radius)` | Create helix |

### 2.3 Headless Mode

FreeCAD provides a dedicated headless executable:

```bash
# Console mode (headless)
freecadcmd script.py

# Or with main executable
freecad --console script.py

# Run specific macro
freecad -c "exec(open('script.py').read())"
```

**Headless limitations:**
- `FreeCADGui` module unavailable
- Some workbenches may have GUI dependencies
- Rendering requires additional setup (no native render engine like Blender)

### 2.4 Existing Solutions Analysis

#### FreeCAD MCP (FastMCP)
- **Features:** RPC server for programmatic control
- **Operations:** Create documents, insert parts, edit objects, execute Python
- **Protocol:** JSON-RPC style

---

## Part 3: MCP vs Local API - Why Local is Better

### 3.1 MCP Limitations

| Issue | Impact |
|-------|--------|
| **Protocol overhead** | Extra serialization/deserialization layers |
| **Latency** | MCP adds reasoning layer that introduces delay |
| **Complexity** | Requires MCP client, server, and tool definitions |
| **LLM dependency** | Designed for LLM tool discovery, overkill for direct API |
| **Non-deterministic** | LLM may misinterpret tool usage |

### 3.2 Local API Advantages

| Benefit | Description |
|---------|-------------|
| **Direct control** | No intermediary reasoning layer |
| **Lower latency** | Direct socket/HTTP communication |
| **Deterministic** | Predictable, testable behavior |
| **Simpler** | Standard REST/WebSocket patterns |
| **Flexible** | Can be called by AI or any client |

### 3.3 Hybrid Approach (Recommended)

From research, the best practice is:
- **Local APIs** for efficient, deterministic operations
- **Skills/Prompts** for AI to understand how to use the APIs
- **No MCP layer** - AI calls APIs directly via function calling

---

## Part 4: Recommended Architecture

### 4.1 High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent / Client                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Unified API Gateway                        │
│                  (FastAPI + WebSocket)                       │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  /blender/*         │  │  /freecad/*         │          │
│  └──────────┬──────────┘  └──────────┬──────────┘          │
└─────────────┼────────────────────────┼──────────────────────┘
              │                        │
              ▼                        ▼
┌─────────────────────────┐  ┌─────────────────────────────────┐
│   Blender Instance      │  │   FreeCAD Instance              │
│   (Headless + Addon)    │  │   (Headless + Script)           │
│                         │  │                                 │
│   Socket Server :9876   │  │   Socket Server :9877           │
└─────────────────────────┘  └─────────────────────────────────┘
```

### 4.2 API Design

#### REST Endpoints (Simple Operations)

```
# Blender
POST /blender/primitives/cube      - Create cube
POST /blender/primitives/sphere    - Create sphere
POST /blender/primitives/cylinder  - Create cylinder
GET  /blender/scene                - Get scene info
POST /blender/render               - Render scene
POST /blender/export               - Export model

# FreeCAD
POST /freecad/primitives/box       - Create box
POST /freecad/primitives/sphere    - Create sphere
POST /freecad/boolean/union        - Boolean union
POST /freecad/boolean/subtract     - Boolean subtract
POST /freecad/export               - Export (STEP, STL, etc.)
```

#### WebSocket (Real-time Operations)

```json
// Execute arbitrary Python code
{
  "type": "execute",
  "target": "blender",
  "code": "bpy.ops.mesh.primitive_cube_add(location=(0,0,0))"
}

// Subscribe to scene changes
{
  "type": "subscribe",
  "target": "blender",
  "event": "scene_update"
}
```

### 4.3 Protocol Design (Inspired by MCP, Simplified)

```json
// Request
{
  "id": "req-001",
  "method": "create_primitive",
  "params": {
    "type": "cube",
    "location": [0, 0, 0],
    "size": 2,
    "name": "MyCube"
  }
}

// Response
{
  "id": "req-001",
  "status": "success",
  "result": {
    "object_id": "Cube.001",
    "vertices": 8,
    "faces": 6
  }
}

// Error
{
  "id": "req-001",
  "status": "error",
  "error": {
    "code": "INVALID_PARAMS",
    "message": "Size must be positive"
  }
}
```

### 4.4 Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **API Gateway** | FastAPI | Async, fast, auto-docs, WebSocket support |
| **Protocol** | JSON-RPC 2.0 (simplified) | Standard, lightweight |
| **Transport** | WebSocket + REST | Real-time + simple ops |
| **Blender Addon** | Python socket server | Direct bpy access |
| **FreeCAD Script** | Python socket server | Direct FreeCAD API access |
| **Process Manager** | Supervisor/systemd | Keep instances running |

---

## Part 5: Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)

1. **Blender Addon Development**
   - Socket server listening on configurable port
   - Command dispatcher for primitives, transforms, materials
   - Scene serialization (JSON export of scene state)

2. **FreeCAD Script Development**
   - Socket server with Part module integration
   - Document management
   - Export handlers (STEP, STL, IGES)

3. **FastAPI Gateway**
   - REST endpoints for common operations
   - WebSocket for code execution and streaming
   - Request validation with Pydantic

### Phase 2: Shape Operations (Week 3-4)

1. **Blender Operations**
   - All mesh primitives (cube, sphere, cylinder, cone, torus, plane)
   - Modifiers (subdivision, boolean, bevel)
   - Materials and textures
   - Camera and lighting setup
   - Rendering (Cycles/EEVEE)

2. **FreeCAD Operations**
   - All Part primitives
   - Boolean operations (fuse, cut, common)
   - Sketcher basics
   - Export formats

### Phase 3: AI Integration (Week 5-6)

1. **Function Definitions**
   - OpenAI-compatible function schemas
   - Anthropic tool definitions
   - Clear parameter descriptions

2. **Skills/Prompts**
   - Best practices for 3D modeling
   - Common workflows (e.g., "create a gear", "make a box with rounded edges")

### Phase 4: Advanced Features (Week 7-8)

1. **Batch Operations**
   - Multiple object creation
   - Scene templates

2. **Rendering Pipeline**
   - Queue management
   - Progress reporting
   - Output formats (PNG, EXR, video)

---

## Part 6: Code Examples

### 6.1 Blender Addon (Socket Server)

```python
# blender_api_addon.py
import bpy
import socket
import json
import threading

class BlenderAPIServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        
    def handle_command(self, cmd):
        method = cmd.get('method')
        params = cmd.get('params', {})
        
        if method == 'create_cube':
            bpy.ops.mesh.primitive_cube_add(
                location=tuple(params.get('location', [0,0,0])),
                size=params.get('size', 2)
            )
            obj = bpy.context.active_object
            if params.get('name'):
                obj.name = params['name']
            return {'object_id': obj.name}
            
        elif method == 'create_sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(
                location=tuple(params.get('location', [0,0,0])),
                radius=params.get('radius', 1)
            )
            return {'object_id': bpy.context.active_object.name}
            
        elif method == 'execute':
            exec(params.get('code', ''))
            return {'executed': True}
            
        elif method == 'get_scene':
            objects = []
            for obj in bpy.data.objects:
                objects.append({
                    'name': obj.name,
                    'type': obj.type,
                    'location': list(obj.location),
                    'rotation': list(obj.rotation_euler),
                    'scale': list(obj.scale)
                })
            return {'objects': objects}
            
        elif method == 'render':
            bpy.context.scene.render.filepath = params.get('output', '/tmp/render.png')
            bpy.ops.render.render(write_still=True)
            return {'output': bpy.context.scene.render.filepath}
            
        return {'error': f'Unknown method: {method}'}
    
    def start(self):
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        def accept_connections():
            while self.running:
                try:
                    client, addr = self.server.accept()
                    threading.Thread(target=self.handle_client, args=(client,)).start()
                except:
                    break
                    
        threading.Thread(target=accept_connections, daemon=True).start()
        print(f"Blender API Server running on {self.host}:{self.port}")
        
    def handle_client(self, client):
        buffer = ""
        while self.running:
            try:
                data = client.recv(4096).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        cmd = json.loads(line)
                        result = self.handle_command(cmd)
                        response = json.dumps({
                            'id': cmd.get('id'),
                            'status': 'success' if 'error' not in result else 'error',
                            'result': result
                        }) + '\n'
                        client.send(response.encode('utf-8'))
            except Exception as e:
                error_response = json.dumps({
                    'status': 'error',
                    'error': str(e)
                }) + '\n'
                client.send(error_response.encode('utf-8'))
                break
        client.close()

# Blender operator to start server
class BLENDER_OT_start_api_server(bpy.types.Operator):
    bl_idname = "blender.start_api_server"
    bl_label = "Start API Server"
    
    def execute(self, context):
        global api_server
        api_server = BlenderAPIServer()
        api_server.start()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(BLENDER_OT_start_api_server)

def unregister():
    bpy.utils.unregister_class(BLENDER_OT_start_api_server)

if __name__ == "__main__":
    register()
```

### 6.2 FreeCAD Socket Server

```python
# freecad_api_server.py
import FreeCAD
import Part
import socket
import json
import threading

class FreeCADAPIServer:
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        self.running = False
        self.doc = None
        
    def ensure_document(self):
        if self.doc is None or self.doc.Name not in FreeCAD.listDocuments():
            self.doc = FreeCAD.newDocument("APIDocument")
        return self.doc
        
    def handle_command(self, cmd):
        method = cmd.get('method')
        params = cmd.get('params', {})
        doc = self.ensure_document()
        
        if method == 'create_box':
            length = params.get('length', 10)
            width = params.get('width', 10)
            height = params.get('height', 10)
            box = Part.makeBox(length, width, height)
            obj = doc.addObject("Part::Feature", params.get('name', 'Box'))
            obj.Shape = box
            doc.recompute()
            return {'object_id': obj.Name}
            
        elif method == 'create_sphere':
            radius = params.get('radius', 5)
            sphere = Part.makeSphere(radius)
            obj = doc.addObject("Part::Feature", params.get('name', 'Sphere'))
            obj.Shape = sphere
            doc.recompute()
            return {'object_id': obj.Name}
            
        elif method == 'create_cylinder':
            radius = params.get('radius', 5)
            height = params.get('height', 10)
            cylinder = Part.makeCylinder(radius, height)
            obj = doc.addObject("Part::Feature", params.get('name', 'Cylinder'))
            obj.Shape = cylinder
            doc.recompute()
            return {'object_id': obj.Name}
            
        elif method == 'boolean_union':
            obj1 = doc.getObject(params['object1'])
            obj2 = doc.getObject(params['object2'])
            result = obj1.Shape.fuse(obj2.Shape)
            new_obj = doc.addObject("Part::Feature", params.get('name', 'Union'))
            new_obj.Shape = result
            doc.recompute()
            return {'object_id': new_obj.Name}
            
        elif method == 'boolean_subtract':
            obj1 = doc.getObject(params['object1'])
            obj2 = doc.getObject(params['object2'])
            result = obj1.Shape.cut(obj2.Shape)
            new_obj = doc.addObject("Part::Feature", params.get('name', 'Subtraction'))
            new_obj.Shape = result
            doc.recompute()
            return {'object_id': new_obj.Name}
            
        elif method == 'export':
            obj = doc.getObject(params['object_id'])
            filepath = params.get('filepath', '/tmp/export.step')
            Part.export([obj], filepath)
            return {'filepath': filepath}
            
        elif method == 'get_objects':
            objects = []
            for obj in doc.Objects:
                objects.append({
                    'name': obj.Name,
                    'type': obj.TypeId,
                    'label': obj.Label
                })
            return {'objects': objects}
            
        elif method == 'execute':
            exec(params.get('code', ''))
            return {'executed': True}
            
        return {'error': f'Unknown method: {method}'}
    
    def start(self):
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        print(f"FreeCAD API Server running on {self.host}:{self.port}")
        
        while self.running:
            try:
                client, addr = self.server.accept()
                self.handle_client(client)
            except:
                break
                
    def handle_client(self, client):
        buffer = ""
        while self.running:
            try:
                data = client.recv(4096).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        cmd = json.loads(line)
                        result = self.handle_command(cmd)
                        response = json.dumps({
                            'id': cmd.get('id'),
                            'status': 'success' if 'error' not in result else 'error',
                            'result': result
                        }) + '\n'
                        client.send(response.encode('utf-8'))
            except Exception as e:
                error_response = json.dumps({
                    'status': 'error',
                    'error': str(e)
                }) + '\n'
                client.send(error_response.encode('utf-8'))
                break
        client.close()

if __name__ == "__main__":
    server = FreeCADAPIServer()
    server.start()
```

### 6.3 FastAPI Gateway

```python
# api_gateway.py
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import socket
import json
import asyncio

app = FastAPI(title="3D Modeling API", version="1.0.0")

class BlenderClient:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        
    def send_command(self, method: str, params: dict = None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        
        cmd = json.dumps({'method': method, 'params': params or {}}) + '\n'
        sock.send(cmd.encode('utf-8'))
        
        response = sock.recv(4096).decode('utf-8')
        sock.close()
        
        return json.loads(response)

class FreeCADClient:
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        
    def send_command(self, method: str, params: dict = None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        
        cmd = json.dumps({'method': method, 'params': params or {}}) + '\n'
        sock.send(cmd.encode('utf-8'))
        
        response = sock.recv(4096).decode('utf-8')
        sock.close()
        
        return json.loads(response)

blender = BlenderClient()
freecad = FreeCADClient()

# Pydantic models
class PrimitiveParams(BaseModel):
    location: Optional[List[float]] = [0, 0, 0]
    size: Optional[float] = 2
    radius: Optional[float] = 1
    name: Optional[str] = None

class BoxParams(BaseModel):
    length: float = 10
    width: float = 10
    height: float = 10
    name: Optional[str] = None

class RenderParams(BaseModel):
    output: str = "/tmp/render.png"
    engine: Optional[str] = "CYCLES"

# Blender endpoints
@app.post("/blender/primitives/cube")
async def blender_create_cube(params: PrimitiveParams):
    return blender.send_command('create_cube', params.dict())

@app.post("/blender/primitives/sphere")
async def blender_create_sphere(params: PrimitiveParams):
    return blender.send_command('create_sphere', params.dict())

@app.get("/blender/scene")
async def blender_get_scene():
    return blender.send_command('get_scene')

@app.post("/blender/render")
async def blender_render(params: RenderParams):
    return blender.send_command('render', params.dict())

# FreeCAD endpoints
@app.post("/freecad/primitives/box")
async def freecad_create_box(params: BoxParams):
    return freecad.send_command('create_box', params.dict())

@app.post("/freecad/primitives/sphere")
async def freecad_create_sphere(params: PrimitiveParams):
    return freecad.send_command('create_sphere', params.dict())

@app.get("/freecad/objects")
async def freecad_get_objects():
    return freecad.send_command('get_objects')

# WebSocket for real-time operations
@app.websocket("/ws/{target}")
async def websocket_endpoint(websocket: WebSocket, target: str):
    await websocket.accept()
    
    client = blender if target == 'blender' else freecad
    
    while True:
        try:
            data = await websocket.receive_json()
            result = client.send_command(data.get('method'), data.get('params'))
            await websocket.send_json(result)
        except Exception as e:
            await websocket.send_json({'error': str(e)})
            break

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Part 7: Installation & Setup

### 7.1 Blender Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install blender

# Or download latest from blender.org
wget https://download.blender.org/release/Blender4.0/blender-4.0.0-linux-x64.tar.xz
tar -xf blender-4.0.0-linux-x64.tar.xz
```

### 7.2 FreeCAD Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install freecad

# Or via AppImage for latest version
wget https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD_0.21.2-Linux-x86_64.AppImage
chmod +x FreeCAD_0.21.2-Linux-x86_64.AppImage
```

### 7.3 Python Dependencies

```bash
pip install fastapi uvicorn pydantic websockets
```

### 7.4 Running the System

```bash
# Terminal 1: Start Blender with addon
blender -b --python blender_api_addon.py

# Terminal 2: Start FreeCAD server
freecadcmd freecad_api_server.py

# Terminal 3: Start API Gateway
python api_gateway.py
```

---

## Part 8: AI Integration Patterns

### 8.1 OpenAI Function Calling Schema

```json
{
  "name": "create_3d_primitive",
  "description": "Create a 3D primitive shape in Blender or FreeCAD",
  "parameters": {
    "type": "object",
    "properties": {
      "application": {
        "type": "string",
        "enum": ["blender", "freecad"],
        "description": "Which 3D application to use"
      },
      "shape": {
        "type": "string",
        "enum": ["cube", "sphere", "cylinder", "cone", "torus"],
        "description": "Type of primitive to create"
      },
      "location": {
        "type": "array",
        "items": {"type": "number"},
        "description": "XYZ coordinates for placement"
      },
      "size": {
        "type": "number",
        "description": "Size/scale of the primitive"
      },
      "name": {
        "type": "string",
        "description": "Name for the object"
      }
    },
    "required": ["application", "shape"]
  }
}
```

### 8.2 Anthropic Tool Definition

```json
{
  "name": "render_scene",
  "description": "Render the current Blender scene to an image",
  "input_schema": {
    "type": "object",
    "properties": {
      "output_path": {
        "type": "string",
        "description": "Path to save the rendered image"
      },
      "resolution": {
        "type": "object",
        "properties": {
          "width": {"type": "integer"},
          "height": {"type": "integer"}
        }
      },
      "engine": {
        "type": "string",
        "enum": ["CYCLES", "EEVEE"],
        "description": "Rendering engine to use"
      }
    },
    "required": ["output_path"]
  }
}
```

---

## Part 9: Comparison Summary

| Feature | MCP Approach | Local API Approach (Recommended) |
|---------|--------------|----------------------------------|
| **Latency** | Higher (LLM reasoning) | Lower (direct calls) |
| **Complexity** | MCP server + client + tools | Simple REST/WebSocket |
| **Determinism** | LLM may vary | Fully deterministic |
| **Flexibility** | LLM decides tool usage | Client controls flow |
| **AI Integration** | Built-in | Via function calling |
| **Debugging** | Harder (LLM in loop) | Standard API debugging |
| **Performance** | Overhead from protocol | Minimal overhead |

---

## Part 10: Conclusion & Next Steps

### Recommended Approach

1. **Build local REST/WebSocket APIs** for both Blender and FreeCAD
2. **Use FastAPI** as the unified gateway
3. **Implement socket servers** inside each application
4. **Define AI function schemas** for tool calling
5. **Skip MCP** - use direct API calls from AI agents

### Immediate Next Steps

1. Create project structure in `/home/ubuntu/devs/eng/`
2. Implement Blender addon with socket server
3. Implement FreeCAD script with socket server
4. Build FastAPI gateway
5. Test with basic primitives
6. Add AI function definitions

### Future Enhancements

- Docker containerization for both apps
- GPU rendering support
- Batch processing queue
- Real-time preview streaming
- Advanced modeling operations (boolean, modifiers)
- Material library

---

## References

1. Blender Python API Documentation: https://docs.blender.org/api/current/
2. FreeCAD Scripting Basics: https://wiki.freecad.org/FreeCAD_Scripting_Basics
3. blender-mcp GitHub: https://github.com/ahujasid/blender-mcp
4. blender-remote: https://igamenovoer.github.io/blender-remote/
5. FreeCAD Part Module: https://freecad-python-stubs.readthedocs.io/en/latest/autoapi/Part/
6. MCP vs APIs Analysis: https://www.tinybird.co/blog/mcp-vs-apis-when-to-use-which-for-ai-agent-development
7. Claude Skills vs MCP: https://intuitionlabs.ai/articles/claude-skills-vs-mcp
