# 📦 Stage 2 Plan: FreeCAD Socket Server

**Stage:** 2 of 4  
**Focus:** Core FreeCAD Integration  
**Dependencies:** None (can start immediately)  
**Parallel with:** Stage 1

---

## Scope

Build a FreeCAD Python script that:
1. Runs a TCP socket server in headless FreeCAD
2. Accepts JSON-RPC commands
3. Executes FreeCAD Python API operations (Part, Sketcher, etc.)
4. Returns results/errors as JSON

---

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| `server/server.py` | TCP socket server |
| `server/handlers.py` | Command dispatcher |
| `server/primitives.py` | Part module primitives |
| `server/boolean.py` | Boolean operations |
| `server/export.py` | Export handlers (STEP, STL, IGES) |
| `server/document.py` | Document management |
| `scripts/start_server.py` | Headless startup script |

---

## Task Breakdown

### 2.1 Project Setup
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.1.1 | Create `/home/ubuntu/devs/eng/src/freecad/` directory structure | ⬜ | |
| 2.1.2 | Create `server/__init__.py` | ⬜ | Package init |
| 2.1.3 | Verify FreeCAD headless mode works (`freecadcmd`) | ⬜ | Test installation |
| 2.1.4 | Test basic Part module import in headless | ⬜ | `import Part` |

### 2.2 Socket Server Core
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.2.1 | Create `server.py` with `FreeCADSocketServer` class | ⬜ | TCP server |
| 2.2.2 | Implement `start()` method | ⬜ | Blocking main loop |
| 2.2.3 | Implement `stop()` method for clean shutdown | ⬜ | |
| 2.2.4 | Implement `handle_client()` for connection handling | ⬜ | |
| 2.2.5 | Implement message buffering (newline-delimited JSON) | ⬜ | Handle partial reads |
| 2.2.6 | Add connection timeout and error handling | ⬜ | Robustness |
| 2.2.7 | Implement graceful shutdown on SIGINT | ⬜ | |

### 2.3 Command Handlers
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.3.1 | Create `handlers.py` with `CommandDispatcher` class | ⬜ | Route commands |
| 2.3.2 | Implement `dispatch(command)` method | ⬜ | Method lookup |
| 2.3.3 | Implement `register_handler(method, func)` | ⬜ | Dynamic registration |
| 2.3.4 | Add error wrapping for all handlers | ⬜ | Consistent errors |
| 2.3.5 | Implement `ping` handler for health checks | ⬜ | Basic test |
| 2.3.6 | Implement `get_version` handler | ⬜ | FreeCAD version info |

### 2.4 Document Management
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.4.1 | Create `document.py` module | ⬜ | |
| 2.4.2 | Implement `new_document(name)` | ⬜ | `FreeCAD.newDocument()` |
| 2.4.3 | Implement `get_active_document()` | ⬜ | |
| 2.4.4 | Implement `list_documents()` | ⬜ | |
| 2.4.5 | Implement `close_document(name)` | ⬜ | |
| 2.4.6 | Implement `save_document(filepath)` | ⬜ | .FCStd file |
| 2.4.7 | Implement `open_document(filepath)` | ⬜ | |
| 2.4.8 | Implement `ensure_document()` - auto-create if none | ⬜ | Convenience |
| 2.4.9 | Register all document handlers with dispatcher | ⬜ | |

### 2.5 Part Primitives
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.5.1 | Create `primitives.py` module | ⬜ | |
| 2.5.2 | Implement `create_box(length, width, height, name)` | ⬜ | `Part.makeBox()` |
| 2.5.3 | Implement `create_sphere(radius, name)` | ⬜ | `Part.makeSphere()` |
| 2.5.4 | Implement `create_cylinder(radius, height, name)` | ⬜ | `Part.makeCylinder()` |
| 2.5.5 | Implement `create_cone(radius1, radius2, height, name)` | ⬜ | `Part.makeCone()` |
| 2.5.6 | Implement `create_torus(radius1, radius2, name)` | ⬜ | `Part.makeTorus()` |
| 2.5.7 | Implement `create_plane(length, width, name)` | ⬜ | `Part.makePlane()` |
| 2.5.8 | Implement `create_wedge(params, name)` | ⬜ | `Part.makeWedge()` |
| 2.5.9 | Implement `create_helix(pitch, height, radius, name)` | ⬜ | `Part.makeHelix()` |
| 2.5.10 | Register all primitive handlers with dispatcher | ⬜ | |

