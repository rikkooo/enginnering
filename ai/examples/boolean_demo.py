#!/usr/bin/env python3
"""
Boolean Operations Demo

Demonstrates CSG boolean operations in FreeCAD.
"""

import sys
sys.path.insert(0, '../..')

from ai import FunctionExecutor


def main():
    executor = FunctionExecutor()
    
    print("Boolean Operations Demo (FreeCAD)")
    print("=" * 40)
    
    # Create a box
    result = executor.execute("create_3d_primitive", {
        "application": "freecad",
        "primitive_type": "box",
        "name": "BaseBox",
        "length": 20,
        "width": 20,
        "height": 20
    })
    print(f"Box: {result.get('status')}")
    
    # Create a sphere
    result = executor.execute("create_3d_primitive", {
        "application": "freecad",
        "primitive_type": "sphere",
        "name": "CutSphere",
        "radius": 12,
        "location": [10, 10, 10]
    })
    print(f"Sphere: {result.get('status')}")
    
    # Boolean subtract (box - sphere)
    result = executor.execute("boolean_operation", {
        "operation": "subtract",
        "object1": "BaseBox",
        "object2": "CutSphere",
        "result_name": "CutBox"
    })
    print(f"Subtract: {result}")
    
    # Create another cylinder for union demo
    result = executor.execute("create_3d_primitive", {
        "application": "freecad",
        "primitive_type": "cylinder",
        "name": "Cylinder1",
        "radius": 5,
        "height": 30
    })
    print(f"Cylinder: {result.get('status')}")
    
    # Boolean union
    result = executor.execute("boolean_operation", {
        "operation": "union",
        "object1": "CutBox",
        "object2": "Cylinder1",
        "result_name": "FinalPart"
    })
    print(f"Union: {result}")
    
    # Export to STEP
    result = executor.execute("export_model", {
        "application": "freecad",
        "filepath": "/tmp/boolean_demo.step",
        "format": "STEP"
    })
    print(f"Export: {result}")
    
    print("\nBoolean demo complete! Exported to /tmp/boolean_demo.step")
    executor.close()


if __name__ == "__main__":
    main()
