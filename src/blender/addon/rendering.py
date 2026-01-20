"""
Rendering Operations
====================
Handlers for rendering and export operations in Blender.
"""

import bpy
import os
from typing import Optional, List

from .handlers import handler


@handler("set_render_engine")
def set_render_engine(engine: str = "CYCLES") -> dict:
    """
    Set the render engine.
    
    Args:
        engine: Render engine name (CYCLES, BLENDER_EEVEE, BLENDER_WORKBENCH)
        
    Returns:
        dict with engine info
    """
    valid_engines = ['CYCLES', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH']
    
    if engine not in valid_engines:
        from common.exceptions import ValidationError
        raise ValidationError(f"Invalid engine. Must be one of: {valid_engines}")
    
    bpy.context.scene.render.engine = engine
    
    return {
        "engine": engine,
        "success": True,
    }


@handler("set_render_resolution")
def set_render_resolution(width: int, height: int, percentage: int = 100) -> dict:
    """
    Set the render resolution.
    
    Args:
        width: Resolution width in pixels
        height: Resolution height in pixels
        percentage: Resolution percentage (1-100), defaults to 100
        
    Returns:
        dict with resolution info
    """
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.context.scene.render.resolution_percentage = percentage
    
    return {
        "width": width,
        "height": height,
        "percentage": percentage,
        "success": True,
    }


@handler("set_render_samples")
def set_render_samples(samples: int) -> dict:
    """
    Set the number of render samples.
    
    Args:
        samples: Number of samples for rendering
        
    Returns:
        dict with samples info
    """
    engine = bpy.context.scene.render.engine
    
    if engine == 'CYCLES':
        bpy.context.scene.cycles.samples = samples
    elif engine in ['BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT']:
        bpy.context.scene.eevee.taa_render_samples = samples
    
    return {
        "samples": samples,
        "engine": engine,
        "success": True,
    }


@handler("render_image")
def render_image(
    output_path: str,
    file_format: str = "PNG",
    write_still: bool = True
) -> dict:
    """
    Render the current scene to an image file.
    
    Args:
        output_path: Path to save the rendered image
        file_format: Image format (PNG, JPEG, OPEN_EXR, etc.)
        write_still: Whether to write the image to disk
        
    Returns:
        dict with render info
    """
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Set output settings
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = file_format
    
    # Render
    bpy.ops.render.render(write_still=write_still)
    
    return {
        "output_path": output_path,
        "file_format": file_format,
        "resolution": [
            bpy.context.scene.render.resolution_x,
            bpy.context.scene.render.resolution_y
        ],
        "success": True,
    }


@handler("render_animation")
def render_animation(
    output_path: str,
    start_frame: Optional[int] = None,
    end_frame: Optional[int] = None,
    file_format: str = "PNG"
) -> dict:
    """
    Render an animation sequence.
    
    Args:
        output_path: Base path for output files (frame number will be appended)
        start_frame: Start frame (uses scene default if not specified)
        end_frame: End frame (uses scene default if not specified)
        file_format: Image format for frames
        
    Returns:
        dict with animation render info
    """
    scene = bpy.context.scene
    
    # Set frame range if specified
    if start_frame is not None:
        scene.frame_start = start_frame
    if end_frame is not None:
        scene.frame_end = end_frame
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Set output settings
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = file_format
    
    # Render animation
    bpy.ops.render.render(animation=True)
    
    return {
        "output_path": output_path,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "frame_count": scene.frame_end - scene.frame_start + 1,
        "success": True,
    }


@handler("get_render_progress")
def get_render_progress() -> dict:
    """
    Get the current render progress.
    
    Returns:
        dict with render progress info
    """
    # Note: This is a simplified version. Real progress tracking
    # requires more complex integration with Blender's render system.
    return {
        "status": "idle",
        "progress": 0.0,
        "message": "No render in progress",
    }


@handler("export_obj")
def export_obj(filepath: str, objects: Optional[List[str]] = None) -> dict:
    """
    Export objects to OBJ format.
    
    Args:
        filepath: Path to save the OBJ file
        objects: List of object names to export (all if None)
        
    Returns:
        dict with export info
    """
    # Ensure directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Select objects to export
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for name in objects:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        export_selected = True
    else:
        export_selected = False
    
    bpy.ops.wm.obj_export(
        filepath=filepath,
        export_selected_objects=export_selected
    )
    
    return {
        "filepath": filepath,
        "format": "OBJ",
        "objects": objects or "all",
        "success": True,
    }


@handler("export_fbx")
def export_fbx(filepath: str, objects: Optional[List[str]] = None) -> dict:
    """
    Export objects to FBX format.
    
    Args:
        filepath: Path to save the FBX file
        objects: List of object names to export (all if None)
        
    Returns:
        dict with export info
    """
    # Ensure directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Select objects to export
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for name in objects:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        use_selection = True
    else:
        use_selection = False
    
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=use_selection
    )
    
    return {
        "filepath": filepath,
        "format": "FBX",
        "objects": objects or "all",
        "success": True,
    }


@handler("export_gltf")
def export_gltf(
    filepath: str,
    objects: Optional[List[str]] = None,
    export_format: str = "GLB"
) -> dict:
    """
    Export objects to GLTF/GLB format.
    
    Args:
        filepath: Path to save the file
        objects: List of object names to export (all if None)
        export_format: GLB (binary) or GLTF_SEPARATE
        
    Returns:
        dict with export info
    """
    # Ensure directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Select objects to export
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for name in objects:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        use_selection = True
    else:
        use_selection = False
    
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=export_format,
        use_selection=use_selection
    )
    
    return {
        "filepath": filepath,
        "format": export_format,
        "objects": objects or "all",
        "success": True,
    }


@handler("export_stl")
def export_stl(filepath: str, objects: Optional[List[str]] = None) -> dict:
    """
    Export objects to STL format.
    
    Args:
        filepath: Path to save the STL file
        objects: List of object names to export (all if None)
        
    Returns:
        dict with export info
    """
    # Ensure directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Select objects to export
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for name in objects:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        export_selected = True
    else:
        export_selected = False
    
    bpy.ops.wm.stl_export(
        filepath=filepath,
        export_selected_objects=export_selected
    )
    
    return {
        "filepath": filepath,
        "format": "STL",
        "objects": objects or "all",
        "success": True,
    }


@handler("execute_python")
def execute_python(code: str) -> dict:
    """
    Execute arbitrary Python code in Blender.
    
    Args:
        code: Python code to execute
        
    Returns:
        dict with execution result
    """
    import io
    import sys
    
    # Capture stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    
    result = None
    error = None
    
    try:
        # Execute code
        exec_globals = {"bpy": bpy, "__builtins__": __builtins__}
        exec(code, exec_globals)
        result = "Code executed successfully"
    except Exception as e:
        error = str(e)
    finally:
        stdout_value = sys.stdout.getvalue()
        stderr_value = sys.stderr.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    return {
        "success": error is None,
        "result": result,
        "error": error,
        "stdout": stdout_value,
        "stderr": stderr_value,
    }
