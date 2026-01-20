# 📦 Stage 3 Plan: FastAPI Gateway

**Stage:** 3 of 4  
**Focus:** Unified API Layer  
**Dependencies:** Stage 1 OR Stage 2 (at least one complete)  
**Blocks:** Stage 4

---

## Scope

Build a FastAPI application that:
1. Provides REST endpoints for common 3D operations
2. Provides WebSocket for real-time code execution
3. Routes requests to Blender or FreeCAD socket servers
4. Auto-generates OpenAPI documentation

---

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| `api/main.py` | FastAPI app entry point |
| `api/config.py` | Configuration management |
| `api/routers/blender.py` | Blender REST endpoints |
| `api/routers/freecad.py` | FreeCAD REST endpoints |
| `api/routers/health.py` | Health check endpoints |
| `api/clients/blender_client.py` | Blender socket client |
| `api/clients/freecad_client.py` | FreeCAD socket client |
| `api/models/*.py` | Pydantic request/response models |
| `api/websocket/handler.py` | WebSocket handler |

---

## Task Breakdown

### 3.1 Project Setup
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.1.1 | Create `/home/ubuntu/devs/eng/api/` directory structure | ⬜ | |
| 3.1.2 | Create `requirements.txt` with dependencies | ⬜ | fastapi, uvicorn, pydantic, websockets |
| 3.1.3 | Create `api/__init__.py` | ⬜ | |
| 3.1.4 | Create `config.py` with settings (ports, hosts) | ⬜ | Pydantic Settings |
| 3.1.5 | Create `.env.example` with environment variables | ⬜ | |

### 3.2 Socket Clients
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.2.1 | Create `clients/__init__.py` | ⬜ | |
| 3.2.2 | Create `clients/base_client.py` with `BaseSocketClient` | ⬜ | Abstract base |
| 3.2.3 | Implement `connect()` method | ⬜ | TCP connection |
| 3.2.4 | Implement `disconnect()` method | ⬜ | Clean close |
| 3.2.5 | Implement `send_command(method, params)` method | ⬜ | JSON-RPC |
| 3.2.6 | Implement `receive_response()` method | ⬜ | Parse JSON |
| 3.2.7 | Implement connection pooling | ⬜ | Reuse connections |
| 3.2.8 | Implement retry logic with backoff | ⬜ | Resilience |
| 3.2.9 | Create `clients/blender_client.py` | ⬜ | Extends base |
| 3.2.10 | Create `clients/freecad_client.py` | ⬜ | Extends base |
| 3.2.11 | Add async versions of send/receive | ⬜ | For FastAPI async |

### 3.3 Pydantic Models
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.3.1 | Create `models/__init__.py` | ⬜ | |
| 3.3.2 | Create `models/common.py` - shared models | ⬜ | Vector3, Color, etc. |
| 3.3.3 | Create `models/primitives.py` - primitive params | ⬜ | |
| 3.3.4 | Define `CubeParams` model | ⬜ | location, size, name |
| 3.3.5 | Define `SphereParams` model | ⬜ | location, radius, name |
| 3.3.6 | Define `CylinderParams` model | ⬜ | location, radius, depth, name |
| 3.3.7 | Define `ConeParams` model | ⬜ | |
| 3.3.8 | Define `TorusParams` model | ⬜ | |
| 3.3.9 | Define `PlaneParams` model | ⬜ | |
| 3.3.10 | Define `BoxParams` model (FreeCAD) | ⬜ | length, width, height |
| 3.3.11 | Create `models/materials.py` | ⬜ | |
| 3.3.12 | Define `MaterialParams` model | ⬜ | name, color, metallic, roughness |
| 3.3.13 | Create `models/rendering.py` | ⬜ | |
| 3.3.14 | Define `RenderParams` model | ⬜ | output, resolution, engine, samples |
| 3.3.15 | Create `models/boolean.py` | ⬜ | |
| 3.3.16 | Define `BooleanParams` model | ⬜ | object1, object2, operation, name |
| 3.3.17 | Create `models/export.py` | ⬜ | |
| 3.3.18 | Define `ExportParams` model | ⬜ | objects, filepath, format |
| 3.3.19 | Create `models/responses.py` | ⬜ | |
| 3.3.20 | Define `APIResponse` model | ⬜ | status, result, error |
| 3.3.21 | Define `ObjectInfo` model | ⬜ | name, type, location, etc. |
| 3.3.22 | Define `SceneInfo` model | ⬜ | objects list |

### 3.4 Health & Status Endpoints
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.4.1 | Create `routers/__init__.py` | ⬜ | |
| 3.4.2 | Create `routers/health.py` | ⬜ | |
| 3.4.3 | Implement `GET /health` - API health | ⬜ | |
| 3.4.4 | Implement `GET /health/blender` - Blender status | ⬜ | Ping socket |
| 3.4.5 | Implement `GET /health/freecad` - FreeCAD status | ⬜ | Ping socket |
| 3.4.6 | Implement `GET /version` - API version | ⬜ | |

