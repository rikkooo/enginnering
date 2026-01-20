"""
WebSocket Handlers

WebSocket endpoints for real-time code execution and streaming.
"""

import asyncio
import json
from typing import Dict, Any, Set
from fastapi import WebSocket, WebSocketDisconnect

from ..config import settings
from ..clients import BlenderClient, FreeCADClient


class ConnectionManager:
    """Manages active WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        
    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        
    async def broadcast(self, message: Dict[str, Any]) -> None:
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


blender_manager = ConnectionManager()
freecad_manager = ConnectionManager()


async def websocket_blender(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for Blender.
    
    Supports:
    - execute: Run Python code in Blender
    - command: Send JSON-RPC command
    - ping: Keep-alive ping
    """
    await blender_manager.connect(websocket)
    
    client = BlenderClient(
        host=settings.blender_host,
        port=settings.blender_port,
        timeout=settings.blender_timeout
    )
    
    try:
        await client.connect()
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Blender WebSocket"
        })
        
        while True:
            try:
                data = await websocket.receive_json()
                message_type = data.get("type", "command")
                
                if message_type == "ping":
                    await websocket.send_json({"type": "pong"})
                    
                elif message_type == "execute":
                    code = data.get("code", "")
                    response = await client.execute_python(code)
                    await websocket.send_json({
                        "type": "execute_result",
                        "result": response.get("result", response)
                    })
                    
                elif message_type == "command":
                    method = data.get("method")
                    params = data.get("params", {})
                    response = await client.send_command(method, params)
                    await websocket.send_json({
                        "type": "command_result",
                        "method": method,
                        "result": response.get("result", response)
                    })
                    
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    })
                    
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                
    finally:
        blender_manager.disconnect(websocket)
        await client.disconnect()


async def websocket_freecad(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for FreeCAD.
    
    Supports:
    - execute: Run Python code in FreeCAD
    - command: Send JSON-RPC command
    - ping: Keep-alive ping
    """
    await freecad_manager.connect(websocket)
    
    client = FreeCADClient(
        host=settings.freecad_host,
        port=settings.freecad_port,
        timeout=settings.freecad_timeout
    )
    
    try:
        await client.connect()
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to FreeCAD WebSocket"
        })
        
        while True:
            try:
                data = await websocket.receive_json()
                message_type = data.get("type", "command")
                
                if message_type == "ping":
                    await websocket.send_json({"type": "pong"})
                    
                elif message_type == "execute":
                    code = data.get("code", "")
                    response = await client.execute_python(code)
                    await websocket.send_json({
                        "type": "execute_result",
                        "result": response.get("result", response)
                    })
                    
                elif message_type == "command":
                    method = data.get("method")
                    params = data.get("params", {})
                    response = await client.send_command(method, params)
                    await websocket.send_json({
                        "type": "command_result",
                        "method": method,
                        "result": response.get("result", response)
                    })
                    
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    })
                    
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                
    finally:
        freecad_manager.disconnect(websocket)
        await client.disconnect()
