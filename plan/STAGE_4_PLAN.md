# 📦 Stage 4 Plan: AI Integration & Testing

**Stage:** 4 of 4  
**Focus:** Production Readiness  
**Dependencies:** Stage 3 (Gateway complete)  
**Blocks:** None (final stage)

---

## Scope

Prepare the system for AI agent integration:
1. Define function/tool schemas for AI providers
2. Create comprehensive test suite
3. Build example workflows
4. Write documentation

---

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| `ai/schemas/openai_functions.json` | OpenAI function calling schemas |
| `ai/schemas/anthropic_tools.json` | Anthropic tool definitions |
| `ai/examples/*.py` | Example AI workflows |
| `tests/` | Complete test suite |
| `docs/` | User documentation |

---

## Task Breakdown

### 4.1 OpenAI Function Schemas
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.1.1 | Create `ai/schemas/` directory | ⬜ | |
| 4.1.2 | Create `openai_functions.json` base structure | ⬜ | |
| 4.1.3 | Define `create_3d_primitive` function | ⬜ | Unified primitive creation |
| 4.1.4 | Define `modify_object` function | ⬜ | Transform, rename, delete |
| 4.1.5 | Define `apply_material` function | ⬜ | Material operations |
| 4.1.6 | Define `boolean_operation` function | ⬜ | Union, subtract, intersect |
| 4.1.7 | Define `render_scene` function | ⬜ | Blender rendering |
| 4.1.8 | Define `export_model` function | ⬜ | Export to various formats |
| 4.1.9 | Define `get_scene_info` function | ⬜ | Query scene state |
| 4.1.10 | Define `execute_code` function | ⬜ | Run arbitrary Python |
| 4.1.11 | Define `add_camera` function | ⬜ | Camera setup |
| 4.1.12 | Define `add_light` function | ⬜ | Lighting setup |
| 4.1.13 | Validate JSON schema syntax | ⬜ | |

### 4.2 Anthropic Tool Definitions
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.2.1 | Create `anthropic_tools.json` base structure | ⬜ | |
| 4.2.2 | Define `create_3d_primitive` tool | ⬜ | With input_schema |
| 4.2.3 | Define `modify_object` tool | ⬜ | |
| 4.2.4 | Define `apply_material` tool | ⬜ | |
| 4.2.5 | Define `boolean_operation` tool | ⬜ | |
| 4.2.6 | Define `render_scene` tool | ⬜ | |
| 4.2.7 | Define `export_model` tool | ⬜ | |
| 4.2.8 | Define `get_scene_info` tool | ⬜ | |
| 4.2.9 | Define `execute_code` tool | ⬜ | |
| 4.2.10 | Validate tool definitions | ⬜ | |

### 4.3 Python Schema Helpers
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.3.1 | Create `ai/__init__.py` | ⬜ | |
| 4.3.2 | Create `ai/schemas/__init__.py` | ⬜ | |
| 4.3.3 | Create `ai/schemas/loader.py` | ⬜ | Load JSON schemas |
| 4.3.4 | Implement `get_openai_functions()` | ⬜ | Return function list |
| 4.3.5 | Implement `get_anthropic_tools()` | ⬜ | Return tool list |
| 4.3.6 | Implement `get_function_by_name(name)` | ⬜ | Lookup helper |

### 4.4 Function Executor
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.4.1 | Create `ai/executor.py` | ⬜ | |
| 4.4.2 | Implement `FunctionExecutor` class | ⬜ | |
| 4.4.3 | Implement `execute(function_name, arguments)` | ⬜ | Route to API |
| 4.4.4 | Map function names to API endpoints | ⬜ | |
| 4.4.5 | Handle API responses and errors | ⬜ | |
| 4.4.6 | Add async version `execute_async()` | ⬜ | |

### 4.5 Example Workflows
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.5.1 | Create `ai/examples/` directory | ⬜ | |
| 4.5.2 | Create `simple_scene.py` - basic shapes | ⬜ | Cube + sphere + render |
| 4.5.3 | Create `boolean_demo.py` - boolean ops | ⬜ | Union/subtract examples |
| 4.5.4 | Create `material_demo.py` - materials | ⬜ | Colored objects |
| 4.5.5 | Create `export_demo.py` - export formats | ⬜ | STEP, STL, GLB |
| 4.5.6 | Create `openai_integration.py` - OpenAI example | ⬜ | With function calling |
| 4.5.7 | Create `anthropic_integration.py` - Claude example | ⬜ | With tool use |
| 4.5.8 | Create `batch_creation.py` - multiple objects | ⬜ | Performance test |
| 4.5.9 | Create `full_workflow.py` - end-to-end | ⬜ | Complete pipeline |

