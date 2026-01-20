"""
FreeCAD Command Handlers

Command dispatcher and handler registration for FreeCAD operations.
"""

from typing import Dict, Any, Callable, Optional, List
from functools import wraps

# Handler registry
_handlers: Dict[str, Callable] = {}


def handler(method_name: str):
    """
    Decorator to register a function as a command handler.
    
    Args:
        method_name: The JSON-RPC method name to handle
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _handlers[method_name] = wrapper
        return wrapper
    return decorator


class CommandDispatcher:
    """
    Dispatches JSON-RPC commands to registered handlers.
    """
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        
    def register(self, method: str, handler_func: Callable) -> None:
        """Register a handler for a method."""
        self.handlers[method] = handler_func
        
    def dispatch(self, method: str, params: Dict[str, Any]) -> Any:
        """
        Dispatch a command to its handler.
        
        Args:
            method: The method name to call
            params: Parameters to pass to the handler
            
        Returns:
            Handler result
            
        Raises:
            MethodNotFoundError: If no handler is registered for the method
        """
        from common.exceptions import MethodNotFoundError
        
        handler_func = self.handlers.get(method)
        if handler_func is None:
            raise MethodNotFoundError(method)
            
        return handler_func(**params)
        
    def list_methods(self) -> List[str]:
        """Return list of registered method names."""
        return sorted(self.handlers.keys())


# Global dispatcher instance
_dispatcher: Optional[CommandDispatcher] = None


def get_dispatcher() -> CommandDispatcher:
    """Get or create the global command dispatcher."""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = CommandDispatcher()
        _register_all_handlers(_dispatcher)
    return _dispatcher


def _register_all_handlers(dispatcher: CommandDispatcher) -> None:
    """Register all handlers with the dispatcher."""
    # Import handler modules to trigger @handler decorators
    from . import document
    from . import primitives
    from . import boolean
    from . import export
    
    # Register decorated handlers
    for method, handler_func in _handlers.items():
        dispatcher.register(method, handler_func)
        
    # Register built-in handlers
    dispatcher.register('ping', _ping)
    dispatcher.register('get_version', _get_version)
    dispatcher.register('list_methods', lambda: dispatcher.list_methods())
    
    print(f"Registered {len(dispatcher.handlers)} command handlers")


# Built-in handlers

def _ping() -> dict:
    """Health check handler."""
    return {
        "status": "pong",
        "message": "3DM-API FreeCAD Server is running"
    }


def _get_version() -> dict:
    """Get FreeCAD and API version information."""
    try:
        import FreeCAD
        fc_version = FreeCAD.Version()
        version_string = f"{fc_version[0]}.{fc_version[1]}.{fc_version[2]}"
    except:
        fc_version = ["0", "0", "0"]
        version_string = "unknown"
        
    return {
        "freecad_version": version_string,
        "freecad_version_tuple": fc_version[:3] if isinstance(fc_version, (list, tuple)) else [],
        "api_version": "1.0.0"
    }
