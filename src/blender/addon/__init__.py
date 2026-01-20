"""
3DM-API Blender Addon
=====================
A Blender addon that provides a TCP socket server for remote control
of Blender via JSON-RPC commands.

This addon enables AI agents and external applications to:
- Create and manipulate 3D objects
- Apply materials and textures
- Control rendering
- Export scenes to various formats
"""

bl_info = {
    "name": "3DM-API Server",
    "author": "rikkooo",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > 3DM-API",
    "description": "TCP socket server for remote Blender control via JSON-RPC",
    "category": "Development",
}

import bpy

from . import server
from . import handlers
from . import primitives
from . import materials
from . import scene
from . import rendering


class TDMAPI_PT_main_panel(bpy.types.Panel):
    """Main panel for 3DM-API addon"""
    bl_label = "3DM-API Server"
    bl_idname = "TDMAPI_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "3DM-API"

    def draw(self, context):
        layout = self.layout
        
        # Server status
        if server.is_running():
            layout.label(text="Status: Running", icon='CHECKMARK')
            layout.label(text=f"Port: {server.get_port()}")
            layout.operator("tdmapi.stop_server", text="Stop Server", icon='PAUSE')
        else:
            layout.label(text="Status: Stopped", icon='X')
            layout.operator("tdmapi.start_server", text="Start Server", icon='PLAY')


class TDMAPI_OT_start_server(bpy.types.Operator):
    """Start the 3DM-API socket server"""
    bl_idname = "tdmapi.start_server"
    bl_label = "Start 3DM-API Server"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            server.start()
            self.report({'INFO'}, f"3DM-API Server started on port {server.get_port()}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to start server: {e}")
        return {'FINISHED'}


class TDMAPI_OT_stop_server(bpy.types.Operator):
    """Stop the 3DM-API socket server"""
    bl_idname = "tdmapi.stop_server"
    bl_label = "Stop 3DM-API Server"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            server.stop()
            self.report({'INFO'}, "3DM-API Server stopped")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to stop server: {e}")
        return {'FINISHED'}


classes = [
    TDMAPI_PT_main_panel,
    TDMAPI_OT_start_server,
    TDMAPI_OT_stop_server,
]


def register():
    """Register addon classes and initialize handlers"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register all command handlers
    handlers.register_all_handlers()
    
    print("3DM-API Addon registered")


def unregister():
    """Unregister addon classes and stop server"""
    # Stop server if running
    if server.is_running():
        server.stop()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("3DM-API Addon unregistered")


if __name__ == "__main__":
    register()
