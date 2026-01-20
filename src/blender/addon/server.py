"""
Blender Socket Server
=====================
TCP socket server that runs inside Blender and accepts JSON-RPC commands.
Uses threading for non-blocking operation and bpy.app.timers for thread-safe
Blender API calls.
"""

import socket
import threading
import json
import sys
import os

# Add common module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.protocol import Request, Response, ErrorResponse
from common.exceptions import TDMAPIError, MethodNotFoundError

# Global server instance
_server_instance = None
_server_lock = threading.Lock()

# Default configuration
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9876
BUFFER_SIZE = 4096
CONNECTION_TIMEOUT = 60.0


class BlenderSocketServer:
    """
    TCP socket server for remote Blender control.
    
    Runs in a separate thread and uses bpy.app.timers to execute
    Blender API calls on the main thread.
    """
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.thread = None
        self.clients = []
        self.clients_lock = threading.Lock()
        
        # Command dispatcher (set by handlers module)
        self.dispatcher = None
    
    def start(self):
        """Start the socket server in a background thread."""
        if self.running:
            return
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1.0)  # Allow periodic checks for shutdown
        
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            self.thread = threading.Thread(target=self._accept_loop, daemon=True)
            self.thread.start()
            
            print(f"3DM-API Server started on {self.host}:{self.port}")
        except Exception as e:
            self.socket.close()
            raise e
    
    def stop(self):
        """Stop the socket server and close all connections."""
        self.running = False
        
        # Close all client connections
        with self.clients_lock:
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
        
        # Close server socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        # Wait for thread to finish
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        
        print("3DM-API Server stopped")
    
    def _accept_loop(self):
        """Main loop that accepts incoming connections."""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                client_socket.settimeout(CONNECTION_TIMEOUT)
                
                with self.clients_lock:
                    self.clients.append(client_socket)
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                # Normal timeout, check if still running
                continue
            except Exception as e:
                if self.running:
                    print(f"Accept error: {e}")
    
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle a single client connection."""
        buffer = ""
        
        try:
            while self.running:
                try:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    
                    buffer += data.decode('utf-8')
                    
                    # Process complete messages (newline-delimited)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            response = self._process_message(line)
                            client_socket.send(response.encode('utf-8'))
                            
                except socket.timeout:
                    # Send ping to check if client is still alive
                    continue
                except Exception as e:
                    error_response = ErrorResponse(
                        code="RECEIVE_ERROR",
                        message=str(e)
                    )
                    try:
                        client_socket.send(error_response.to_json().encode('utf-8'))
                    except:
                        pass
                    break
        finally:
            # Remove client from list and close
            with self.clients_lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            try:
                client_socket.close()
            except:
                pass
    
    def _process_message(self, message: str) -> str:
        """Process a JSON-RPC message and return the response."""
        try:
            request = Request.from_json(message)
            
            if self.dispatcher is None:
                error = ErrorResponse(
                    code="SERVER_NOT_READY",
                    message="Command dispatcher not initialized",
                    id=request.id
                )
                return error.to_json()
            
            # Execute command through dispatcher
            try:
                result = self.dispatcher.dispatch(request.method, request.params)
                response = Response(result=result, id=request.id)
                return response.to_json()
            except TDMAPIError as e:
                error = ErrorResponse(
                    code=e.code,
                    message=e.message,
                    details=e.details,
                    id=request.id
                )
                return error.to_json()
            except Exception as e:
                error = ErrorResponse(
                    code="EXECUTION_ERROR",
                    message=str(e),
                    id=request.id
                )
                return error.to_json()
                
        except json.JSONDecodeError as e:
            error = ErrorResponse(
                code="PARSE_ERROR",
                message=f"Invalid JSON: {e}"
            )
            return error.to_json()
        except Exception as e:
            error = ErrorResponse(
                code="INTERNAL_ERROR",
                message=str(e)
            )
            return error.to_json()
    
    def set_dispatcher(self, dispatcher):
        """Set the command dispatcher."""
        self.dispatcher = dispatcher


# Module-level functions for easy access

def get_server() -> BlenderSocketServer:
    """Get or create the global server instance."""
    global _server_instance
    with _server_lock:
        if _server_instance is None:
            _server_instance = BlenderSocketServer()
        return _server_instance


def start(host: str = None, port: int = None):
    """Start the global server instance."""
    server = get_server()
    if host:
        server.host = host
    if port:
        server.port = port
    server.start()


def stop():
    """Stop the global server instance."""
    global _server_instance
    with _server_lock:
        if _server_instance:
            _server_instance.stop()


def is_running() -> bool:
    """Check if the server is running."""
    global _server_instance
    with _server_lock:
        return _server_instance is not None and _server_instance.running


def get_port() -> int:
    """Get the server port."""
    global _server_instance
    with _server_lock:
        if _server_instance:
            return _server_instance.port
        return DEFAULT_PORT


def set_dispatcher(dispatcher):
    """Set the command dispatcher on the global server."""
    server = get_server()
    server.set_dispatcher(dispatcher)
