# 📦 Stage 1 Plan: Blender Socket Addon

**Stage:** 1 of 4  
**Focus:** Core Blender Integration  
**Dependencies:** None (can start immediately)  
**Parallel with:** Stage 2

---

## Scope

Build a Blender addon that:
1. Runs a TCP socket server inside Blender
2. Accepts JSON-RPC commands
3. Executes Blender Python API operations
4. Returns results/errors as JSON

---

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| `addon/__init__.py` | Blender addon registration |
| `addon/server.py` | TCP socket server |
| `addon/handlers.py` | Command dispatcher |
| `addon/primitives.py` | Shape creation functions |
| `addon/materials.py` | Material operations |
| `addon/rendering.py` | Render operations |
| `addon/scene.py` | Scene management |
| `scripts/start_server.py` | Headless startup script |

---

## Task Breakdown

### 1.1 Project Setup
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.1.1 | Create `/home/ubuntu/devs/eng/src/blender/` directory structure | ⬜ | |
| 1.1.2 | Create `addon/__init__.py` with bl_info metadata | ⬜ | Blender addon manifest |
| 1.1.3 | Create `common/protocol.py` with JSON-RPC message classes | ⬜ | Shared protocol |
| 1.1.4 | Create `common/exceptions.py` with custom exceptions | ⬜ | Error handling |

### 1.2 Socket Server Core
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.2.1 | Create `server.py` with `BlenderSocketServer` class | ⬜ | TCP server |
| 1.2.2 | Implement `start()` method with threading | ⬜ | Non-blocking |
| 1.2.3 | Implement `stop()` method for clean shutdown | ⬜ | |
| 1.2.4 | Implement `handle_client()` for connection handling | ⬜ | Per-client thread |
| 1.2.5 | Implement message buffering (newline-delimited JSON) | ⬜ | Handle partial reads |
| 1.2.6 | Add connection timeout and error handling | ⬜ | Robustness |
| 1.2.7 | Create Blender operator `BLENDER_OT_start_api_server` | ⬜ | UI integration |
| 1.2.8 | Create Blender operator `BLENDER_OT_stop_api_server` | ⬜ | |
| 1.2.9 | Add server status to Blender UI panel | ⬜ | Visual feedback |

### 1.3 Command Handlers
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.3.1 | Create `handlers.py` with `CommandDispatcher` class | ⬜ | Route commands |
| 1.3.2 | Implement `dispatch(command)` method | ⬜ | Method lookup |
| 1.3.3 | Implement `register_handler(method, func)` | ⬜ | Dynamic registration |
| 1.3.4 | Add error wrapping for all handlers | ⬜ | Consistent errors |
| 1.3.5 | Implement `ping` handler for health checks | ⬜ | Basic test |
| 1.3.6 | Implement `get_version` handler | ⬜ | Blender version info |

### 1.4 Primitive Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.4.1 | Create `primitives.py` module | ⬜ | |
| 1.4.2 | Implement `create_cube(location, size, name)` | ⬜ | `bpy.ops.mesh.primitive_cube_add` |
| 1.4.3 | Implement `create_sphere(location, radius, segments, name)` | ⬜ | `bpy.ops.mesh.primitive_uv_sphere_add` |
| 1.4.4 | Implement `create_cylinder(location, radius, depth, name)` | ⬜ | `bpy.ops.mesh.primitive_cylinder_add` |
| 1.4.5 | Implement `create_cone(location, radius1, radius2, depth, name)` | ⬜ | `bpy.ops.mesh.primitive_cone_add` |
| 1.4.6 | Implement `create_torus(location, major_radius, minor_radius, name)` | ⬜ | `bpy.ops.mesh.primitive_torus_add` |
| 1.4.7 | Implement `create_plane(location, size, name)` | ⬜ | `bpy.ops.mesh.primitive_plane_add` |
| 1.4.8 | Implement `create_empty(location, type, name)` | ⬜ | For grouping |
| 1.4.9 | Register all primitive handlers with dispatcher | ⬜ | |

### 1.5 Object Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.5.1 | Implement `get_object(name)` - get object info | ⬜ | |
| 1.5.2 | Implement `list_objects()` - list all objects | ⬜ | |
| 1.5.3 | Implement `delete_object(name)` | ⬜ | |
| 1.5.4 | Implement `select_object(name)` | ⬜ | |
| 1.5.5 | Implement `transform_object(name, location, rotation, scale)` | ⬜ | |
| 1.5.6 | Implement `duplicate_object(name, new_name)` | ⬜ | |
| 1.5.7 | Implement `rename_object(old_name, new_name)` | ⬜ | |
| 1.5.8 | Register all object handlers with dispatcher | ⬜ | |

### 1.6 Material Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.6.1 | Create `materials.py` module | ⬜ | |
| 1.6.2 | Implement `create_material(name, color)` | ⬜ | Basic diffuse |
| 1.6.3 | Implement `apply_material(object_name, material_name)` | ⬜ | |
| 1.6.4 | Implement `set_material_color(material_name, color)` | ⬜ | RGBA |
| 1.6.5 | Implement `set_material_metallic(material_name, value)` | ⬜ | 0-1 |
| 1.6.6 | Implement `set_material_roughness(material_name, value)` | ⬜ | 0-1 |
| 1.6.7 | Implement `list_materials()` | ⬜ | |
| 1.6.8 | Implement `delete_material(name)` | ⬜ | |
| 1.6.9 | Register all material handlers with dispatcher | ⬜ | |

