# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- **Stage 2:** FreeCAD socket server with Part module, boolean operations
- **Stage 3:** FastAPI gateway with REST endpoints and WebSocket
- **Stage 4:** AI function schemas, test suite, documentation

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