### 2.6 Object Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.6.1 | Implement `get_object(name)` - get object info | ⬜ | |
| 2.6.2 | Implement `list_objects()` - list all objects | ⬜ | |
| 2.6.3 | Implement `delete_object(name)` | ⬜ | |
| 2.6.4 | Implement `rename_object(old_name, new_name)` | ⬜ | |
| 2.6.5 | Implement `copy_object(name, new_name)` | ⬜ | |
| 2.6.6 | Implement `get_object_shape(name)` - shape info | ⬜ | Vertices, faces, etc. |
| 2.6.7 | Implement `set_placement(name, position, rotation)` | ⬜ | Transform object |
| 2.6.8 | Register all object handlers with dispatcher | ⬜ | |

### 2.7 Boolean Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.7.1 | Create `boolean.py` module | ⬜ | |
| 2.7.2 | Implement `boolean_union(obj1, obj2, name)` | ⬜ | `shape.fuse()` |
| 2.7.3 | Implement `boolean_subtract(obj1, obj2, name)` | ⬜ | `shape.cut()` |
| 2.7.4 | Implement `boolean_intersect(obj1, obj2, name)` | ⬜ | `shape.common()` |
| 2.7.5 | Implement `multi_union(objects, name)` | ⬜ | Fuse multiple |
| 2.7.6 | Implement `multi_subtract(base, tools, name)` | ⬜ | Cut multiple |
| 2.7.7 | Register all boolean handlers with dispatcher | ⬜ | |

### 2.8 Shape Modifications
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.8.1 | Implement `extrude(object, direction, length, name)` | ⬜ | `shape.extrude()` |
| 2.8.2 | Implement `revolve(object, axis, angle, name)` | ⬜ | `shape.revolve()` |
| 2.8.3 | Implement `fillet(object, radius, edges, name)` | ⬜ | Round edges |
| 2.8.4 | Implement `chamfer(object, size, edges, name)` | ⬜ | Bevel edges |
| 2.8.5 | Implement `mirror(object, plane, name)` | ⬜ | Mirror shape |
| 2.8.6 | Implement `offset(object, distance, name)` | ⬜ | Offset surface |
| 2.8.7 | Register all modification handlers with dispatcher | ⬜ | |

### 2.9 Export Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.9.1 | Create `export.py` module | ⬜ | |
| 2.9.2 | Implement `export_step(objects, filepath)` | ⬜ | STEP format |
| 2.9.3 | Implement `export_iges(objects, filepath)` | ⬜ | IGES format |
| 2.9.4 | Implement `export_stl(objects, filepath)` | ⬜ | STL mesh |
| 2.9.5 | Implement `export_obj(objects, filepath)` | ⬜ | Wavefront OBJ |
| 2.9.6 | Implement `export_brep(objects, filepath)` | ⬜ | BREP format |
| 2.9.7 | Implement `import_step(filepath)` | ⬜ | Import STEP |
| 2.9.8 | Implement `import_stl(filepath)` | ⬜ | Import STL |
| 2.9.9 | Register all export handlers with dispatcher | ⬜ | |

### 2.10 Code Execution
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.10.1 | Implement `execute_python(code)` | ⬜ | Run arbitrary code |
| 2.10.2 | Provide FreeCAD/Part in execution context | ⬜ | Pre-imported |
| 2.10.3 | Capture stdout/stderr from executed code | ⬜ | Return output |
| 2.10.4 | Register execute handler with dispatcher | ⬜ | |

