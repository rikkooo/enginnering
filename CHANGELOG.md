# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project structure
- Research documentation
  - `BLENDER_FREECAD_API_RESEARCH.md` — Comprehensive technical analysis
  - `MASTER_PLAN.md` — Project roadmap and architecture
  - `STAGE_1_PLAN.md` — Blender Socket Addon (87 tasks)
  - `STAGE_2_PLAN.md` — FreeCAD Socket Server (86 tasks)
  - `STAGE_3_PLAN.md` — FastAPI Gateway (121 tasks)
  - `STAGE_4_PLAN.md` — AI Integration & Testing (125 tasks)
- Project README with overview and quick start guide
- This CHANGELOG file

### Planned
- **Stage 1:** Blender socket addon with primitives, materials, rendering
- **Stage 2:** FreeCAD socket server with Part module, boolean operations
- **Stage 3:** FastAPI gateway with REST endpoints and WebSocket
- **Stage 4:** AI function schemas, test suite, documentation

---

## Version History

### [0.1.0] - TBD
- Stage 1 complete: Blender Socket Addon
- Socket server running on port 9876
- Basic primitives (cube, sphere, cylinder, cone, torus, plane)
- Material creation and application
- Render to PNG
- Export to GLB/OBJ/FBX

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