### 4.6 Unit Tests - Blender
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.6.1 | Create `tests/test_blender/__init__.py` | ⬜ | |
| 4.6.2 | Create `tests/test_blender/conftest.py` | ⬜ | Fixtures |
| 4.6.3 | Create `test_primitives.py` | ⬜ | |
| 4.6.4 | Test: Create cube | ⬜ | |
| 4.6.5 | Test: Create sphere | ⬜ | |
| 4.6.6 | Test: Create cylinder | ⬜ | |
| 4.6.7 | Test: Create with custom location | ⬜ | |
| 4.6.8 | Test: Create with custom name | ⬜ | |
| 4.6.9 | Create `test_materials.py` | ⬜ | |
| 4.6.10 | Test: Create material | ⬜ | |
| 4.6.11 | Test: Apply material to object | ⬜ | |
| 4.6.12 | Test: Set material color | ⬜ | |
| 4.6.13 | Create `test_rendering.py` | ⬜ | |
| 4.6.14 | Test: Render to PNG | ⬜ | |
| 4.6.15 | Test: Set render resolution | ⬜ | |
| 4.6.16 | Create `test_export.py` | ⬜ | |
| 4.6.17 | Test: Export to GLB | ⬜ | |
| 4.6.18 | Test: Export to OBJ | ⬜ | |

### 4.7 Unit Tests - FreeCAD
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.7.1 | Create `tests/test_freecad/__init__.py` | ⬜ | |
| 4.7.2 | Create `tests/test_freecad/conftest.py` | ⬜ | Fixtures |
| 4.7.3 | Create `test_primitives.py` | ⬜ | |
| 4.7.4 | Test: Create box | ⬜ | |
| 4.7.5 | Test: Create sphere | ⬜ | |
| 4.7.6 | Test: Create cylinder | ⬜ | |
| 4.7.7 | Test: Create with dimensions | ⬜ | |
| 4.7.8 | Create `test_boolean.py` | ⬜ | |
| 4.7.9 | Test: Boolean union | ⬜ | |
| 4.7.10 | Test: Boolean subtract | ⬜ | |
| 4.7.11 | Test: Boolean intersect | ⬜ | |
| 4.7.12 | Create `test_export.py` | ⬜ | |
| 4.7.13 | Test: Export to STEP | ⬜ | |
| 4.7.14 | Test: Export to STL | ⬜ | |
| 4.7.15 | Test: Export to IGES | ⬜ | |

### 4.8 Integration Tests
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.8.1 | Create `tests/integration/__init__.py` | ⬜ | |
| 4.8.2 | Create `tests/integration/conftest.py` | ⬜ | Start services |
| 4.8.3 | Create `test_full_workflow.py` | ⬜ | |
| 4.8.4 | Test: Create scene → Add objects → Render | ⬜ | Blender workflow |
| 4.8.5 | Test: Create parts → Boolean → Export | ⬜ | FreeCAD workflow |
| 4.8.6 | Test: API → Blender → Response | ⬜ | Full stack |
| 4.8.7 | Test: API → FreeCAD → Response | ⬜ | Full stack |
| 4.8.8 | Test: WebSocket code execution | ⬜ | |
| 4.8.9 | Test: Concurrent requests | ⬜ | Load test |
| 4.8.10 | Test: Error recovery | ⬜ | Resilience |

### 4.9 Test Configuration
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.9.1 | Create `tests/conftest.py` - root fixtures | ⬜ | |
| 4.9.2 | Create `pytest.ini` configuration | ⬜ | |
| 4.9.3 | Create `tests/requirements.txt` | ⬜ | pytest, pytest-asyncio |
| 4.9.4 | Add test coverage configuration | ⬜ | pytest-cov |
| 4.9.5 | Create GitHub Actions workflow (optional) | ⬜ | CI/CD |

### 4.10 Documentation
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.10.1 | Create `docs/` directory | ⬜ | |
| 4.10.2 | Create `docs/SETUP.md` - installation guide | ⬜ | |
| 4.10.3 | Document Blender installation | ⬜ | |
| 4.10.4 | Document FreeCAD installation | ⬜ | |
| 4.10.5 | Document Python dependencies | ⬜ | |
| 4.10.6 | Document service startup | ⬜ | |
| 4.10.7 | Create `docs/API.md` - API reference | ⬜ | |
| 4.10.8 | Document all Blender endpoints | ⬜ | |
| 4.10.9 | Document all FreeCAD endpoints | ⬜ | |
| 4.10.10 | Document WebSocket usage | ⬜ | |
| 4.10.11 | Create `docs/EXAMPLES.md` - usage examples | ⬜ | |
| 4.10.12 | Add curl examples | ⬜ | |
| 4.10.13 | Add Python examples | ⬜ | |
| 4.10.14 | Add AI integration examples | ⬜ | |
| 4.10.15 | Create `docs/AI_INTEGRATION.md` | ⬜ | |
| 4.10.16 | Document OpenAI function calling | ⬜ | |
| 4.10.17 | Document Anthropic tool use | ⬜ | |
| 4.10.18 | Update root `README.md` | ⬜ | Project overview |

