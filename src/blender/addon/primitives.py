"""
Primitive Operations
====================
Handlers for creating 3D primitive shapes in Blender.
"""

import bpy
from typing import Optional, List, Tuple

from .handlers import handler


@handler("create_cube")
def create_cube(
    location: List[float] = None,
    size: float = 2.0,
    name: Optional[str] = None
) -> dict:
    """
    Create a cube mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        size: Size of the cube, defaults to 2.0
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    # Create cube mesh data directly (works in headless mode)
    mesh = bpy.data.meshes.new(name or "Cube")
    obj = bpy.data.objects.new(name or "Cube", mesh)
    
    # Link to scene
    bpy.context.collection.objects.link(obj)
    
    # Create cube geometry using bmesh
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=size)
    bm.to_mesh(mesh)
    bm.free()
    
    # Set location
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_sphere")
def create_sphere(
    location: List[float] = None,
    radius: float = 1.0,
    segments: int = 32,
    ring_count: int = 16,
    name: Optional[str] = None
) -> dict:
    """
    Create a UV sphere mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        radius: Radius of the sphere, defaults to 1.0
        segments: Number of segments, defaults to 32
        ring_count: Number of rings, defaults to 16
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    # Create sphere mesh data directly (works in headless mode)
    import bmesh
    mesh = bpy.data.meshes.new(name or "Sphere")
    obj = bpy.data.objects.new(name or "Sphere", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=ring_count, radius=radius)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_cylinder")
def create_cylinder(
    location: List[float] = None,
    radius: float = 1.0,
    depth: float = 2.0,
    vertices: int = 32,
    name: Optional[str] = None
) -> dict:
    """
    Create a cylinder mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        radius: Radius of the cylinder, defaults to 1.0
        depth: Height of the cylinder, defaults to 2.0
        vertices: Number of vertices, defaults to 32
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    import bmesh
    mesh = bpy.data.meshes.new(name or "Cylinder")
    obj = bpy.data.objects.new(name or "Cylinder", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=vertices,
                          radius1=radius, radius2=radius, depth=depth)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_cone")
def create_cone(
    location: List[float] = None,
    radius1: float = 1.0,
    radius2: float = 0.0,
    depth: float = 2.0,
    vertices: int = 32,
    name: Optional[str] = None
) -> dict:
    """
    Create a cone mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        radius1: Bottom radius, defaults to 1.0
        radius2: Top radius, defaults to 0.0 (point)
        depth: Height of the cone, defaults to 2.0
        vertices: Number of vertices, defaults to 32
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    import bmesh
    mesh = bpy.data.meshes.new(name or "Cone")
    obj = bpy.data.objects.new(name or "Cone", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=vertices,
                          radius1=radius1, radius2=radius2, depth=depth)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_torus")
