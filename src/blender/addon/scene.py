"""
Scene Operations
================
Handlers for scene management, cameras, and lights in Blender.
"""

import bpy
from typing import Optional, List
import math

from .handlers import handler


@handler("get_scene_info")
def get_scene_info() -> dict:
    """
    Get full scene information.
    
    Returns:
        dict with scene state including objects, materials, cameras, lights
    """
    scene = bpy.context.scene
    
    objects = []
    cameras = []
    lights = []
    
    for obj in bpy.data.objects:
        obj_info = {
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale),
        }
        
        if obj.type == 'CAMERA':
            cameras.append(obj_info)
        elif obj.type == 'LIGHT':
            obj_info["light_type"] = obj.data.type
            obj_info["energy"] = obj.data.energy
            lights.append(obj_info)
        else:
            objects.append(obj_info)
    
    return {
        "scene_name": scene.name,
        "frame_current": scene.frame_current,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "objects": objects,
        "cameras": cameras,
        "lights": lights,
        "active_camera": scene.camera.name if scene.camera else None,
        "object_count": len(objects),
        "camera_count": len(cameras),
        "light_count": len(lights),
    }


@handler("clear_scene")
def clear_scene(keep_cameras: bool = False, keep_lights: bool = False) -> dict:
    """
    Clear all objects from the scene.
    
    Args:
        keep_cameras: If True, don't delete cameras
        keep_lights: If True, don't delete lights
        
    Returns:
        dict with deletion summary
    """
    deleted = []
    
    for obj in list(bpy.data.objects):
        if keep_cameras and obj.type == 'CAMERA':
            continue
        if keep_lights and obj.type == 'LIGHT':
            continue
        
        deleted.append(obj.name)
        bpy.data.objects.remove(obj, do_unlink=True)
    
    return {
        "deleted": deleted,
        "count": len(deleted),
        "success": True,
    }


@handler("new_scene")
def new_scene(name: str) -> dict:
    """
    Create a new scene.
    
    Args:
        name: Name for the new scene
        
    Returns:
        dict with new scene info
    """
    new_scene = bpy.data.scenes.new(name=name)
    bpy.context.window.scene = new_scene
    
    return {
        "scene_name": new_scene.name,
        "success": True,
    }


@handler("save_scene")
def save_scene(filepath: str) -> dict:
    """
    Save the current scene to a .blend file.
    
    Args:
        filepath: Path to save the file (should end with .blend)
        
    Returns:
        dict confirming save
    """
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    
    return {
        "filepath": filepath,
        "success": True,
    }


@handler("load_scene")
def load_scene(filepath: str) -> dict:
    """
    Load a scene from a .blend file.
    
    Args:
        filepath: Path to the .blend file
        
    Returns:
        dict with loaded scene info
    """
    bpy.ops.wm.open_mainfile(filepath=filepath)
    
    return {
        "filepath": filepath,
        "scene_name": bpy.context.scene.name,
        "success": True,
    }


@handler("add_camera")
def add_camera(
    location: List[float] = None,
    rotation: List[float] = None,
    name: Optional[str] = None,
    lens: float = 50.0
) -> dict:
    """
    Add a camera to the scene.
    
    Args:
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 5]
        rotation: XYZ rotation in radians [x, y, z], defaults to [0, 0, 0]
        name: Optional name for the camera
        lens: Focal length in mm, defaults to 50.0
        
    Returns:
        dict with camera info
    """
    loc = tuple(location) if location else (0, 0, 5)
    rot = tuple(rotation) if rotation else (0, 0, 0)
    
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = bpy.context.active_object
    
    if name:
        camera.name = name
    
    camera.data.lens = lens
    
    return {
        "object_id": camera.name,
        "type": "CAMERA",
        "location": list(camera.location),
        "rotation": list(camera.rotation_euler),
        "lens": camera.data.lens,
    }


@handler("add_light")
def add_light(
    light_type: str = "POINT",
    location: List[float] = None,
    energy: float = 1000.0,
    color: List[float] = None,
    name: Optional[str] = None
) -> dict:
    """
    Add a light to the scene.
    
    Args:
        light_type: Type of light (POINT, SUN, SPOT, AREA)
        location: XYZ coordinates [x, y, z], defaults to [0, 0, 5]
        energy: Light energy/power, defaults to 1000.0
        color: RGB color [r, g, b], values 0-1, defaults to [1, 1, 1]
        name: Optional name for the light
        
    Returns:
        dict with light info
    """
    loc = tuple(location) if location else (0, 0, 5)
    
    bpy.ops.object.light_add(type=light_type, location=loc)
    light = bpy.context.active_object
    
    if name:
        light.name = name
    
    light.data.energy = energy
    
    if color:
        light.data.color = tuple(color[:3])
    
    return {
        "object_id": light.name,
        "type": "LIGHT",
        "light_type": light_type,
        "location": list(light.location),
        "energy": light.data.energy,
        "color": list(light.data.color),
    }


@handler("set_active_camera")
def set_active_camera(name: str) -> dict:
    """
    Set the active camera for rendering.
    
    Args:
        name: Name of the camera object
        
    Returns:
        dict confirming camera set
    """
    camera = bpy.data.objects.get(name)
    if camera is None:
        from common.exceptions import ObjectNotFoundError
        raise ObjectNotFoundError(name)
    
    if camera.type != 'CAMERA':
        from common.exceptions import CommandError
        raise CommandError(f"Object '{name}' is not a camera")
    
    bpy.context.scene.camera = camera
    
    return {
        "active_camera": name,
        "success": True,
    }


@handler("set_frame")
def set_frame(frame: int) -> dict:
    """
    Set the current frame.
    
    Args:
        frame: Frame number to set
        
    Returns:
        dict with frame info
    """
    bpy.context.scene.frame_set(frame)
    
    return {
        "frame": frame,
        "success": True,
    }


@handler("set_frame_range")
def set_frame_range(start: int, end: int) -> dict:
    """
    Set the frame range for animation.
    
    Args:
        start: Start frame
        end: End frame
        
    Returns:
        dict with frame range info
    """
    bpy.context.scene.frame_start = start
    bpy.context.scene.frame_end = end
    
    return {
        "frame_start": start,
        "frame_end": end,
        "success": True,
    }
