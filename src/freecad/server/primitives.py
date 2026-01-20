"""
FreeCAD Part Primitives Handlers

Handlers for creating Part primitives (Box, Sphere, Cylinder, etc.).
"""

from typing import Optional, List, Dict, Any
from .handlers import handler


def _ensure_document():
    """Ensure a document exists."""
    import FreeCAD
    if FreeCAD.ActiveDocument is None:
        FreeCAD.newDocument("Unnamed")
    return FreeCAD.ActiveDocument


def _add_object_to_doc(shape, name: str, doc=None):
    """Add a shape to the document as a Part::Feature."""
    import FreeCAD
    
    if doc is None:
        doc = _ensure_document()
        
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    doc.recompute()
    
    return obj


@handler("create_box")
def create_box(
    length: float = 10.0,
    width: float = 10.0,
    height: float = 10.0,
    position: Optional[List[float]] = None,
    name: str = "Box"
) -> dict:
    """
    Create a box primitive.
    
    Args:
        length: Length (X dimension)
        width: Width (Y dimension)
        height: Height (Z dimension)
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    box = Part.makeBox(length, width, height)
    
    if position:
        box.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(box, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Box",
        "dimensions": {"length": length, "width": width, "height": height},
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_sphere")
def create_sphere(
    radius: float = 5.0,
    position: Optional[List[float]] = None,
    name: str = "Sphere"
) -> dict:
    """
    Create a sphere primitive.
    
    Args:
        radius: Sphere radius
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    sphere = Part.makeSphere(radius)
    
    if position:
        sphere.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(sphere, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Sphere",
        "radius": radius,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_cylinder")
def create_cylinder(
    radius: float = 5.0,
    height: float = 10.0,
    position: Optional[List[float]] = None,
    name: str = "Cylinder"
) -> dict:
    """
    Create a cylinder primitive.
    
    Args:
        radius: Cylinder radius
        height: Cylinder height
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    cylinder = Part.makeCylinder(radius, height)
    
    if position:
        cylinder.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(cylinder, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Cylinder",
        "radius": radius,
        "height": height,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_cone")
def create_cone(
    radius1: float = 5.0,
    radius2: float = 0.0,
    height: float = 10.0,
    position: Optional[List[float]] = None,
    name: str = "Cone"
) -> dict:
    """
    Create a cone primitive.
    
    Args:
        radius1: Bottom radius
        radius2: Top radius (0 for point)
        height: Cone height
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    cone = Part.makeCone(radius1, radius2, height)
    
    if position:
        cone.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(cone, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Cone",
        "radius1": radius1,
        "radius2": radius2,
        "height": height,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_torus")
def create_torus(
    radius1: float = 10.0,
    radius2: float = 2.0,
    position: Optional[List[float]] = None,
    name: str = "Torus"
) -> dict:
    """
    Create a torus primitive.
    
    Args:
        radius1: Major radius (ring)
        radius2: Minor radius (tube)
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    torus = Part.makeTorus(radius1, radius2)
    
    if position:
        torus.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(torus, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Torus",
        "radius1": radius1,
        "radius2": radius2,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_plane")
def create_plane(
    length: float = 10.0,
    width: float = 10.0,
    position: Optional[List[float]] = None,
    name: str = "Plane"
) -> dict:
    """
    Create a plane (face) primitive.
    
    Args:
        length: Length (X dimension)
        width: Width (Y dimension)
        position: Optional [x, y, z] position
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    plane = Part.makePlane(length, width)
    
    if position:
        plane.translate(FreeCAD.Vector(*position))
        
    obj = _add_object_to_doc(plane, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Plane",
        "length": length,
        "width": width,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_wedge")
def create_wedge(
    xmin: float = 0.0,
    ymin: float = 0.0,
    zmin: float = 0.0,
    x2min: float = 2.0,
    z2min: float = 2.0,
    xmax: float = 10.0,
    ymax: float = 10.0,
    zmax: float = 10.0,
    x2max: float = 8.0,
    z2max: float = 8.0,
    name: str = "Wedge"
) -> dict:
    """
    Create a wedge primitive.
    
    Args:
        Various wedge parameters
        name: Object name
        
    Returns:
        dict with object info
    """
    import Part
    
    doc = _ensure_document()
    
    wedge = Part.makeWedge(xmin, ymin, zmin, x2min, z2min, xmax, ymax, zmax, x2max, z2max)
    obj = _add_object_to_doc(wedge, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Wedge",
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("create_helix")
def create_helix(
    pitch: float = 5.0,
    height: float = 20.0,
    radius: float = 5.0,
    name: str = "Helix"
) -> dict:
    """
    Create a helix curve.
    
    Args:
        pitch: Distance between turns
        height: Total height
        radius: Helix radius
        name: Object name
        
    Returns:
        dict with object info
    """
    import Part
    
    doc = _ensure_document()
    
    helix = Part.makeHelix(pitch, height, radius)
    obj = _add_object_to_doc(helix, name, doc)
    
    return {
        "object_id": obj.Name,
        "type": "Helix",
        "pitch": pitch,
        "height": height,
        "radius": radius,
        "bounding_box": _get_bounding_box(obj.Shape)
    }


@handler("get_object")
def get_object(name: str) -> dict:
    """
    Get information about an object by name.
    
    Args:
        name: Object name
        
    Returns:
        dict with object info
    """
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(name)
        
    obj = doc.getObject(name)
    if obj is None:
        raise ObjectNotFoundError(name)
        
    result = {
        "name": obj.Name,
        "label": obj.Label,
        "type": obj.TypeId,
    }
    
    if hasattr(obj, 'Shape'):
        result["bounding_box"] = _get_bounding_box(obj.Shape)
        result["volume"] = obj.Shape.Volume if hasattr(obj.Shape, 'Volume') else None
        result["area"] = obj.Shape.Area if hasattr(obj.Shape, 'Area') else None
        
    if hasattr(obj, 'Placement'):
        result["placement"] = {
            "position": list(obj.Placement.Base),
            "rotation": list(obj.Placement.Rotation.Q)
        }
        
    return result


@handler("list_objects")
def list_objects() -> dict:
    """
    List all objects in the active document.
    
    Returns:
        dict with list of objects
    """
    import FreeCAD
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return {"objects": [], "count": 0}
        
    objects = []
    for obj in doc.Objects:
        obj_info = {
            "name": obj.Name,
            "label": obj.Label,
            "type": obj.TypeId
        }
        objects.append(obj_info)
        
    return {
        "objects": objects,
        "count": len(objects)
    }


@handler("delete_object")
def delete_object(name: str) -> dict:
    """
    Delete an object by name.
    
    Args:
        name: Object name to delete
        
    Returns:
        dict with success status
    """
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(name)
        
    obj = doc.getObject(name)
    if obj is None:
        raise ObjectNotFoundError(name)
        
    doc.removeObject(name)
    doc.recompute()
    
    return {
        "success": True,
        "deleted": name
    }


@handler("rename_object")
def rename_object(old_name: str, new_name: str) -> dict:
    """
    Rename an object.
    
    Args:
        old_name: Current object name
        new_name: New name for the object
        
    Returns:
        dict with success status
    """
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(old_name)
        
    obj = doc.getObject(old_name)
    if obj is None:
        raise ObjectNotFoundError(old_name)
        
    obj.Label = new_name
    
    return {
        "success": True,
        "old_name": old_name,
        "new_name": obj.Label
    }


@handler("copy_object")
def copy_object(name: str, new_name: str) -> dict:
    """
    Copy an object.
    
    Args:
        name: Object to copy
        new_name: Name for the copy
        
    Returns:
        dict with new object info
    """
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(name)
        
    obj = doc.getObject(name)
    if obj is None:
        raise ObjectNotFoundError(name)
        
    if hasattr(obj, 'Shape'):
        new_obj = _add_object_to_doc(obj.Shape.copy(), new_name, doc)
    else:
        raise ValueError(f"Object '{name}' cannot be copied")
        
    return {
        "success": True,
        "original": name,
        "copy": new_obj.Name
    }


@handler("set_placement")
def set_placement(
    name: str,
    position: Optional[List[float]] = None,
    rotation: Optional[List[float]] = None
) -> dict:
    """
    Set object placement (position and rotation).
    
    Args:
        name: Object name
        position: [x, y, z] position
        rotation: [x, y, z, w] quaternion or [x, y, z] euler angles
        
    Returns:
        dict with success status
    """
    import FreeCAD
    from common.exceptions import ObjectNotFoundError
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise ObjectNotFoundError(name)
        
    obj = doc.getObject(name)
    if obj is None:
        raise ObjectNotFoundError(name)
        
    placement = obj.Placement
    
    if position:
        placement.Base = FreeCAD.Vector(*position)
        
    if rotation:
        if len(rotation) == 4:
            # Quaternion
            placement.Rotation = FreeCAD.Rotation(*rotation)
        elif len(rotation) == 3:
            # Euler angles (degrees)
            placement.Rotation = FreeCAD.Rotation(
                FreeCAD.Vector(1, 0, 0), rotation[0]
            ).multiply(FreeCAD.Rotation(
                FreeCAD.Vector(0, 1, 0), rotation[1]
            )).multiply(FreeCAD.Rotation(
                FreeCAD.Vector(0, 0, 1), rotation[2]
            ))
            
    obj.Placement = placement
    doc.recompute()
    
    return {
        "success": True,
        "object": name,
        "position": list(obj.Placement.Base),
        "rotation": list(obj.Placement.Rotation.Q)
    }


def _get_bounding_box(shape) -> dict:
    """Get bounding box of a shape."""
    bb = shape.BoundBox
    return {
        "min": [bb.XMin, bb.YMin, bb.ZMin],
        "max": [bb.XMax, bb.YMax, bb.ZMax],
        "size": [bb.XLength, bb.YLength, bb.ZLength]
    }
