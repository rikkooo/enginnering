#!/usr/bin/env python3
"""
Simple Scene Example

Creates a basic scene with cube and sphere, then renders it.
"""

import sys
sys.path.insert(0, '../..')

from ai import FunctionExecutor


def main():
    executor = FunctionExecutor()
    
    print("Creating simple Blender scene...")
    
    # Create a cube
    result = executor.execute("create_3d_primitive", {
        "application": "blender",
        "primitive_type": "cube",
        "name": "MyCube",
        "location": [0, 0, 0],
        "size": 2.0
    })
    print(f"Cube: {result}")
    
    # Create a sphere
    result = executor.execute("create_3d_primitive", {
        "application": "blender",
        "primitive_type": "sphere",
        "name": "MySphere",
        "location": [3, 0, 0],
        "radius": 1.0
    })
    print(f"Sphere: {result}")
    
    # Add a light
    result = executor.execute("add_light", {
        "name": "MainLight",
        "light_type": "SUN",
        "location": [5, 5, 10],
        "energy": 5.0
    })
    print(f"Light: {result}")
    
    # Add a camera
    result = executor.execute("add_camera", {
        "name": "MainCamera",
        "location": [7, -7, 5],
        "rotation": [1.1, 0, 0.8]
    })
    print(f"Camera: {result}")
    
    # Render the scene
    result = executor.execute("render_scene", {
        "output_path": "/tmp/simple_scene.png",
        "resolution_x": 800,
        "resolution_y": 600,
        "engine": "EEVEE",
        "samples": 64
    })
    print(f"Render: {result}")
    
    print("\nScene created and rendered to /tmp/simple_scene.png")
    executor.close()


if __name__ == "__main__":
    main()
