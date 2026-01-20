"""
FreeCAD Boolean Operations Handlers

Handlers for boolean operations (union, subtract, intersect).
"""

from typing import Optional, List, Dict, Any
from .handlers import handler


def _ensure_document():
    """Ensure a document exists."""
    import FreeCAD
    if FreeCAD.ActiveDocument is None:
        FreeCAD.newDocument("Unnamed")
    return FreeCAD.ActiveDocument


def _get_object(name: str):
    """Get an object by name, raising error if not found."""
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(name)
        
    obj = doc.getObject(name)
    if obj is None:
        raise ObjectNotFoundError(name)
        
    return obj


def _add_object_to_doc(shape, name: str, doc=None):
    """Add a shape to the document as a Part::Feature."""
    import FreeCAD
    
    if doc is None:
        doc = _ensure_document()
        
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    doc.recompute()
    
    return obj


def _get_bounding_box(shape) -> dict:
    """Get bounding box of a shape."""
    bb = shape.BoundBox
    return {
        "min": [bb.XMin, bb.YMin, bb.ZMin],
        "max": [bb.XMax, bb.YMax, bb.ZMax],
        "size": [bb.XLength, bb.YLength, bb.ZLength]
    }


@handler("boolean_union")
def boolean_union(
    object1: str,
    object2: str,
    name: str = "Union",
    delete_originals: bool = False
) -> dict:
    """
    Perform boolean union (fuse) of two objects.
    
    Args:
        object1: First object name
        object2: Second object name
        name: Name for the result object
        delete_originals: Whether to delete the original objects
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    
    obj1 = _get_object(object1)
    obj2 = _get_object(object2)
    
    result_shape = obj1.Shape.fuse(obj2.Shape)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    if delete_originals:
        doc.removeObject(object1)
        doc.removeObject(object2)
        doc.recompute()
    
    return {
        "object_id": result_obj.Name,
        "type": "Union",
        "inputs": [object1, object2],
        "bounding_box": _get_bounding_box(result_obj.Shape),
        "volume": result_obj.Shape.Volume
    }


@handler("boolean_subtract")
def boolean_subtract(
    base: str,
    tool: str,
    name: str = "Subtract",
    delete_originals: bool = False
) -> dict:
    """
    Perform boolean subtraction (cut) of two objects.
    
    Args:
        base: Base object name (to cut from)
        tool: Tool object name (to cut with)
        name: Name for the result object
        delete_originals: Whether to delete the original objects
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    
    base_obj = _get_object(base)
    tool_obj = _get_object(tool)
    
    result_shape = base_obj.Shape.cut(tool_obj.Shape)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    if delete_originals:
        doc.removeObject(base)
        doc.removeObject(tool)
        doc.recompute()
    
    return {
        "object_id": result_obj.Name,
        "type": "Subtract",
        "base": base,
        "tool": tool,
        "bounding_box": _get_bounding_box(result_obj.Shape),
        "volume": result_obj.Shape.Volume
    }


@handler("boolean_intersect")
def boolean_intersect(
    object1: str,
    object2: str,
    name: str = "Intersect",
    delete_originals: bool = False
) -> dict:
    """
    Perform boolean intersection (common) of two objects.
    
    Args:
        object1: First object name
        object2: Second object name
        name: Name for the result object
        delete_originals: Whether to delete the original objects
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    
    obj1 = _get_object(object1)
    obj2 = _get_object(object2)
    
    result_shape = obj1.Shape.common(obj2.Shape)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    if delete_originals:
        doc.removeObject(object1)
        doc.removeObject(object2)
        doc.recompute()
    
    return {
        "object_id": result_obj.Name,
        "type": "Intersect",
        "inputs": [object1, object2],
        "bounding_box": _get_bounding_box(result_obj.Shape),
        "volume": result_obj.Shape.Volume
    }


@handler("multi_union")
def multi_union(
    objects: List[str],
    name: str = "MultiUnion",
    delete_originals: bool = False
) -> dict:
    """
    Perform boolean union of multiple objects.
    
    Args:
        objects: List of object names to union
        name: Name for the result object
        delete_originals: Whether to delete the original objects
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    if len(objects) < 2:
        raise ValueError("At least 2 objects required for multi_union")
        
    doc = _ensure_document()
    
    # Start with first object
    result_shape = _get_object(objects[0]).Shape.copy()
    
    # Fuse with remaining objects
    for obj_name in objects[1:]:
        obj = _get_object(obj_name)
        result_shape = result_shape.fuse(obj.Shape)
        
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    if delete_originals:
        for obj_name in objects:
            doc.removeObject(obj_name)
        doc.recompute()
    
    return {
        "object_id": result_obj.Name,
        "type": "MultiUnion",
        "inputs": objects,
        "bounding_box": _get_bounding_box(result_obj.Shape),
        "volume": result_obj.Shape.Volume
    }


