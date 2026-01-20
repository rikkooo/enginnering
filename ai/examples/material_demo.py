#!/usr/bin/env python3
"""
Material Demo

Demonstrates creating and applying materials in Blender.
"""

import sys
sys.path.insert(0, '../..')

from ai import FunctionExecutor


def main():
    executor = FunctionExecutor()
    
    print("Material Demo (Blender)")
    print("=" * 40)
    
    # Create objects with different materials
    objects = [
        {"name": "RedCube", "type": "cube", "location": [-3, 0, 0], "color": [1, 0, 0, 1]},
        {"name": "GreenSphere", "type": "sphere", "location": [0, 0, 0], "color": [0, 1, 0, 1]},
        {"name": "BlueCylinder", "type": "cylinder", "location": [3, 0, 0], "color": [0, 0, 1, 1]},
        {"name": "GoldTorus", "type": "torus", "location": [0, 3, 0], "color": [1, 0.8, 0, 1], "metallic": 1.0},
    ]
    
    for obj in objects:
        # Create primitive
        result = executor.execute("create_3d_primitive", {
            "application": "blender",
            "primitive_type": obj["type"],
            "name": obj["name"],
            "location": obj["location"]
        })
        print(f"Created {obj['name']}: {result.get('status')}")
        
        # Apply material
        result = executor.execute("apply_material", {
            "object_name": obj["name"],
            "material_name": f"{obj['name']}Mat",
            "color": obj["color"],
            "metallic": obj.get("metallic", 0.0),
            "roughness": obj.get("roughness", 0.5)
        })
        print(f"Material applied: {result.get('status')}")
    
    # Add lighting
    executor.execute("add_light", {
        "name": "KeyLight",
        "light_type": "AREA",
        "location": [5, -5, 8],
        "energy": 500
    })
    
    executor.execute("add_light", {
        "name": "FillLight",
        "light_type": "AREA",
        "location": [-5, -3, 5],
        "energy": 200
    })
    
    # Add camera
    executor.execute("add_camera", {
        "name": "RenderCam",
        "location": [8, -8, 6],
        "rotation": [1.1, 0, 0.8]
    })
    
    # Render
    result = executor.execute("render_scene", {
        "output_path": "/tmp/material_demo.png",
        "resolution_x": 1280,
        "resolution_y": 720,
        "engine": "CYCLES",
        "samples": 64
    })
    print(f"\nRender: {result}")
    
    print("\nMaterial demo complete! Rendered to /tmp/material_demo.png")
    executor.close()


if __name__ == "__main__":
    main()