### 2.11 Headless Startup
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.11.1 | Create `scripts/start_server.py` | ⬜ | CLI entry point |
| 2.11.2 | Parse command line arguments (port, host) | ⬜ | Configurable |
| 2.11.3 | Initialize FreeCAD environment | ⬜ | |
| 2.11.4 | Auto-start socket server on script load | ⬜ | |
| 2.11.5 | Handle SIGINT/SIGTERM for clean shutdown | ⬜ | |
| 2.11.6 | Test: `freecadcmd start_server.py` | ⬜ | Verify headless |

### 2.12 Testing & Validation
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 2.12.1 | Create simple Python test client | ⬜ | For manual testing |
| 2.12.2 | Test: Create box via socket | ⬜ | |
| 2.12.3 | Test: Create sphere via socket | ⬜ | |
| 2.12.4 | Test: Boolean union via socket | ⬜ | |
| 2.12.5 | Test: Boolean subtract via socket | ⬜ | |
| 2.12.6 | Test: Export STEP via socket | ⬜ | |
| 2.12.7 | Test: Export STL via socket | ⬜ | |
| 2.12.8 | Test: Error handling (invalid commands) | ⬜ | |
| 2.12.9 | Test: Large model performance | ⬜ | |

---

## Task Summary

| Section | Tasks | Priority |
|---------|-------|----------|
| 2.1 Project Setup | 4 | 🔴 Critical |
| 2.2 Socket Server Core | 7 | 🔴 Critical |
| 2.3 Command Handlers | 6 | 🔴 Critical |
| 2.4 Document Management | 9 | 🔴 Critical |
| 2.5 Part Primitives | 10 | 🔴 Critical |
| 2.6 Object Operations | 8 | 🟡 High |
| 2.7 Boolean Operations | 7 | 🔴 Critical |
| 2.8 Shape Modifications | 7 | 🟢 Medium |
| 2.9 Export Operations | 9 | 🟡 High |
| 2.10 Code Execution | 4 | 🟢 Medium |
| 2.11 Headless Startup | 6 | 🔴 Critical |
| 2.12 Testing | 9 | 🟡 High |
| **TOTAL** | **86** | |

---

## Execution Order

```
2.1 Setup ──► 2.2 Server ──► 2.3 Handlers ──► 2.4 Document ──► 2.5 Primitives
                                    │
                                    ├──► 2.6 Objects
                                    ├──► 2.7 Boolean (Critical!)
                                    ├──► 2.8 Modifications
                                    ├──► 2.9 Export
                                    └──► 2.10 Code Exec
                                              │
                                              ▼
                                    2.11 Headless ──► 2.12 Testing
```

---

## Acceptance Criteria

Stage 2 is **COMPLETE** when:

- [ ] FreeCAD script runs in headless mode (`freecadcmd`)
- [ ] Socket server starts on configurable port (default 9877)
- [ ] Can create all Part primitives via JSON commands
- [ ] Can perform boolean union operation
- [ ] Can perform boolean subtract operation
- [ ] Can export to STEP format
- [ ] Can export to STL format
- [ ] All basic tests pass
- [ ] Clean shutdown on SIGINT

---

## FreeCAD-Specific Notes

### Headless Execution
```bash
# Option 1: Using freecadcmd (recommended)
freecadcmd script.py

# Option 2: Using FreeCAD with --console
freecad --console script.py

# Option 3: Using FreeCAD AppImage
./FreeCAD.AppImage --console script.py
```

### Key Differences from Blender
| Aspect | Blender | FreeCAD |
|--------|---------|---------|
| Threading | Needs timers/modal | Single-threaded OK |
| GUI module | Always available | `FreeCADGui` unavailable headless |
| Shape creation | Operators (`bpy.ops`) | Direct functions (`Part.make*`) |
| Document | Implicit | Explicit document management |

### Part Module Functions
```python
import Part

# Primitives
Part.makeBox(length, width, height)
Part.makeSphere(radius)
Part.makeCylinder(radius, height)
Part.makeCone(radius1, radius2, height)
Part.makeTorus(radius1, radius2)
Part.makePlane(length, width)

# Boolean
shape1.fuse(shape2)      # Union
shape1.cut(shape2)       # Subtract
shape1.common(shape2)    # Intersect

# Export
Part.export([obj], "file.step")
```