@handler("multi_subtract")
def multi_subtract(
    base: str,
    tools: List[str],
    name: str = "MultiSubtract",
    delete_originals: bool = False
) -> dict:
    """
    Perform boolean subtraction of multiple tools from a base.
    
    Args:
        base: Base object name
        tools: List of tool object names to subtract
        name: Name for the result object
        delete_originals: Whether to delete the original objects
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    if len(tools) < 1:
        raise ValueError("At least 1 tool required for multi_subtract")
        
    doc = _ensure_document()
    
    # Start with base object
    result_shape = _get_object(base).Shape.copy()
    
    # Cut with each tool
    for tool_name in tools:
        tool_obj = _get_object(tool_name)
        result_shape = result_shape.cut(tool_obj.Shape)
        
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    if delete_originals:
        doc.removeObject(base)
        for tool_name in tools:
            doc.removeObject(tool_name)
        doc.recompute()
    
    return {
        "object_id": result_obj.Name,
        "type": "MultiSubtract",
        "base": base,
        "tools": tools,
        "bounding_box": _get_bounding_box(result_obj.Shape),
        "volume": result_obj.Shape.Volume
    }


@handler("extrude")
def extrude(
    object_name: str,
    direction: List[float],
    length: float,
    name: str = "Extrude"
) -> dict:
    """
    Extrude a shape along a direction.
    
    Args:
        object_name: Object to extrude
        direction: [x, y, z] direction vector
        length: Extrusion length
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    # Normalize direction and scale by length
    dir_vec = FreeCAD.Vector(*direction)
    dir_vec.normalize()
    dir_vec = dir_vec * length
    
    result_shape = obj.Shape.extrude(dir_vec)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Extrude",
        "source": object_name,
        "direction": direction,
        "length": length,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }


@handler("revolve")
def revolve(
    object_name: str,
    axis: List[float] = None,
    axis_point: List[float] = None,
    angle: float = 360.0,
    name: str = "Revolve"
) -> dict:
    """
    Revolve a shape around an axis.
    
    Args:
        object_name: Object to revolve
        axis: [x, y, z] axis direction (default Z)
        axis_point: [x, y, z] point on axis (default origin)
        angle: Revolution angle in degrees
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    axis_vec = FreeCAD.Vector(*(axis or [0, 0, 1]))
    point_vec = FreeCAD.Vector(*(axis_point or [0, 0, 0]))
    
    result_shape = obj.Shape.revolve(point_vec, axis_vec, angle)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Revolve",
        "source": object_name,
        "angle": angle,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }


@handler("fillet")
def fillet(
    object_name: str,
    radius: float,
    edge_indices: Optional[List[int]] = None,
    name: str = "Fillet"
) -> dict:
    """
    Apply fillet to edges of an object.
    
    Args:
        object_name: Object to fillet
        radius: Fillet radius
        edge_indices: Optional list of edge indices (all edges if None)
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    if edge_indices is None:
        edges = obj.Shape.Edges
    else:
        edges = [obj.Shape.Edges[i] for i in edge_indices]
        
    result_shape = obj.Shape.makeFillet(radius, edges)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Fillet",
        "source": object_name,
        "radius": radius,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }


@handler("chamfer")
def chamfer(
    object_name: str,
    size: float,
    edge_indices: Optional[List[int]] = None,
    name: str = "Chamfer"
) -> dict:
    """
    Apply chamfer to edges of an object.
    
    Args:
        object_name: Object to chamfer
        size: Chamfer size
        edge_indices: Optional list of edge indices (all edges if None)
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    if edge_indices is None:
        edges = obj.Shape.Edges
    else:
        edges = [obj.Shape.Edges[i] for i in edge_indices]
        
    result_shape = obj.Shape.makeChamfer(size, edges)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Chamfer",
        "source": object_name,
        "size": size,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }


@handler("mirror")
def mirror(
    object_name: str,
    plane: str = "XY",
    name: str = "Mirror"
) -> dict:
    """
    Mirror an object across a plane.
    
    Args:
        object_name: Object to mirror
        plane: Plane to mirror across (XY, XZ, YZ)
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    # Define mirror planes
    planes = {
        "XY": (FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1)),
        "XZ": (FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0)),
        "YZ": (FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0)),
    }
    
    if plane.upper() not in planes:
        raise ValueError(f"Invalid plane: {plane}. Use XY, XZ, or YZ")
        
    point, normal = planes[plane.upper()]
    result_shape = obj.Shape.mirror(point, normal)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Mirror",
        "source": object_name,
        "plane": plane,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }


@handler("offset")
def offset(
    object_name: str,
    distance: float,
    name: str = "Offset"
) -> dict:
    """
    Offset (shell) an object by a distance.
    
    Args:
        object_name: Object to offset
        distance: Offset distance (positive = outward)
        name: Name for the result object
        
    Returns:
        dict with result object info
    """
    import FreeCAD
    
    doc = _ensure_document()
    obj = _get_object(object_name)
    
    result_shape = obj.Shape.makeOffsetShape(distance, 0.01)
    result_obj = _add_object_to_doc(result_shape, name, doc)
    
    return {
        "object_id": result_obj.Name,
        "type": "Offset",
        "source": object_name,
        "distance": distance,
        "bounding_box": _get_bounding_box(result_obj.Shape)
    }
