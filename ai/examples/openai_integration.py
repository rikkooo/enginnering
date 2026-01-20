#!/usr/bin/env python3
"""
OpenAI Integration Example

Demonstrates using OpenAI function calling with 3DM-API.
Requires: pip install openai
"""

import json
import sys
sys.path.insert(0, '../..')

from ai import get_openai_functions, FunctionExecutor

# Check if openai is available
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Note: openai package not installed. Run: pip install openai")


def run_with_openai():
    """Run example with actual OpenAI API."""
    client = OpenAI()
    executor = FunctionExecutor()
    functions = get_openai_functions()
    
    messages = [
        {"role": "system", "content": "You are a 3D modeling assistant. Use the available functions to create 3D scenes."},
        {"role": "user", "content": "Create a red cube at the origin and a blue sphere next to it, then render the scene."}
    ]
    
    print("Sending request to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    
    # Process function calls
    while response.choices[0].message.function_call:
        func_call = response.choices[0].message.function_call
        func_name = func_call.name
        func_args = json.loads(func_call.arguments)
        
        print(f"\nExecuting: {func_name}")
        print(f"Arguments: {func_args}")
        
        # Execute the function
        result = executor.execute(func_name, func_args)
        print(f"Result: {result}")
        
        # Add function result to messages
        messages.append(response.choices[0].message)
        messages.append({
            "role": "function",
            "name": func_name,
            "content": json.dumps(result)
        })
        
        # Get next response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
    
    print("\nFinal response:", response.choices[0].message.content)
    executor.close()


def run_demo():
    """Run demo without OpenAI API (shows how it would work)."""
    executor = FunctionExecutor()
    functions = get_openai_functions()
    
    print("OpenAI Integration Demo")
    print("=" * 50)
    print(f"\nAvailable functions ({len(functions)}):")
    for f in functions:
        print(f"  - {f['name']}: {f['description'][:50]}...")
    
    # Simulate what OpenAI would call
    print("\n--- Simulating OpenAI function calls ---\n")
    
    # Step 1: Create cube
    print("1. OpenAI calls: create_3d_primitive")
    result = executor.execute("create_3d_primitive", {
        "application": "blender",
        "primitive_type": "cube",
        "name": "RedCube",
        "location": [0, 0, 0]
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 2: Apply red material
    print("\n2. OpenAI calls: apply_material")
    result = executor.execute("apply_material", {
        "object_name": "RedCube",
        "material_name": "RedMat",
        "color": [1, 0, 0, 1]
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 3: Create sphere
    print("\n3. OpenAI calls: create_3d_primitive")
    result = executor.execute("create_3d_primitive", {
        "application": "blender",
        "primitive_type": "sphere",
        "name": "BlueSphere",
        "location": [3, 0, 0]
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 4: Apply blue material
    print("\n4. OpenAI calls: apply_material")
    result = executor.execute("apply_material", {
        "object_name": "BlueSphere",
        "material_name": "BlueMat",
        "color": [0, 0, 1, 1]
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 5: Render
    print("\n5. OpenAI calls: render_scene")
    result = executor.execute("render_scene", {
        "output_path": "/tmp/openai_demo.png",
        "engine": "EEVEE",
        "samples": 32
    })
    print(f"   Result: {result}")
    
    print("\n" + "=" * 50)
    print("Demo complete! Image saved to /tmp/openai_demo.png")
    print("\nTo use with real OpenAI API:")
    print("  1. pip install openai")
    print("  2. export OPENAI_API_KEY=your-key")
    print("  3. Uncomment run_with_openai() in main()")
    
    executor.close()


def main():
    if HAS_OPENAI and False:  # Set to True to use real API
        run_with_openai()
    else:
        run_demo()


if __name__ == "__main__":
    main()
