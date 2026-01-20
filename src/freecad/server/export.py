"""
FreeCAD Export/Import Operations Handlers

Handlers for exporting and importing various file formats.
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


def _get_objects_or_all(object_names: Optional[List[str]] = None):
    """Get specified objects or all objects in document."""
    import FreeCAD
    
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return []
        
    if object_names:
        return [_get_object(name) for name in object_names]
    else:
        return [obj for obj in doc.Objects if hasattr(obj, 'Shape')]


@handler("export_step")
def export_step(
    filepath: str,
    objects: Optional[List[str]] = None
) -> dict:
    """
    Export objects to STEP format.
    
    Args:
        filepath: Output file path (.step or .stp)
        objects: List of object names (all if None)
        
    Returns:
        dict with export info
    """
    import Part
    
    objs = _get_objects_or_all(objects)
    if not objs:
        return {"success": False, "message": "No objects to export"}
        
    shapes = [obj.Shape for obj in objs]
    Part.export(shapes, filepath)
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "STEP",
        "object_count": len(objs),
        "objects": [obj.Name for obj in objs]
    }


@handler("export_iges")
def export_iges(
    filepath: str,
    objects: Optional[List[str]] = None
) -> dict:
    """
    Export objects to IGES format.
    
    Args:
        filepath: Output file path (.iges or .igs)
        objects: List of object names (all if None)
        
    Returns:
        dict with export info
    """
    import Part
    
    objs = _get_objects_or_all(objects)
    if not objs:
        return {"success": False, "message": "No objects to export"}
        
    shapes = [obj.Shape for obj in objs]
    Part.export(shapes, filepath)
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "IGES",
        "object_count": len(objs),
        "objects": [obj.Name for obj in objs]
    }


@handler("export_stl")
def export_stl(
    filepath: str,
    objects: Optional[List[str]] = None,
    tolerance: float = 0.1
) -> dict:
    """
    Export objects to STL format.
    
    Args:
        filepath: Output file path (.stl)
        objects: List of object names (all if None)
        tolerance: Mesh tolerance for tessellation
        
    Returns:
        dict with export info
    """
    import Mesh
    
    objs = _get_objects_or_all(objects)
    if not objs:
        return {"success": False, "message": "No objects to export"}
        
    # Create mesh from shapes using Mesh.export
    shapes = []
    for obj in objs:
        if hasattr(obj, 'Shape') and obj.Shape.isValid():
            shapes.append(obj)
            
    if shapes:
        Mesh.export(shapes, filepath)
    else:
        return {"success": False, "message": "No valid shapes to export"}
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "STL",
        "object_count": len(objs),
        "objects": [obj.Name for obj in objs]
    }


@handler("export_obj")
def export_obj(
    filepath: str,
    objects: Optional[List[str]] = None,
    tolerance: float = 0.1
) -> dict:
    """
    Export objects to OBJ format.
    
    Args:
        filepath: Output file path (.obj)
        objects: List of object names (all if None)
        tolerance: Mesh tolerance for tessellation
        
    Returns:
        dict with export info
    """
    import Mesh
    
    objs = _get_objects_or_all(objects)
    if not objs:
        return {"success": False, "message": "No objects to export"}
        
    # Create mesh from shapes
    meshes = []
    for obj in objs:
        if hasattr(obj, 'Shape'):
            mesh = Mesh.Mesh(obj.Shape.tessellate(tolerance)[0])
            meshes.append(mesh)
            
    if meshes:
        combined = meshes[0]
        for m in meshes[1:]:
            combined.addMesh(m)
        combined.write(filepath)
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "OBJ",
        "object_count": len(objs),
        "objects": [obj.Name for obj in objs]
    }


@handler("export_brep")
def export_brep(
    filepath: str,
    objects: Optional[List[str]] = None
) -> dict:
    """
    Export objects to BREP format.
    
    Args:
        filepath: Output file path (.brep or .brp)
        objects: List of object names (all if None)
        
    Returns:
        dict with export info
    """
    import Part
    
    objs = _get_objects_or_all(objects)
    if not objs:
        return {"success": False, "message": "No objects to export"}
        
    # Combine shapes if multiple
    if len(objs) == 1:
        shape = objs[0].Shape
    else:
        compound = Part.makeCompound([obj.Shape for obj in objs])
        shape = compound
        
    shape.exportBrep(filepath)
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "BREP",
        "object_count": len(objs),
        "objects": [obj.Name for obj in objs]
    }


@handler("import_step")
def import_step(filepath: str) -> dict:
    """
    Import objects from STEP file.
    
    Args:
        filepath: Input file path (.step or .stp)
        
    Returns:
        dict with import info
    """
    import FreeCAD
    import Part
    
    doc = _ensure_document()
    
    # Import STEP file
    shape = Part.Shape()
    shape.read(filepath)
    
    # Add to document
    obj = doc.addObject("Part::Feature", "ImportedSTEP")
    obj.Shape = shape
    doc.recompute()
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "STEP",
        "object_id": obj.Name
    }


@handler("import_stl")
def import_stl(filepath: str, name: str = "ImportedSTL") -> dict:
    """
    Import mesh from STL file.
    
    Args:
        filepath: Input file path (.stl)
        name: Name for the imported object
        
    Returns:
        dict with import info
    """
    import FreeCAD
    import Mesh
    
    doc = _ensure_document()
    
    # Import STL as mesh
    mesh = Mesh.Mesh(filepath)
    obj = doc.addObject("Mesh::Feature", name)
    obj.Mesh = mesh
    doc.recompute()
    
    return {
        "success": True,
        "filepath": filepath,
        "format": "STL",
        "object_id": obj.Name,
        "vertex_count": mesh.CountPoints,
        "face_count": mesh.CountFacets
    }


@handler("execute_python")
def execute_python(code: str) -> dict:
    """
    Execute arbitrary Python code in FreeCAD context.
    
    Args:
        code: Python code to execute
        
    Returns:
        dict with execution result
    """
    import FreeCAD
    import Part
    import sys
    from io import StringIO
    
    # Capture stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    
    result = None
    error = None
    
    try:
        # Create execution context
        exec_globals = {
            'FreeCAD': FreeCAD,
            'Part': Part,
            'App': FreeCAD,
            '__builtins__': __builtins__,
        }
        
        # Try to import optional modules
        try:
            import Mesh
            exec_globals['Mesh'] = Mesh
        except:
            pass
            
        try:
            import Draft
            exec_globals['Draft'] = Draft
        except:
            pass
        
        # Execute code
        exec(code, exec_globals)
        result = exec_globals.get('result', None)
        
    except Exception as e:
        error = str(e)
    finally:
        stdout_output = sys.stdout.getvalue()
        stderr_output = sys.stderr.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    response = {
        "success": error is None,
        "stdout": stdout_output,
        "stderr": stderr_output,
    }
    
    if error:
        response["error"] = error
    if result is not None:
        response["result"] = str(result)
        
    return response
