#!/usr/bin/env python3
"""
Anthropic Integration Example

Demonstrates using Anthropic Claude tool use with 3DM-API.
Requires: pip install anthropic
"""

import json
import sys
sys.path.insert(0, '../..')

from ai import get_anthropic_tools, FunctionExecutor

# Check if anthropic is available
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("Note: anthropic package not installed. Run: pip install anthropic")


def run_with_anthropic():
    """Run example with actual Anthropic API."""
    client = anthropic.Anthropic()
    executor = FunctionExecutor()
    tools = get_anthropic_tools()
    
    messages = [
        {"role": "user", "content": "Create a FreeCAD box and sphere, then perform a boolean subtract to cut the sphere from the box. Export the result to STEP format."}
    ]
    
    print("Sending request to Claude...")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    
    # Process tool calls
    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input
        
        print(f"\nExecuting: {tool_name}")
        print(f"Input: {tool_input}")
        
        # Execute the tool
        result = executor.execute(tool_name, tool_input)
        print(f"Result: {result}")
        
        # Add tool result to messages
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(result)
            }]
        })
        
        # Get next response
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
    
    # Print final text response
    for block in response.content:
        if hasattr(block, 'text'):
            print("\nFinal response:", block.text)
    
    executor.close()


def run_demo():
    """Run demo without Anthropic API (shows how it would work)."""
    executor = FunctionExecutor()
    tools = get_anthropic_tools()
    
    print("Anthropic Claude Integration Demo")
    print("=" * 50)
    print(f"\nAvailable tools ({len(tools)}):")
    for t in tools:
        print(f"  - {t['name']}: {t['description'][:50]}...")
    
    # Simulate what Claude would call
    print("\n--- Simulating Claude tool calls ---\n")
    
    # Step 1: Create box
    print("1. Claude calls: create_3d_primitive (box)")
    result = executor.execute("create_3d_primitive", {
        "application": "freecad",
        "primitive_type": "box",
        "name": "MainBox",
        "length": 20,
        "width": 20,
        "height": 20
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 2: Create sphere
    print("\n2. Claude calls: create_3d_primitive (sphere)")
    result = executor.execute("create_3d_primitive", {
        "application": "freecad",
        "primitive_type": "sphere",
        "name": "CutterSphere",
        "radius": 15,
        "location": [10, 10, 10]
    })
    print(f"   Result: {result.get('status')}")
    
    # Step 3: Boolean subtract
    print("\n3. Claude calls: boolean_operation (subtract)")
    result = executor.execute("boolean_operation", {
        "operation": "subtract",
        "object1": "MainBox",
        "object2": "CutterSphere",
        "result_name": "CutResult"
    })
    print(f"   Result: {result}")
    
    # Step 4: Export
    print("\n4. Claude calls: export_model")
    result = executor.execute("export_model", {
        "application": "freecad",
        "filepath": "/tmp/anthropic_demo.step",
        "format": "STEP"
    })
    print(f"   Result: {result}")
    
    print("\n" + "=" * 50)
    print("Demo complete! STEP file saved to /tmp/anthropic_demo.step")
    print("\nTo use with real Anthropic API:")
    print("  1. pip install anthropic")
    print("  2. export ANTHROPIC_API_KEY=your-key")
    print("  3. Uncomment run_with_anthropic() in main()")
    
    executor.close()


def main():
    if HAS_ANTHROPIC and False:  # Set to True to use real API
        run_with_anthropic()
    else:
        run_demo()


if __name__ == "__main__":
    main()
