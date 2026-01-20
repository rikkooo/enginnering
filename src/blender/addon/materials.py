"""
Material Operations
===================
Handlers for creating and managing materials in Blender.
"""

import bpy
from typing import Optional, List

from .handlers import handler


@handler("create_material")
def create_material(
    name: str,
    color: List[float] = None,
    metallic: float = 0.0,
    roughness: float = 0.5
) -> dict:
    """
    Create a new material.
    
    Args:
        name: Name for the material
        color: RGBA color [r, g, b, a], values 0-1, defaults to [0.8, 0.8, 0.8, 1.0]
        metallic: Metallic value 0-1, defaults to 0.0
        roughness: Roughness value 0-1, defaults to 0.5
        
    Returns:
        dict with material info
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Get the Principled BSDF node
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if color:
            bsdf.inputs["Base Color"].default_value = tuple(color) if len(color) == 4 else (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    
    return {
        "material_name": mat.name,
        "color": list(bsdf.inputs["Base Color"].default_value) if bsdf else None,
        "metallic": metallic,
        "roughness": roughness,
    }


@handler("apply_material")
def apply_material(object_name: str, material_name: str) -> dict:
    """
    Apply a material to an object.
    
    Args:
        object_name: Name of the object
        material_name: Name of the material to apply
        
    Returns:
        dict confirming application
    """
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(object_name)
    
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        from common.exceptions import MaterialNotFoundError
        raise MaterialNotFoundError(material_name)
    
    if obj.data is None:
        from common.exceptions import CommandError
        raise CommandError(f"Object '{object_name}' has no data to apply material to")
    
    # Clear existing materials and add new one
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    
    return {
        "object": object_name,
        "material": material_name,
        "success": True,
    }


@handler("set_material_color")
def set_material_color(material_name: str, color: List[float]) -> dict:
    """
    Set the base color of a material.
    
    Args:
        material_name: Name of the material
        color: RGBA color [r, g, b, a], values 0-1
        
    Returns:
        dict with updated color
    """
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        from common.exceptions import MaterialNotFoundError
        raise MaterialNotFoundError(material_name)
    
    if not mat.use_nodes:
        mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        rgba = tuple(color) if len(color) == 4 else (*color, 1.0)
        bsdf.inputs["Base Color"].default_value = rgba
    
    return {
        "material_name": material_name,
        "color": list(color),
        "success": True,
    }


@handler("set_material_metallic")
def set_material_metallic(material_name: str, value: float) -> dict:
    """
    Set the metallic value of a material.
    
    Args:
        material_name: Name of the material
        value: Metallic value 0-1
        
    Returns:
        dict with updated value
    """
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        from common.exceptions import MaterialNotFoundError
        raise MaterialNotFoundError(material_name)
    
    if not mat.use_nodes:
        mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Metallic"].default_value = value
    
    return {
        "material_name": material_name,
        "metallic": value,
        "success": True,
    }


@handler("set_material_roughness")
def set_material_roughness(material_name: str, value: float) -> dict:
    """
    Set the roughness value of a material.
    
    Args:
        material_name: Name of the material
        value: Roughness value 0-1
        
    Returns:
        dict with updated value
    """
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        from common.exceptions import MaterialNotFoundError
        raise MaterialNotFoundError(material_name)
    
    if not mat.use_nodes:
        mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Roughness"].default_value = value
    
    return {
        "material_name": material_name,
        "roughness": value,
        "success": True,
    }


@handler("list_materials")
def list_materials() -> dict:
    """
    List all materials in the scene.
    
    Returns:
        dict with list of materials
    """
    materials = []
    for mat in bpy.data.materials:
        mat_info = {
            "name": mat.name,
            "use_nodes": mat.use_nodes,
        }
        
        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                mat_info["color"] = list(bsdf.inputs["Base Color"].default_value)
                mat_info["metallic"] = bsdf.inputs["Metallic"].default_value
                mat_info["roughness"] = bsdf.inputs["Roughness"].default_value
        
        materials.append(mat_info)
    
    return {"materials": materials, "count": len(materials)}


@handler("delete_material")
def delete_material(name: str) -> dict:
    """
    Delete a material by name.
    
    Args:
        name: Name of the material to delete
        
    Returns:
        dict confirming deletion
    """
    mat = bpy.data.materials.get(name)
    if mat is None:
        from common.exceptions import MaterialNotFoundError
        raise MaterialNotFoundError(name)
    
    bpy.data.materials.remove(mat)
    
    return {"deleted": name, "success": True}
