"""
Schema Loader

Load and access AI function/tool schemas.
"""

import json
import os
from typing import Any, Dict, List, Optional

_SCHEMA_DIR = os.path.dirname(os.path.abspath(__file__))
_openai_cache: Optional[Dict] = None
_anthropic_cache: Optional[Dict] = None


def get_openai_functions() -> List[Dict[str, Any]]:
    """
    Get OpenAI function definitions.
    
    Returns:
        List of function definitions in OpenAI format
    """
    global _openai_cache
    if _openai_cache is None:
        path = os.path.join(_SCHEMA_DIR, 'openai_functions.json')
        with open(path, 'r') as f:
            _openai_cache = json.load(f)
    return _openai_cache.get('functions', [])


def get_anthropic_tools() -> List[Dict[str, Any]]:
    """
    Get Anthropic tool definitions.
    
    Returns:
        List of tool definitions in Anthropic format
    """
    global _anthropic_cache
    if _anthropic_cache is None:
        path = os.path.join(_SCHEMA_DIR, 'anthropic_tools.json')
        with open(path, 'r') as f:
            _anthropic_cache = json.load(f)
    return _anthropic_cache.get('tools', [])


def get_function_by_name(name: str, provider: str = 'openai') -> Optional[Dict[str, Any]]:
    """
    Get a specific function/tool definition by name.
    
    Args:
        name: Function/tool name
        provider: 'openai' or 'anthropic'
        
    Returns:
        Function/tool definition or None if not found
    """
    if provider == 'openai':
        functions = get_openai_functions()
    else:
        functions = get_anthropic_tools()
        
    for func in functions:
        if func.get('name') == name:
            return func
    return None


def get_all_function_names() -> List[str]:
    """Get list of all available function names."""
    return [f['name'] for f in get_openai_functions()]


def validate_schemas() -> Dict[str, bool]:
    """
    Validate that all schema files load correctly.
    
    Returns:
        Dict with validation results
    """
    results = {}
    
    try:
        funcs = get_openai_functions()
        results['openai'] = len(funcs) > 0
    except Exception as e:
        results['openai'] = False
        results['openai_error'] = str(e)
        
    try:
        tools = get_anthropic_tools()
        results['anthropic'] = len(tools) > 0
    except Exception as e:
        results['anthropic'] = False
        results['anthropic_error'] = str(e)
        
    return results