def create_torus(
    location: List[float] = None,
    major_radius: float = 1.0,
    minor_radius: float = 0.25,
    major_segments: int = 48,
    minor_segments: int = 12,
    name: Optional[str] = None
) -> dict:
    """
    Create a torus mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        major_radius: Major radius (ring), defaults to 1.0
        minor_radius: Minor radius (tube), defaults to 0.25
        major_segments: Segments for the ring, defaults to 48
        minor_segments: Segments for the tube, defaults to 12
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    import bmesh
    import math
    mesh = bpy.data.meshes.new(name or "Torus")
    obj = bpy.data.objects.new(name or "Torus", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=False, radius=minor_radius, segments=minor_segments)
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], axis=(0, 0, 1), 
                   cent=(major_radius, 0, 0), steps=major_segments, angle=math.pi * 2)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_plane")
def create_plane(
    location: List[float] = None,
    size: float = 2.0,
    name: Optional[str] = None
) -> dict:
    """
    Create a plane mesh primitive.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        size: Size of the plane, defaults to 2.0
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    import bmesh
    mesh = bpy.data.meshes.new(name or "Plane")
    obj = bpy.data.objects.new(name or "Plane", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    half = size / 2
    v1 = bm.verts.new((-half, -half, 0))
    v2 = bm.verts.new((half, -half, 0))
    v3 = bm.verts.new((half, half, 0))
    v4 = bm.verts.new((-half, half, 0))
    bm.faces.new([v1, v2, v3, v4])
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = loc
    
    return {
        "object_id": obj.name,
        "type": "MESH",
        "location": list(obj.location),
        "dimensions": list(obj.dimensions),
    }


@handler("create_empty")
def create_empty(
    location: List[float] = None,
    empty_type: str = "PLAIN_AXES",
    name: Optional[str] = None
) -> dict:
    """
    Create an empty object (for grouping/organization).
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 0]
        empty_type: Type of empty display (PLAIN_AXES, ARROWS, SINGLE_ARROW, 
                   CIRCLE, CUBE, SPHERE, CONE, IMAGE)
        name: Optional name for the object
        
    Returns:
        dict with object_id and object info
    """
    loc = tuple(location) if location else (0, 0, 0)
    
    obj = bpy.data.objects.new(name or "Empty", None)
    obj.empty_display_type = empty_type
    obj.location = loc
    bpy.context.collection.objects.link(obj)
    
    return {
        "object_id": obj.name,
        "type": "EMPTY",
        "location": list(obj.location),
        "empty_display_type": obj.empty_display_type,
    }


@handler("get_object")
def get_object(name: str) -> dict:
    """
    Get information about an object by name.
    
    Args:
        name: Name of the object
        
    Returns:
        dict with object information
    """
    obj = bpy.data.objects.get(name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    result = {
        "object_id": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
    }
    
    if obj.type == 'MESH':
        result["vertices"] = len(obj.data.vertices)
        result["faces"] = len(obj.data.polygons)
        result["dimensions"] = list(obj.dimensions)
    
    return result


@handler("list_objects")
def list_objects(object_type: Optional[str] = None) -> dict:
    """
    List all objects in the scene.
    
    Args:
        object_type: Optional filter by type (MESH, CAMERA, LIGHT, etc.)
        
    Returns:
        dict with list of objects
    """
    objects = []
    for obj in bpy.data.objects:
        if object_type is None or obj.type == object_type:
            objects.append({
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
            })
    
    return {"objects": objects, "count": len(objects)}


@handler("delete_object")
def delete_object(name: str) -> dict:
    """
    Delete an object by name.
    
    Args:
        name: Name of the object to delete
        
    Returns:
        dict confirming deletion
    """
    obj = bpy.data.objects.get(name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    bpy.data.objects.remove(obj, do_unlink=True)
    
    return {"deleted": name, "success": True}


@handler("select_object")
def select_object(name: str, add_to_selection: bool = False) -> dict:
    """
    Select an object by name.
    
    Args:
        name: Name of the object to select
        add_to_selection: If True, add to current selection; if False, replace
        
    Returns:
        dict confirming selection
    """
    obj = bpy.data.objects.get(name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    if not add_to_selection:
        bpy.ops.object.select_all(action='DESELECT')
    
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    return {"selected": name, "active": True}


@handler("transform_object")
def transform_object(
    name: str,
    location: List[float] = None,
    rotation: List[float] = None,
    scale: List[float] = None
) -> dict:
    """
    Transform an object (location, rotation, scale).
    
    Args:
        name: Name of the object
        location: New XYZ location [x, y, z]
        rotation: New XYZ rotation in radians [x, y, z]
        scale: New XYZ scale [x, y, z]
        
    Returns:
        dict with updated transform
    """
    obj = bpy.data.objects.get(name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    if location is not None:
        obj.location = tuple(location)
    if rotation is not None:
        obj.rotation_euler = tuple(rotation)
    if scale is not None:
        obj.scale = tuple(scale)
    
    return {
        "object_id": obj.name,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
    }


@handler("duplicate_object")
def duplicate_object(name: str, new_name: Optional[str] = None) -> dict:
    """
    Duplicate an object.
    
    Args:
        name: Name of the object to duplicate
        new_name: Optional name for the new object
        
    Returns:
        dict with new object info
    """
    obj = bpy.data.objects.get(name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    new_obj = obj.copy()
    if obj.data:
        new_obj.data = obj.data.copy()
    
    if new_name:
        new_obj.name = new_name
    
    bpy.context.collection.objects.link(new_obj)
    
    return {
        "object_id": new_obj.name,
        "source": name,
        "type": new_obj.type,
        "location": list(new_obj.location),
    }


@handler("rename_object")
def rename_object(old_name: str, new_name: str) -> dict:
    """
    Rename an object.
    
    Args:
        old_name: Current name of the object
        new_name: New name for the object
        
    Returns:
        dict confirming rename
    """
    obj = bpy.data.objects.get(old_name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(old_name)
    
    obj.name = new_name
    
    return {
        "old_name": old_name,
        "new_name": obj.name,  # May differ if name already exists
        "success": True,
    }