### 3.5 Blender REST Endpoints
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.5.1 | Create `routers/blender.py` | ⬜ | |
| 3.5.2 | Implement `POST /api/v1/blender/primitives/cube` | ⬜ | |
| 3.5.3 | Implement `POST /api/v1/blender/primitives/sphere` | ⬜ | |
| 3.5.4 | Implement `POST /api/v1/blender/primitives/cylinder` | ⬜ | |
| 3.5.5 | Implement `POST /api/v1/blender/primitives/cone` | ⬜ | |
| 3.5.6 | Implement `POST /api/v1/blender/primitives/torus` | ⬜ | |
| 3.5.7 | Implement `POST /api/v1/blender/primitives/plane` | ⬜ | |
| 3.5.8 | Implement `GET /api/v1/blender/objects` | ⬜ | List objects |
| 3.5.9 | Implement `GET /api/v1/blender/objects/{name}` | ⬜ | Get object |
| 3.5.10 | Implement `DELETE /api/v1/blender/objects/{name}` | ⬜ | Delete object |
| 3.5.11 | Implement `PATCH /api/v1/blender/objects/{name}` | ⬜ | Transform |
| 3.5.12 | Implement `POST /api/v1/blender/materials` | ⬜ | Create material |
| 3.5.13 | Implement `POST /api/v1/blender/materials/apply` | ⬜ | Apply to object |
| 3.5.14 | Implement `GET /api/v1/blender/scene` | ⬜ | Scene info |
| 3.5.15 | Implement `DELETE /api/v1/blender/scene` | ⬜ | Clear scene |
| 3.5.16 | Implement `POST /api/v1/blender/render` | ⬜ | Render image |
| 3.5.17 | Implement `POST /api/v1/blender/export` | ⬜ | Export model |
| 3.5.18 | Implement `POST /api/v1/blender/camera` | ⬜ | Add camera |
| 3.5.19 | Implement `POST /api/v1/blender/light` | ⬜ | Add light |

### 3.6 FreeCAD REST Endpoints
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.6.1 | Create `routers/freecad.py` | ⬜ | |
| 3.6.2 | Implement `POST /api/v1/freecad/primitives/box` | ⬜ | |
| 3.6.3 | Implement `POST /api/v1/freecad/primitives/sphere` | ⬜ | |
| 3.6.4 | Implement `POST /api/v1/freecad/primitives/cylinder` | ⬜ | |
| 3.6.5 | Implement `POST /api/v1/freecad/primitives/cone` | ⬜ | |
| 3.6.6 | Implement `POST /api/v1/freecad/primitives/torus` | ⬜ | |
| 3.6.7 | Implement `GET /api/v1/freecad/objects` | ⬜ | List objects |
| 3.6.8 | Implement `GET /api/v1/freecad/objects/{name}` | ⬜ | Get object |
| 3.6.9 | Implement `DELETE /api/v1/freecad/objects/{name}` | ⬜ | Delete object |
| 3.6.10 | Implement `POST /api/v1/freecad/boolean/union` | ⬜ | |
| 3.6.11 | Implement `POST /api/v1/freecad/boolean/subtract` | ⬜ | |
| 3.6.12 | Implement `POST /api/v1/freecad/boolean/intersect` | ⬜ | |
| 3.6.13 | Implement `POST /api/v1/freecad/export` | ⬜ | Export (STEP/STL) |
| 3.6.14 | Implement `GET /api/v1/freecad/documents` | ⬜ | List documents |
| 3.6.15 | Implement `POST /api/v1/freecad/documents` | ⬜ | New document |

### 3.7 WebSocket Handler
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.7.1 | Create `websocket/__init__.py` | ⬜ | |
| 3.7.2 | Create `websocket/handler.py` | ⬜ | |
| 3.7.3 | Implement `WebSocket /ws/blender` endpoint | ⬜ | |
| 3.7.4 | Implement `WebSocket /ws/freecad` endpoint | ⬜ | |
| 3.7.5 | Handle `execute` message type | ⬜ | Run Python code |
| 3.7.6 | Handle `subscribe` message type | ⬜ | Event subscription |
| 3.7.7 | Implement connection management | ⬜ | Track active connections |
| 3.7.8 | Implement broadcast capability | ⬜ | Send to all clients |
| 3.7.9 | Add heartbeat/ping-pong | ⬜ | Keep alive |

### 3.8 FastAPI App Assembly
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.8.1 | Create `main.py` with FastAPI app | ⬜ | |
| 3.8.2 | Configure CORS middleware | ⬜ | Allow cross-origin |
| 3.8.3 | Include health router | ⬜ | |
| 3.8.4 | Include blender router | ⬜ | |
| 3.8.5 | Include freecad router | ⬜ | |
| 3.8.6 | Mount WebSocket endpoints | ⬜ | |
| 3.8.7 | Configure OpenAPI metadata | ⬜ | Title, description, version |
| 3.8.8 | Add startup event (init clients) | ⬜ | |
| 3.8.9 | Add shutdown event (cleanup) | ⬜ | |
| 3.8.10 | Configure logging | ⬜ | |

