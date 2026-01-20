# API Reference

Complete API documentation for 3DM-API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (local development).

---

## Health Endpoints

### GET /health
Check API health status.

**Response:**
```json
{"status": "healthy", "api_version": "1.0.0"}
```

### GET /health/blender
Check Blender server connection.

### GET /health/freecad
Check FreeCAD server connection.

### GET /version
Get version information for all services.

---

## Blender Endpoints

### Primitives

#### POST /api/v1/blender/primitives/cube
Create a cube mesh.

**Request:**
```json
{
  "size": 2.0,
  "location": [0, 0, 0],
  "name": "MyCube"
}
```

#### POST /api/v1/blender/primitives/sphere
Create a UV sphere.

**Request:**
```json
{
  "radius": 1.0,
  "segments": 32,
  "location": [0, 0, 0],
  "name": "MySphere"
}
```

#### POST /api/v1/blender/primitives/cylinder
Create a cylinder.

**Request:**
```json
{
  "radius": 1.0,
  "depth": 2.0,
  "location": [0, 0, 0],
  "name": "MyCylinder"
}
```

#### POST /api/v1/blender/primitives/cone
Create a cone.

#### POST /api/v1/blender/primitives/torus
Create a torus.

#### POST /api/v1/blender/primitives/plane
Create a plane.

### Objects

#### GET /api/v1/blender/objects
List all objects in the scene.

#### GET /api/v1/blender/objects/{name}
Get object details by name.

#### DELETE /api/v1/blender/objects/{name}
Delete an object.

#### PATCH /api/v1/blender/objects/{name}
Transform an object.

**Request:**
```json
{
  "location": [1, 2, 3],
  "rotation": [0, 0, 1.57],
  "scale": [1, 1, 1]
}
```

### Materials

#### POST /api/v1/blender/materials
Create a new material.

**Request:**
```json
{
  "name": "RedMetal",
  "color": [1.0, 0.0, 0.0, 1.0],
  "metallic": 0.8,
  "roughness": 0.2
}
```

#### POST /api/v1/blender/materials/apply
Apply material to object.

**Request:**
```json
{
  "object_name": "MyCube",
  "material_name": "RedMetal"
}
```

### Scene

#### GET /api/v1/blender/scene
Get scene information.

#### DELETE /api/v1/blender/scene
Clear all objects from scene.

#### POST /api/v1/blender/camera
Add a camera.

**Request:**
```json
{
  "location": [7, -7, 5],
  "rotation": [1.1, 0, 0.8],
  "name": "MainCamera"
}
```

#### POST /api/v1/blender/light
Add a light.

**Request:**
```json
{
  "light_type": "SUN",
  "location": [5, 5, 10],
  "energy": 5.0,
  "name": "MainLight"
}
```

### Rendering

#### POST /api/v1/blender/render
Render the scene.

**Request:**
```json
{
  "output_path": "/tmp/render.png",
  "resolution_x": 1920,
  "resolution_y": 1080,
  "engine": "CYCLES",
  "samples": 128
}
```

### Export

#### POST /api/v1/blender/export
Export scene to file.

**Request:**
```json
{
  "filepath": "/tmp/model.glb",
  "format": "GLB",
  "objects": ["Cube", "Sphere"]
}
```

---

## FreeCAD Endpoints

### Documents

#### GET /api/v1/freecad/documents
List open documents.

#### POST /api/v1/freecad/documents
Create new document.

### Primitives

#### POST /api/v1/freecad/primitives/box
Create a box.

**Request:**
```json
{
  "length": 10.0,
  "width": 10.0,
  "height": 10.0,
  "name": "MyBox"
}
```

#### POST /api/v1/freecad/primitives/sphere
Create a sphere.

#### POST /api/v1/freecad/primitives/cylinder
Create a cylinder.

#### POST /api/v1/freecad/primitives/cone
Create a cone.

#### POST /api/v1/freecad/primitives/torus
Create a torus.

### Objects

#### GET /api/v1/freecad/objects
List all objects.

#### GET /api/v1/freecad/objects/{name}
Get object details.

#### DELETE /api/v1/freecad/objects/{name}
Delete an object.

### Boolean Operations

#### POST /api/v1/freecad/boolean/union
Boolean union of two objects.

**Request:**
```json
{
  "object1": "Box",
  "object2": "Sphere",
  "name": "UnionResult"
}
```

#### POST /api/v1/freecad/boolean/subtract
Boolean subtraction.

**Request:**
```json
{
  "base": "Box",
  "tool": "Sphere",
  "name": "SubtractResult"
}
```

#### POST /api/v1/freecad/boolean/intersect
Boolean intersection.

### Export

#### POST /api/v1/freecad/export
Export to file.

**Request:**
```json
{
  "filepath": "/tmp/part.step",
  "format": "STEP",
  "objects": ["Box"]
}
```

---

## WebSocket Endpoints

### WS /ws/blender
WebSocket for Blender real-time operations.

**Message Types:**
- `ping` - Keep-alive
- `execute` - Run Python code
- `command` - Send JSON-RPC command

### WS /ws/freecad
WebSocket for FreeCAD real-time operations.

---

## Response Format

### Success
```json
{
  "status": "success",
  "result": { ... }
}
```

### Error
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```
