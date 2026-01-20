#!/usr/bin/env python3
"""
Headless Server Startup Script
==============================
Starts the 3DM-API Blender socket server in headless mode.

Usage:
    blender -b -P start_server.py
    blender -b -P start_server.py -- --port 9876 --host localhost
"""

import sys
import os
import signal
import argparse

# Add the src directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
blender_dir = os.path.dirname(script_dir)  # src/blender
src_dir = os.path.dirname(blender_dir)      # src
project_dir = os.path.dirname(src_dir)      # project root

# Add paths for imports
sys.path.insert(0, src_dir)
sys.path.insert(0, blender_dir)

import bpy

# Import addon modules directly
from addon import server, handlers


def parse_args():
    """Parse command line arguments after the -- separator."""
    # Find the -- separator in sys.argv
    try:
        separator_index = sys.argv.index('--')
        script_args = sys.argv[separator_index + 1:]
    except ValueError:
        script_args = []
    
    parser = argparse.ArgumentParser(description='3DM-API Blender Server')
    parser.add_argument('--port', type=int, default=9876, help='Server port (default: 9876)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host (default: localhost)')
    
    return parser.parse_args(script_args)


_running = True


def keep_alive():
    """Timer callback to keep Blender running."""
    global _running
    if not _running:
        return None  # Stop timer
    return 0.1  # Check every 100ms


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    global _running
    print(f"\nReceived signal {signum}, shutting down...")
    _running = False
    server.stop()


def main():
    """Main entry point for headless server."""
    global _running
    args = parse_args()
    
    print("=" * 50)
    print("3DM-API Blender Server - Headless Mode")
    print("=" * 50)
    
    # Register signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register all command handlers
    handlers.register_all_handlers()
    
    # Start the server
    try:
        server.start(host=args.host, port=args.port)
        print(f"Server running on {args.host}:{args.port}")
        print("Press Ctrl+C to stop")
        print("=" * 50)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)
    
    # Register keep-alive timer
    bpy.app.timers.register(keep_alive, first_interval=0.1, persistent=True)
    
    # In headless mode with -b, Blender exits after script.
    # We need to block here to keep the process alive.
    import time
    try:
        while _running and server.is_running():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        print("Server shutdown complete")


if __name__ == "__main__":
    main()