### 4.11 Configuration Files
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.11.1 | Create `config/` directory | ⬜ | |
| 4.11.2 | Create `config/blender.yaml` | ⬜ | Blender settings |
| 4.11.3 | Create `config/freecad.yaml` | ⬜ | FreeCAD settings |
| 4.11.4 | Create `config/api.yaml` | ⬜ | API settings |
| 4.11.5 | Create `pyproject.toml` | ⬜ | Project metadata |

### 4.12 Final Validation
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 4.12.1 | Run all unit tests | ⬜ | `pytest tests/` |
| 4.12.2 | Run integration tests | ⬜ | |
| 4.12.3 | Verify Swagger docs complete | ⬜ | |
| 4.12.4 | Test OpenAI integration example | ⬜ | |
| 4.12.5 | Test Anthropic integration example | ⬜ | |
| 4.12.6 | Performance benchmark | ⬜ | Requests/second |
| 4.12.7 | Memory usage check | ⬜ | No leaks |
| 4.12.8 | Clean shutdown test | ⬜ | All services |
| 4.12.9 | Documentation review | ⬜ | Complete and accurate |
| 4.12.10 | Code cleanup and formatting | ⬜ | Black, isort |

---

## Task Summary

| Section | Tasks | Priority |
|---------|-------|----------|
| 4.1 OpenAI Schemas | 13 | 🔴 Critical |
| 4.2 Anthropic Tools | 10 | 🔴 Critical |
| 4.3 Schema Helpers | 6 | 🟡 High |
| 4.4 Function Executor | 6 | 🟡 High |
| 4.5 Example Workflows | 9 | 🟡 High |
| 4.6 Unit Tests - Blender | 18 | 🔴 Critical |
| 4.7 Unit Tests - FreeCAD | 15 | 🔴 Critical |
| 4.8 Integration Tests | 10 | 🟡 High |
| 4.9 Test Configuration | 5 | 🟡 High |
| 4.10 Documentation | 18 | 🟢 Medium |
| 4.11 Configuration Files | 5 | 🟢 Medium |
| 4.12 Final Validation | 10 | 🔴 Critical |
| **TOTAL** | **125** | |

---

## Execution Order

```
4.1 OpenAI ──┬──► 4.3 Helpers ──► 4.4 Executor ──► 4.5 Examples
4.2 Anthropic┘                                         │
                                                       ▼
4.6 Blender Tests ──┬──► 4.8 Integration ──► 4.9 Config
4.7 FreeCAD Tests ──┘           │
                                ▼
                    4.10 Docs ──► 4.11 Config ──► 4.12 Validation
```

---

## Acceptance Criteria

Stage 4 is **COMPLETE** when:

- [ ] OpenAI function schemas are valid and complete
- [ ] Anthropic tool definitions are valid and complete
- [ ] All unit tests pass (>90% coverage)
- [ ] All integration tests pass
- [ ] OpenAI integration example works
- [ ] Anthropic integration example works
- [ ] Documentation is complete
- [ ] README provides clear setup instructions
- [ ] All services start/stop cleanly

---

## AI Function Schema Example

### OpenAI Format
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
        "enum": ["cube", "sphere", "cylinder", "cone", "torus", "box"],
        "description": "Type of primitive shape to create"
      },
      "location": {
        "type": "array",
        "items": {"type": "number"},
        "description": "XYZ coordinates [x, y, z]",
        "default": [0, 0, 0]
      },
      "size": {
        "type": "number",
        "description": "Size or scale of the primitive",
        "default": 1.0
      },
      "name": {
        "type": "string",
        "description": "Optional name for the object"
      }
    },
    "required": ["application", "shape"]
  }
}
```

### Anthropic Format
```json
{
  "name": "create_3d_primitive",
  "description": "Create a 3D primitive shape in Blender or FreeCAD",
  "input_schema": {
    "type": "object",
    "properties": {
      "application": {
        "type": "string",
        "enum": ["blender", "freecad"],
        "description": "Which 3D application to use"
      },
      "shape": {
        "type": "string",
        "enum": ["cube", "sphere", "cylinder", "cone", "torus", "box"],
        "description": "Type of primitive shape to create"
      },
      "location": {
        "type": "array",
        "items": {"type": "number"},
        "description": "XYZ coordinates [x, y, z]"
      },
      "size": {
        "type": "number",
        "description": "Size or scale of the primitive"
      },
      "name": {
        "type": "string",
        "description": "Optional name for the object"
      }
    },
    "required": ["application", "shape"]
  }
}
```

---

## Notes

- **Testing Strategy:** Use mocks for unit tests, real services for integration tests
- **Coverage Goal:** Aim for >90% code coverage
- **Documentation:** Keep in sync with code changes
- **AI Schemas:** Test with actual AI providers before finalizing