### 1.7 Scene Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.7.1 | Create `scene.py` module | ⬜ | |
| 1.7.2 | Implement `get_scene_info()` - full scene state | ⬜ | JSON serializable |
| 1.7.3 | Implement `clear_scene()` - remove all objects | ⬜ | |
| 1.7.4 | Implement `new_scene(name)` | ⬜ | |
| 1.7.5 | Implement `save_scene(filepath)` | ⬜ | .blend file |
| 1.7.6 | Implement `load_scene(filepath)` | ⬜ | |
| 1.7.7 | Implement `add_camera(location, rotation, name)` | ⬜ | |
| 1.7.8 | Implement `add_light(type, location, energy, name)` | ⬜ | Point/Sun/Spot |
| 1.7.9 | Implement `set_active_camera(name)` | ⬜ | |
| 1.7.10 | Register all scene handlers with dispatcher | ⬜ | |

### 1.8 Rendering Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.8.1 | Create `rendering.py` module | ⬜ | |
| 1.8.2 | Implement `set_render_engine(engine)` | ⬜ | CYCLES/EEVEE |
| 1.8.3 | Implement `set_render_resolution(width, height)` | ⬜ | |
| 1.8.4 | Implement `set_render_samples(samples)` | ⬜ | Quality |
| 1.8.5 | Implement `render_image(output_path)` | ⬜ | PNG/JPEG |
| 1.8.6 | Implement `render_animation(output_path, start, end)` | ⬜ | Frame range |
| 1.8.7 | Implement `get_render_progress()` | ⬜ | For async |
| 1.8.8 | Register all render handlers with dispatcher | ⬜ | |

### 1.9 Export Operations
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.9.1 | Implement `export_obj(filepath, objects)` | ⬜ | Wavefront OBJ |
| 1.9.2 | Implement `export_fbx(filepath, objects)` | ⬜ | Autodesk FBX |
| 1.9.3 | Implement `export_gltf(filepath, objects)` | ⬜ | GLB/GLTF |
| 1.9.4 | Implement `export_stl(filepath, objects)` | ⬜ | For 3D printing |
| 1.9.5 | Register all export handlers with dispatcher | ⬜ | |

### 1.10 Code Execution
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.10.1 | Implement `execute_python(code)` | ⬜ | Run arbitrary code |
| 1.10.2 | Add safety checks for dangerous operations | ⬜ | Optional sandboxing |
| 1.10.3 | Capture stdout/stderr from executed code | ⬜ | Return output |
| 1.10.4 | Register execute handler with dispatcher | ⬜ | |

### 1.11 Headless Startup
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.11.1 | Create `scripts/start_server.py` | ⬜ | CLI entry point |
| 1.11.2 | Parse command line arguments (port, host) | ⬜ | Configurable |
| 1.11.3 | Auto-start socket server on script load | ⬜ | |
| 1.11.4 | Keep Blender running (event loop) | ⬜ | Don't exit |
| 1.11.5 | Handle SIGINT/SIGTERM for clean shutdown | ⬜ | |
| 1.11.6 | Test: `blender -b -P start_server.py` | ⬜ | Verify headless |

### 1.12 Testing & Validation
| ID | Task | Status | Notes |
|----|------|--------|-------|
| 1.12.1 | Create simple Python test client | ⬜ | For manual testing |
| 1.12.2 | Test: Create cube via socket | ⬜ | |
| 1.12.3 | Test: Create sphere via socket | ⬜ | |
| 1.12.4 | Test: Apply material via socket | ⬜ | |
| 1.12.5 | Test: Render scene via socket | ⬜ | |
| 1.12.6 | Test: Export GLB via socket | ⬜ | |
| 1.12.7 | Test: Multiple concurrent connections | ⬜ | |
| 1.12.8 | Test: Error handling (invalid commands) | ⬜ | |
| 1.12.9 | Test: Large scene performance | ⬜ | |

---

## Task Summary

| Section | Tasks | Priority |
|---------|-------|----------|
| 1.1 Project Setup | 4 | 🔴 Critical |
| 1.2 Socket Server Core | 9 | 🔴 Critical |
| 1.3 Command Handlers | 6 | 🔴 Critical |
| 1.4 Primitive Operations | 9 | 🔴 Critical |
| 1.5 Object Operations | 8 | 🟡 High |
| 1.6 Material Operations | 9 | 🟡 High |
| 1.7 Scene Operations | 10 | 🟡 High |
| 1.8 Rendering Operations | 8 | 🟡 High |
| 1.9 Export Operations | 5 | 🟢 Medium |
| 1.10 Code Execution | 4 | 🟢 Medium |
| 1.11 Headless Startup | 6 | 🔴 Critical |
| 1.12 Testing | 9 | 🟡 High |
| **TOTAL** | **87** | |

---

## Execution Order

```
1.1 Setup ──► 1.2 Server ──► 1.3 Handlers ──► 1.4 Primitives ──► 1.11 Headless
                                    │
                                    ├──► 1.5 Objects
                                    ├──► 1.6 Materials  
                                    ├──► 1.7 Scene
                                    ├──► 1.8 Rendering
                                    ├──► 1.9 Export
                                    └──► 1.10 Code Exec
                                              │
                                              ▼
                                         1.12 Testing
```

---

## Acceptance Criteria

Stage 1 is **COMPLETE** when:

- [ ] Blender addon loads without errors
- [ ] Socket server starts on configurable port (default 9876)
- [ ] Can create all primitive shapes via JSON commands
- [ ] Can apply materials to objects
- [ ] Can render scene to PNG file
- [ ] Can export scene to GLB format
- [ ] Server runs in headless mode (`blender -b`)
- [ ] All basic tests pass
- [ ] Clean shutdown on SIGINT

---

## Notes

- **Threading:** Blender's Python API is not thread-safe. Use `bpy.app.timers` for deferred execution from socket thread.
- **Modal Operators:** Consider using modal operators for long-running tasks.
- **Error Handling:** Always wrap bpy calls in try/except to prevent server crashes.