### 3.9 Error Handling
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.9.1 | Create custom exception classes | ⬜ | |
| 3.9.2 | Create `BlenderConnectionError` | ⬜ | |
| 3.9.3 | Create `FreeCADConnectionError` | ⬜ | |
| 3.9.4 | Create `CommandExecutionError` | ⬜ | |
| 3.9.5 | Implement global exception handler | ⬜ | Consistent responses |
| 3.9.6 | Add request validation error handler | ⬜ | Pydantic errors |

### 3.10 Documentation
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.10.1 | Add docstrings to all endpoints | ⬜ | For OpenAPI |
| 3.10.2 | Add example requests/responses | ⬜ | In Pydantic models |
| 3.10.3 | Create `docs/API.md` with usage guide | ⬜ | |
| 3.10.4 | Verify Swagger UI at `/docs` | ⬜ | |
| 3.10.5 | Verify ReDoc at `/redoc` | ⬜ | |

### 3.11 Startup Scripts
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.11.1 | Create `scripts/start_api.sh` | ⬜ | Start uvicorn |
| 3.11.2 | Create `scripts/start_all.sh` | ⬜ | Start all services |
| 3.11.3 | Create `scripts/stop_all.sh` | ⬜ | Stop all services |
| 3.11.4 | Create `scripts/health_check.sh` | ⬜ | Check all services |

### 3.12 Testing
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 3.12.1 | Create `tests/test_api/__init__.py` | ⬜ | |
| 3.12.2 | Create `tests/test_api/conftest.py` | ⬜ | Fixtures |
| 3.12.3 | Test: Health endpoints | ⬜ | |
| 3.12.4 | Test: Blender primitive endpoints | ⬜ | |
| 3.12.5 | Test: FreeCAD primitive endpoints | ⬜ | |
| 3.12.6 | Test: WebSocket connection | ⬜ | |
| 3.12.7 | Test: WebSocket code execution | ⬜ | |
| 3.12.8 | Test: Error responses | ⬜ | |
| 3.12.9 | Test: Connection failure handling | ⬜ | |

---

## Task Summary

| Section | Tasks | Priority |
|---------|-------|----------|
| 3.1 Project Setup | 5 | 🔴 Critical |
| 3.2 Socket Clients | 11 | 🔴 Critical |
| 3.3 Pydantic Models | 22 | 🔴 Critical |
| 3.4 Health Endpoints | 6 | 🟡 High |
| 3.5 Blender Endpoints | 19 | 🔴 Critical |
| 3.6 FreeCAD Endpoints | 15 | 🔴 Critical |
| 3.7 WebSocket Handler | 9 | 🟡 High |
| 3.8 App Assembly | 10 | 🔴 Critical |
| 3.9 Error Handling | 6 | 🟡 High |
| 3.10 Documentation | 5 | 🟢 Medium |
| 3.11 Startup Scripts | 4 | 🟡 High |
| 3.12 Testing | 9 | 🟡 High |
| **TOTAL** | **121** | |

---

## Execution Order

```
3.1 Setup ──► 3.2 Clients ──► 3.3 Models ──► 3.8 App Assembly
                   │              │                  │
                   │              ├──► 3.4 Health ───┤
                   │              ├──► 3.5 Blender ──┤
                   │              ├──► 3.6 FreeCAD ──┤
                   │              └──► 3.7 WebSocket─┤
                   │                                 │
                   └──► 3.9 Errors ──────────────────┘
                                                     │
                                                     ▼
                              3.10 Docs ──► 3.11 Scripts ──► 3.12 Testing
```

---

## Acceptance Criteria

Stage 3 is **COMPLETE** when:

- [ ] FastAPI server starts on port 8000
- [ ] Swagger docs available at `/docs`
- [ ] Health check endpoints work
- [ ] All Blender primitive endpoints functional
- [ ] All FreeCAD primitive endpoints functional
- [ ] Boolean operations work via API
- [ ] Render endpoint produces image
- [ ] Export endpoints produce files
- [ ] WebSocket code execution works
- [ ] All API tests pass

---

## API Design Principles

### URL Structure
```
/api/v1/{application}/{resource}
/api/v1/blender/primitives/cube
/api/v1/freecad/boolean/union
```

### Response Format
```json
{
  "status": "success",
  "result": {
    "object_id": "Cube.001",
    "message": "Created cube"
  }
}
```

### Error Format
```json
{
  "status": "error",
  "error": {
    "code": "CONNECTION_FAILED",
    "message": "Could not connect to Blender server",
    "details": {}
  }
}
```
