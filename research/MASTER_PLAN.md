# 🎯 Master Plan: Blender & FreeCAD Local API Project

**Project Name:** 3D Modeling API (3DM-API)  
**Created:** January 20, 2026  
**Location:** `/home/ubuntu/devs/eng/`

---

## Executive Summary

Build a unified local API system to control **Blender** and **FreeCAD** programmatically, enabling AI agents to create, manipulate, and render 3D shapes without MCP overhead.

---

## Project Vision

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI AGENT                                 │
│              (Claude, GPT, Local LLM, Your Code)                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    3DM-API GATEWAY                               │
│                   FastAPI + WebSocket                            │
│                     Port 8000                                    │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │   /api/v1/blender/*     │  │   /api/v1/freecad/*         │  │
│  └────────────┬────────────┘  └────────────┬────────────────┘  │
└───────────────┼─────────────────────────────┼───────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌─────────────────────────────────┐
│      BLENDER ENGINE       │   │       FREECAD ENGINE            │
│    (Headless Instance)    │   │     (Headless Instance)         │
│                           │   │                                 │
│  ┌─────────────────────┐  │   │  ┌───────────────────────────┐  │
│  │  Socket Server      │  │   │  │  Socket Server            │  │
│  │  Port 9876          │  │   │  │  Port 9877                │  │
│  └─────────────────────┘  │   │  └───────────────────────────┘  │
│                           │   │                                 │
│  Features:                │   │  Features:                      │
│  • Mesh primitives        │   │  • Part primitives              │
│  • Materials & textures   │   │  • Boolean operations           │
│  • Lighting & cameras     │   │  • Parametric modeling          │
│  • Cycles/EEVEE render    │   │  • STEP/IGES/STL export         │
│  • GLB/FBX/OBJ export     │   │  • Sketcher operations          │
└───────────────────────────┘   └─────────────────────────────────┘
```

---

## Roadmap Overview

| Stage | Name | Focus | Deliverables |
|-------|------|-------|--------------|
| **1** | Blender Socket Addon | Core Blender integration | Socket server, primitives, rendering |
| **2** | FreeCAD Socket Server | Core FreeCAD integration | Socket server, Part module, export |
| **3** | FastAPI Gateway | Unified API layer | REST endpoints, WebSocket, docs |
| **4** | AI Integration & Testing | Production readiness | Function schemas, tests, examples |

---

## Stage Dependencies

```
Stage 1 ──────────────┐
(Blender Addon)       │
                      ├──────► Stage 3 ──────► Stage 4
Stage 2 ──────────────┘        (Gateway)       (AI + Tests)
(FreeCAD Server)
```

- Stages 1 & 2 can run **in parallel**
- Stage 3 requires at least one of Stage 1 or 2 complete
- Stage 4 requires Stage 3 complete

---

## Project Structure

```
/home/ubuntu/devs/eng/
├── research/
│   ├── BLENDER_FREECAD_API_RESEARCH.md
│   ├── MASTER_PLAN.md
│   ├── STAGE_1_PLAN.md
│   ├── STAGE_2_PLAN.md
│   ├── STAGE_3_PLAN.md
│   └── STAGE_4_PLAN.md
│
├── src/
│   ├── blender/
│   │   ├── __init__.py
│   │   ├── addon/
│   │   │   ├── __init__.py
│   │   │   ├── server.py          # Socket server
│   │   │   ├── handlers.py        # Command handlers
│   │   │   ├── primitives.py      # Shape creation
│   │   │   ├── materials.py       # Material operations
│   │   │   ├── rendering.py       # Render operations
│   │   │   └── scene.py           # Scene management
│   │   └── scripts/
│   │       └── start_server.py    # Headless startup script
│   │
│   ├── freecad/
│   │   ├── __init__.py
│   │   ├── server/
│   │   │   ├── __init__.py
│   │   │   ├── server.py          # Socket server
│   │   │   ├── handlers.py        # Command handlers
│   │   │   ├── primitives.py      # Part primitives
│   │   │   ├── boolean.py         # Boolean operations
│   │   │   ├── export.py          # Export handlers
│   │   │   └── document.py        # Document management
│   │   └── scripts/
│   │       └── start_server.py    # Headless startup script
│   │
│   └── common/
│       ├── __init__.py
│       ├── protocol.py            # JSON-RPC protocol
│       ├── client.py              # Socket client base
│       └── exceptions.py          # Custom exceptions
│
├── api/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # Configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── blender.py             # Blender endpoints
│   │   ├── freecad.py             # FreeCAD endpoints
│   │   └── health.py              # Health checks
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── blender_client.py      # Blender socket client
│   │   └── freecad_client.py      # FreeCAD socket client
│   ├── models/
│   │   ├── __init__.py
│   │   ├── primitives.py          # Pydantic models
│   │   ├── materials.py
│   │   ├── rendering.py
│   │   └── responses.py
│   └── websocket/
│       ├── __init__.py
│       └── handler.py             # WebSocket handler
│
├── tests/
│   ├── __init__.py
│   ├── test_blender/
│   │   ├── test_primitives.py
│   │   ├── test_materials.py
│   │   └── test_rendering.py
│   ├── test_freecad/
│   │   ├── test_primitives.py
│   │   ├── test_boolean.py
│   │   └── test_export.py
│   ├── test_api/
│   │   ├── test_endpoints.py
│   │   └── test_websocket.py
│   └── integration/
│       └── test_full_workflow.py
│
├── ai/
│   ├── schemas/
│   │   ├── openai_functions.json
│   │   └── anthropic_tools.json
│   └── examples/
│       ├── create_scene.py
│       └── render_workflow.py
│
├── scripts/
│   ├── install.sh                 # Installation script
│   ├── start_all.sh               # Start all services
│   ├── stop_all.sh                # Stop all services
│   └── health_check.sh            # Check service status
│
├── config/
│   ├── blender.yaml               # Blender config
│   ├── freecad.yaml               # FreeCAD config
│   └── api.yaml                   # API config
│
├── docs/
│   ├── API.md                     # API documentation
│   ├── SETUP.md                   # Setup guide
│   └── EXAMPLES.md                # Usage examples
│
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata
└── README.md                      # Project overview
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| API Framework | FastAPI | 0.109+ |
| Async Server | Uvicorn | 0.27+ |
| Validation | Pydantic | 2.5+ |
| WebSocket | websockets | 12.0+ |
| 3D Modeling | Blender | 4.0+ |
| CAD Engine | FreeCAD | 0.21+ |
| Testing | pytest | 8.0+ |
| Async Testing | pytest-asyncio | 0.23+ |

---

## Success Criteria

### Stage 1 Complete When:
- [ ] Blender addon installs without errors
- [ ] Socket server starts and accepts connections
- [ ] Can create cube, sphere, cylinder via API
- [ ] Can apply basic material
- [ ] Can render scene to PNG

### Stage 2 Complete When:
- [ ] FreeCAD script runs in headless mode
- [ ] Socket server starts and accepts connections
- [ ] Can create box, sphere, cylinder via API
- [ ] Can perform boolean union/subtract
- [ ] Can export to STEP format

### Stage 3 Complete When:
- [ ] FastAPI server starts on port 8000
- [ ] All Blender endpoints functional
- [ ] All FreeCAD endpoints functional
- [ ] WebSocket code execution works
- [ ] Swagger docs auto-generated

### Stage 4 Complete When:
- [ ] OpenAI function schemas defined
- [ ] Anthropic tool definitions defined
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Example AI workflow runs successfully

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Blender threading issues | High | Use modal operators, timer-based execution |
| FreeCAD GUI dependencies | Medium | Test all operations in headless mode first |
| Socket connection drops | Medium | Implement reconnection logic |
| Large render blocking | High | Async rendering with progress callbacks |

---

## Next Steps

1. Review Stage 1 Plan → `STAGE_1_PLAN.md`
2. Review Stage 2 Plan → `STAGE_2_PLAN.md`
3. Review Stage 3 Plan → `STAGE_3_PLAN.md`
4. Review Stage 4 Plan → `STAGE_4_PLAN.md`
5. Discuss and refine
6. Begin execution!

---

*Let's build something awesome! 🚀*
