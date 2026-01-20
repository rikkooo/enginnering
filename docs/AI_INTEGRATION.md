# AI Integration Guide

Guide for integrating 3DM-API with AI assistants (OpenAI, Anthropic Claude).

## Overview

3DM-API provides function/tool schemas compatible with:
- **OpenAI** Function Calling
- **Anthropic** Claude Tool Use

## Available Functions

| Function | Description |
|----------|-------------|
| `create_3d_primitive` | Create basic shapes (cube, sphere, cylinder, etc.) |
| `modify_object` | Transform, rename, or delete objects |
| `apply_material` | Create and apply PBR materials |
| `boolean_operation` | CSG operations (union, subtract, intersect) |
| `render_scene` | Render to image file |
| `export_model` | Export to various formats |
| `get_scene_info` | Query scene state |
| `execute_code` | Run arbitrary Python code |
| `add_camera` | Add camera to scene |
| `add_light` | Add light source |

## OpenAI Integration

### Loading Functions

```python
from ai import get_openai_functions

functions = get_openai_functions()
```

### Using with Chat Completions

```python
from openai import OpenAI
from ai import get_openai_functions, FunctionExecutor
import json

client = OpenAI()
executor = FunctionExecutor()
functions = get_openai_functions()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Create a red cube"}
    ],
    functions=functions,
    function_call="auto"
)

# Handle function call
if response.choices[0].message.function_call:
    func = response.choices[0].message.function_call
    result = executor.execute(func.name, json.loads(func.arguments))
    print(result)
```

## Anthropic Integration

### Loading Tools

```python
from ai import get_anthropic_tools

tools = get_anthropic_tools()
```

### Using with Claude

```python
import anthropic
from ai import get_anthropic_tools, FunctionExecutor
import json

client = anthropic.Anthropic()
executor = FunctionExecutor()
tools = get_anthropic_tools()

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4096,
    tools=tools,
    messages=[
        {"role": "user", "content": "Create a box and sphere, then subtract the sphere from the box"}
    ]
)

# Handle tool use
for block in response.content:
    if block.type == "tool_use":
        result = executor.execute(block.name, block.input)
        print(result)
```

## Function Executor

The `FunctionExecutor` class routes AI function calls to the appropriate API endpoints.

```python
from ai import FunctionExecutor

executor = FunctionExecutor(base_url="http://localhost:8000")

# Synchronous execution
result = executor.execute("create_3d_primitive", {
    "application": "blender",
    "primitive_type": "cube",
    "name": "MyCube"
})

# Async execution
result = await executor.execute_async("render_scene", {
    "output_path": "/tmp/render.png"
})
```

## Example Workflows

### Simple Scene Creation

```python
from ai import FunctionExecutor

executor = FunctionExecutor()

# Create objects
executor.execute("create_3d_primitive", {
    "application": "blender",
    "primitive_type": "cube",
    "location": [0, 0, 0]
})

executor.execute("create_3d_primitive", {
    "application": "blender", 
    "primitive_type": "sphere",
    "location": [3, 0, 0]
})

# Add lighting
executor.execute("add_light", {
    "light_type": "SUN",
    "energy": 5.0
})

# Render
executor.execute("render_scene", {
    "output_path": "/tmp/scene.png"
})
```

### CAD Boolean Operations

```python
from ai import FunctionExecutor

executor = FunctionExecutor()

# Create parts
executor.execute("create_3d_primitive", {
    "application": "freecad",
    "primitive_type": "box",
    "length": 20, "width": 20, "height": 20
})

executor.execute("create_3d_primitive", {
    "application": "freecad",
    "primitive_type": "sphere",
    "radius": 12
})

# Boolean subtract
executor.execute("boolean_operation", {
    "operation": "subtract",
    "object1": "Box",
    "object2": "Sphere"
})

# Export
executor.execute("export_model", {
    "application": "freecad",
    "filepath": "/tmp/part.step",
    "format": "STEP"
})
```

## Schema Files

- `ai/schemas/openai_functions.json` - OpenAI function definitions
- `ai/schemas/anthropic_tools.json` - Anthropic tool definitions

## Best Practices

1. **Use appropriate application**: Use `blender` for visualization/rendering, `freecad` for CAD/engineering
2. **Name objects**: Always provide meaningful names for objects
3. **Check results**: Verify function execution results before proceeding
4. **Handle errors**: Implement error handling for failed operations
5. **Clean up**: Delete temporary objects when done
