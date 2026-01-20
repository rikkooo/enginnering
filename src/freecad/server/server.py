"""
FreeCAD Socket Server

TCP socket server for receiving JSON-RPC commands and executing FreeCAD operations.
"""

import socket
import threading
import json
import signal
import sys
from typing import Optional, Callable

# Add parent paths for imports
sys.path.insert(0, str(__file__).rsplit('/src/', 1)[0] + '/src')

from common.protocol import Request, Response, ErrorResponse
from common.exceptions import TDMAPIError


class FreeCADSocketServer:
    """
    TCP socket server for FreeCAD remote control.
    
    Accepts JSON-RPC commands over TCP and dispatches them to registered handlers.
    """
    
    def __init__(self, host: str = '127.0.0.1', port: int = 9877):
        """
        Initialize the socket server.
        
        Args:
            host: Host address to bind to
            port: Port number to listen on
        """
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.clients = []
        self.dispatcher = None
        self._shutdown_event = threading.Event()
        
    def set_dispatcher(self, dispatcher) -> None:
        """Set the command dispatcher for handling requests."""
        self.dispatcher = dispatcher
        
    def start(self) -> None:
        """Start the socket server (blocking)."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1.0)  # Allow periodic shutdown checks
        
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            print(f"FreeCAD Socket Server listening on {self.host}:{self.port}")
            
            while self.running and not self._shutdown_event.is_set():
                try:
                    client_socket, address = self.socket.accept()
                    print(f"Client connected from {address}")
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    self.clients.append((client_socket, client_thread))
                except socket.timeout:
                    continue
                except OSError:
                    if self.running:
                        raise
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
            raise
        finally:
            self.stop()
            
    def stop(self) -> None:
        """Stop the socket server and close all connections."""
        self.running = False
        self._shutdown_event.set()
        
        # Close all client connections
        for client_socket, _ in self.clients:
            try:
                client_socket.close()
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
            
        print("FreeCAD Socket Server stopped")
        
    def _handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Handle a client connection.
        
        Args:
            client_socket: The client socket
            address: Client address tuple
        """
        buffer = ""
        client_socket.settimeout(30.0)
        
        try:
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                        
                    buffer += data.decode('utf-8')
                    
                    # Process complete messages (newline-delimited)
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        if message.strip():
                            response = self._process_message(message)
                            client_socket.sendall((response + '\n').encode('utf-8'))
                            
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    break
                    
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            print(f"Client disconnected: {address}")
            
    def _process_message(self, message: str) -> str:
        """
        Process a JSON-RPC message and return the response.
        
        Args:
            message: JSON-RPC request string
            
        Returns:
            JSON-RPC response string
        """
        try:
            request = Request.from_json(message)
        except Exception as e:
            error_response = ErrorResponse(
                id=None,
                code="PARSE_ERROR",
                message=f"Invalid JSON: {str(e)}"
            )
            return error_response.to_json()
            
        if self.dispatcher is None:
            error_response = ErrorResponse(
                id=request.id,
                code="SERVER_ERROR",
                message="No dispatcher configured"
            )
            return error_response.to_json()
            
        try:
            result = self.dispatcher.dispatch(request.method, request.params)
            response = Response(id=request.id, result=result)
            return response.to_json()
        except TDMAPIError as e:
            error_response = ErrorResponse(
                id=request.id,
                code=e.code,
                message=str(e),
                details=e.details
            )
            return error_response.to_json()
        except Exception as e:
            error_response = ErrorResponse(
                id=request.id,
                code="EXECUTION_ERROR",
                message=str(e)
            )
            return error_response.to_json()


def create_server(host: str = '127.0.0.1', port: int = 9877) -> FreeCADSocketServer:
    """
    Create and configure a FreeCAD socket server.
    
    Args:
        host: Host address to bind to
        port: Port number to listen on
        
    Returns:
        Configured FreeCADSocketServer instance
    """
    from .handlers import get_dispatcher
    
    server = FreeCADSocketServer(host=host, port=port)
    server.set_dispatcher(get_dispatcher())
    return server
