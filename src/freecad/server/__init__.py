"""
FreeCAD Socket Server Package

Provides a TCP socket server for remote control of FreeCAD via JSON-RPC commands.
"""

from .server import FreeCADSocketServer
from .handlers import CommandDispatcher, handler

__all__ = [
    'FreeCADSocketServer',
    'CommandDispatcher',
    'handler',
]

__version__ = '1.0.0'
