# Changelog

## [1.1.0] - 2026-01-21

### Added
- **Command Manuals** in YAML format
  - `docs/man/blender.man` - Complete Blender API reference
  - `docs/man/freecad.man` - Complete FreeCAD API reference
- Updated README with manual references and quick command examples

---

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-20

### 🎉 Project Complete!

- **Stage 4 Complete: AI Integration & Testing**
- `ai/schemas/` — AI function/tool schemas
  - `openai_functions.json` — OpenAI function calling format
  - `anthropic_tools.json` — Anthropic Claude tool use format
  - `loader.py` — Schema loading utilities
- `ai/executor.py` — Function executor for AI integration
- `ai/examples/` — Example workflows
  - `simple_scene.py` — Basic scene creation
  - `boolean_demo.py` — CSG boolean operations
  - `material_demo.py` — Material application
  - `openai_integration.py` — OpenAI function calling example
  - `anthropic_integration.py` — Anthropic tool use example
- `tests/` — Comprehensive test suite
  - `test_blender/` — Blender unit tests
  - `test_freecad/` — FreeCAD unit tests
  - `integration/` — Integration tests
- `docs/` — Complete documentation
  - `SETUP.md` — Installation guide
  - `API.md` — API reference
  - `AI_INTEGRATION.md` — AI integration guide
- `config/` — Configuration files
- `pyproject.toml` — Project metadata
- All 23 tests passing

---

## [0.3.0] - 2026-01-20

### Added
- **Stage 3 Complete: FastAPI Gateway**
- `api/` — Full FastAPI application
  - `main.py` — FastAPI app with CORS, routers, WebSocket
  - `config.py` — Pydantic Settings configuration
  - `clients/` — Async socket clients for Blender/FreeCAD
  - `models/` — Pydantic request/response models
  - `routers/` — REST endpoints (health, blender, freecad)
  - `websocket/` — WebSocket handlers for real-time execution
- `scripts/` — Startup and management scripts
  - `start_api.sh` — Start FastAPI gateway
  - `start_all.sh` — Start all services
  - `stop_all.sh` — Stop all services
  - `health_check.sh` — Check service status
- REST endpoints for Blender primitives, materials, rendering, export
- REST endpoints for FreeCAD primitives, boolean operations, export
- WebSocket endpoints for real-time code execution
- Swagger UI at `/docs`, ReDoc at `/redoc`
- Health check endpoints for all services

---

## [0.2.0] - 2026-01-20

### Added
- **Stage 2 Complete: FreeCAD Socket Server**
- `src/freecad/server/` — Full socket server implementation
  - `server.py` — TCP socket server on port 9877
  - `handlers.py` — Command dispatcher with handler registration
  - `primitives.py` — Part primitives (box, sphere, cylinder, cone, torus, plane, wedge, helix)
  - `document.py` — Document management (new, open, save, close)
  - `boolean.py` — Boolean operations (union, subtract, intersect) + shape modifications
  - `export.py` — Export/import (STEP, IGES, STL, OBJ, BREP)
- `src/freecad/scripts/start_server.py` — Headless startup script
- `tests/test_freecad_client.py` — Socket client for testing
- 43 registered command handlers
- Shape modifications (extrude, revolve, fillet, chamfer, mirror, offset)
- Python code execution in FreeCAD context
- All 12 integration tests passing

---

## [0.1.0] - 2026-01-20

### Added
- **Stage 1 Complete: Blender Socket Addon**
- `src/blender/addon/` — Full socket server addon
  - `server.py` — TCP socket server on port 9876
  - `handlers.py` — Command dispatcher with thread-safe execution
  - `primitives.py` — Mesh primitives (cube, sphere, cylinder, cone, torus, plane, empty)
  - `materials.py` — Material creation and application
  - `scene.py` — Scene management, cameras, lights
  - `rendering.py` — Render and export operations
- `src/common/` — Shared utilities
  - `protocol.py` — JSON-RPC message classes
  - `exceptions.py` — Custom exception hierarchy
- `src/blender/scripts/start_server.py` — Headless startup script
- `tests/test_client.py` — Socket client for testing
- 45 registered command handlers
- Headless mode support (blender -b)
- All 10 integration tests passing

### Changed
- Moved planning docs from `research/` to `plan/`
- Added WSTODO files for all 4 stages

---

### [0.2.0] - TBD
- Stage 2 complete: FreeCAD Socket Server
- Socket server running on port 9877
- Part primitives (box, sphere, cylinder, cone, torus)
- Boolean operations (union, subtract, intersect)
- Export to STEP/STL/IGES

### [0.3.0] - TBD
- Stage 3 complete: FastAPI Gateway
- Unified REST API on port 8000
- WebSocket for code execution
- Auto-generated Swagger documentation
- Health check endpoints

### [1.0.0] - TBD
- Stage 4 complete: Production Ready
- OpenAI function schemas
- Anthropic tool definitions
- Complete test suite (>90% coverage)
- Full documentation
- Example AI workflows

---

## Legend

- **Added** — New features
- **Changed** — Changes in existing functionality
- **Deprecated** — Soon-to-be removed features
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Vulnerability fixes
