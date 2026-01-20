"""
Command Handlers and Dispatcher
================================
Routes incoming JSON-RPC commands to the appropriate handler functions.
Uses bpy.app.timers for thread-safe execution of Blender API calls.
"""

import bpy
import threading
import queue
from typing import Callable, Dict, Any, Optional
from functools import wraps

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.exceptions import MethodNotFoundError, CommandError


# Queue for thread-safe command execution
_command_queue = queue.Queue()
_result_queue = queue.Queue()
_timer_registered = False


class CommandDispatcher:
    """
    Dispatches JSON-RPC method calls to registered handler functions.
    Ensures thread-safe execution of Blender API calls.
    """
    
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._lock = threading.Lock()
    
    def register(self, method: str, handler: Callable):
        """Register a handler function for a method name."""
        with self._lock:
            self._handlers[method] = handler
    
    def unregister(self, method: str):
        """Unregister a handler for a method name."""
        with self._lock:
            if method in self._handlers:
                del self._handlers[method]
    
    def dispatch(self, method: str, params: Dict[str, Any]) -> Any:
        """
        Dispatch a method call to its handler.
        
        Args:
            method: The method name to call
            params: Parameters to pass to the handler
            
        Returns:
            The result from the handler
            
        Raises:
            MethodNotFoundError: If no handler is registered for the method
        """
        with self._lock:
            handler = self._handlers.get(method)
        
        if handler is None:
            raise MethodNotFoundError(method)
        
        # Execute handler with thread-safe wrapper if needed
        return self._execute_threadsafe(handler, params)
    
    def _execute_threadsafe(self, handler: Callable, params: Dict[str, Any]) -> Any:
        """
        Execute a handler in a thread-safe manner.
        
        In headless mode (-b), we execute directly since there's no UI thread.
        In GUI mode, we would queue for main thread execution.
        """
        # In headless mode, bpy.app.timers don't process, so execute directly.
        # This is safe because headless mode is single-threaded for bpy operations.
        # For GUI mode with proper threading, we'd use the timer queue.
        
        # Check if running in background/headless mode
        if bpy.app.background:
            # Execute directly in headless mode
            return handler(**params)
        
        # Check if we're on the main thread
        if threading.current_thread() is threading.main_thread():
            return handler(**params)
        
        # Queue command for main thread execution (GUI mode)
        result_event = threading.Event()
        result_container = {'result': None, 'error': None}
        
        _command_queue.put((handler, params, result_event, result_container))
        
        # Ensure timer is registered
        _ensure_timer_registered()
        
        # Wait for result
        result_event.wait(timeout=30.0)
        
        if result_container['error'] is not None:
            raise result_container['error']
        
        return result_container['result']
    
    def list_methods(self) -> list:
        """List all registered method names."""
        with self._lock:
            return list(self._handlers.keys())


def _process_command_queue():
    """Timer callback to process queued commands on the main thread."""
    try:
        while not _command_queue.empty():
            handler, params, result_event, result_container = _command_queue.get_nowait()
            
            try:
                result_container['result'] = handler(**params)
            except Exception as e:
                result_container['error'] = e
            finally:
                result_event.set()
    except:
        pass
    
    # Return interval to keep timer running (0.01 seconds)
    return 0.01


def _ensure_timer_registered():
    """Ensure the command processing timer is registered."""
    global _timer_registered
    if not _timer_registered:
        if bpy.app.timers.is_registered(_process_command_queue):
            bpy.app.timers.unregister(_process_command_queue)
        bpy.app.timers.register(_process_command_queue, first_interval=0.01)
        _timer_registered = True


# Global dispatcher instance
_dispatcher = None


def get_dispatcher() -> CommandDispatcher:
    """Get or create the global dispatcher instance."""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = CommandDispatcher()
    return _dispatcher


def handler(method: str):
    """
    Decorator to register a function as a command handler.
    
    Usage:
        @handler("create_cube")
        def create_cube(location=(0,0,0), size=2, name=None):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(**kwargs):
            return func(**kwargs)
        
        get_dispatcher().register(method, wrapper)
        return wrapper
    return decorator


# Built-in handlers

@handler("ping")
def ping() -> dict:
    """Health check handler."""
    return {"status": "pong", "message": "3DM-API Server is running"}


@handler("get_version")
def get_version() -> dict:
    """Get Blender version information."""
    return {
        "blender_version": ".".join(str(v) for v in bpy.app.version),
        "blender_version_string": bpy.app.version_string,
        "api_version": "1.0.0",
    }


@handler("list_methods")
def list_methods() -> dict:
    """List all available methods."""
    return {"methods": get_dispatcher().list_methods()}


def register_all_handlers():
    """
    Register all command handlers with the server.
    Called during addon initialization.
    """
    from . import server
    from . import primitives
    from . import materials
    from . import scene
    from . import rendering
    
    # Set dispatcher on server
    server.set_dispatcher(get_dispatcher())
    
    # Ensure timer is registered for thread-safe execution
    _ensure_timer_registered()
    
    print(f"Registered {len(get_dispatcher().list_methods())} command handlers")
