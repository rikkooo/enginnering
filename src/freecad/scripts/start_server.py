#!/usr/bin/env python3
"""
FreeCAD Socket Server Startup Script

Run with: freecadcmd start_server.py -- --port 9877
Or: FreeCADCmd start_server.py -- --port 9877
"""

import sys
import os
import signal
import argparse

# Add paths for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, src_dir)
sys.path.insert(0, os.path.dirname(script_dir))

# Parse arguments (after --)
def parse_args():
    parser = argparse.ArgumentParser(description='FreeCAD Socket Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=9877, help='Port to listen on')
    
    # Find args after --
    try:
        idx = sys.argv.index('--')
        args = parser.parse_args(sys.argv[idx + 1:])
    except ValueError:
        args = parser.parse_args([])
        
    return args


def main():
    print("=" * 50)
    print("3DM-API FreeCAD Server - Headless Mode")
    print("=" * 50)
    
    args = parse_args()
    
    # Import FreeCAD
    try:
        import FreeCAD
        import Part
        print(f"FreeCAD Version: {'.'.join(str(x) for x in FreeCAD.Version()[:3])}")
    except ImportError as e:
        print(f"Error: Could not import FreeCAD: {e}")
        print("Make sure to run with freecadcmd or FreeCADCmd")
        sys.exit(1)
        
    # Import server components
    from server import FreeCADSocketServer
    from server.handlers import get_dispatcher
    
    # Create and configure server
    server = FreeCADSocketServer(host=args.host, port=args.port)
    server.set_dispatcher(get_dispatcher())
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print("\nShutdown signal received...")
        server.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start server (blocking)
    try:
        server.start()
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
