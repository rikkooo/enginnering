"""
Base Socket Client

Async socket client for communicating with Blender/FreeCAD servers.
"""

import asyncio
import json
import socket
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager


class BaseSocketClient:
    """
    Async socket client for JSON-RPC communication.
    
    Provides connection pooling, retry logic, and async send/receive.
    """
    
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9876,
        timeout: float = 30.0,
        retry_attempts: int = 3,
        retry_delay: float = 1.0
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._lock = asyncio.Lock()
        self._request_id = 0
        
    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._writer is not None and not self._writer.is_closing()
        
    async def connect(self) -> bool:
        """
        Establish connection to the server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout
            )
            return True
        except Exception as e:
            self._reader = None
            self._writer = None
            return False
            
    async def disconnect(self) -> None:
        """Close the connection."""
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except:
                pass
            finally:
                self._writer = None
                self._reader = None
                
    async def send_command(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a JSON-RPC command and return the response.
        
        Args:
            method: The method name to call
            params: Optional parameters for the method
            
        Returns:
            Response dictionary with status and result/error
        """
        async with self._lock:
            for attempt in range(self.retry_attempts):
                try:
                    # Ensure connected
                    if not self.is_connected:
                        if not await self.connect():
                            raise ConnectionError(f"Cannot connect to {self.host}:{self.port}")
                    
                    # Build request
                    self._request_id += 1
                    request = {
                        "jsonrpc": "2.0",
                        "id": self._request_id,
                        "method": method,
                        "params": params or {}
                    }
                    
                    # Send
                    message = json.dumps(request) + "\n"
                    self._writer.write(message.encode('utf-8'))
                    await self._writer.drain()
                    
                    # Receive
                    response_data = await asyncio.wait_for(
                        self._reader.readline(),
                        timeout=self.timeout
                    )
                    
                    if not response_data:
                        raise ConnectionError("Connection closed by server")
                        
                    response = json.loads(response_data.decode('utf-8'))
                    return response
                    
                except (ConnectionError, asyncio.TimeoutError, OSError) as e:
                    await self.disconnect()
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(self.retry_delay)
                    else:
                        return {
                            "status": "error",
                            "error": {
                                "code": "CONNECTION_ERROR",
                                "message": str(e)
                            }
                        }
                except json.JSONDecodeError as e:
                    return {
                        "status": "error",
                        "error": {
                            "code": "PARSE_ERROR",
                            "message": f"Invalid JSON response: {e}"
                        }
                    }
                    
    async def ping(self) -> bool:
        """
        Check if server is responding.
        
        Returns:
            True if server responds to ping, False otherwise
        """
        try:
            response = await self.send_command("ping")
            return response.get("status") == "success" or "result" in response
        except:
            return False
            
    async def get_version(self) -> Dict[str, Any]:
        """Get server version information."""
        return await self.send_command("get_version")
        
    @asynccontextmanager
    async def connection(self):
        """Context manager for connection lifecycle."""
        try:
            await self.connect()
            yield self
        finally:
            await self.disconnect()


class ConnectionPool:
    """
    Pool of socket connections for concurrent requests.
    """
    
    def __init__(
        self,
        client_class: type,
        host: str,
        port: int,
        size: int = 5,
        **kwargs
    ):
        self.client_class = client_class
        self.host = host
        self.port = port
        self.size = size
        self.kwargs = kwargs
        self._pool: asyncio.Queue = None
        self._created = 0
        
    async def initialize(self) -> None:
        """Initialize the connection pool."""
        self._pool = asyncio.Queue(maxsize=self.size)
        
    async def acquire(self) -> BaseSocketClient:
        """Acquire a client from the pool."""
        if self._pool is None:
            await self.initialize()
            
        # Try to get from pool
        try:
            client = self._pool.get_nowait()
            if client.is_connected:
                return client
        except asyncio.QueueEmpty:
            pass
            
        # Create new client
        client = self.client_class(
            host=self.host,
            port=self.port,
            **self.kwargs
        )
        await client.connect()
        return client
        
    async def release(self, client: BaseSocketClient) -> None:
        """Release a client back to the pool."""
        if self._pool is None:
            await self.initialize()
            
        try:
            self._pool.put_nowait(client)
        except asyncio.QueueFull:
            await client.disconnect()
            
    async def close(self) -> None:
        """Close all connections in the pool."""
        if self._pool is None:
            return
            
        while not self._pool.empty():
            try:
                client = self._pool.get_nowait()
                await client.disconnect()
            except asyncio.QueueEmpty:
                break
