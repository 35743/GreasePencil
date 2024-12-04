bl_info = {
    "name": "AP Keyframe Tools",
    "description": "Toolbar buttons to add blank keyframes on the active Grease Pencil layer",
    "author": "A Phillips aka chluaid",
    "version": (1, 1, 0),
    "blender": (4, 3, 0),
    "location": "Dope Sheet > Header Menu",
    "category": "Animation",
    "support": "COMMUNITY",
    "doc_url": "https://bitey.com",
    "tracker_url": "https://github.com/35743/GreasePencil/issues",
    "warning": "",
    "license": "GPL-3.0"
}

import bpy


class AddKeyframesOperator5(bpy.types.Operator):
    """Add 5 Blank Keyframes"""
    bl_idname = "grease_pencil.add_5_keyframes"
    bl_label = "Add +5 Frames"
    bl_description = "Adds 5 blank keyframes on twos."

    def execute(self, context):
        message = add_keyframes(context, frame_count=5, spacing=2)
        self.report({'INFO'}, message)
        return {'FINISHED'}


class AddKeyframesOperator10(bpy.types.Operator):
    """Add 10 Blank Keyframes"""
    bl_idname = "grease_pencil.add_10_keyframes"
    bl_label = "Add +10 Frames"
    bl_description = "Adds 10 blank keyframes on ones."

    def execute(self, context):
        message = add_keyframes(context, frame_count=10, spacing=1)
        self.report({'INFO'}, message)
        return {'FINISHED'}


def add_keyframes(context, frame_count, spacing):
    """Core function to add blank keyframes with specified spacing."""
    # Get the active object
    gp_obj = context.active_object

    # Ensure the active object is a Grease Pencil object
    if gp_obj and gp_obj.type == 'GREASEPENCIL':
        # Access the active layer
        gp_layer = gp_obj.data.layers.active
        if gp_layer:
            # Get all existing frame numbers in the layer
            existing_frames = [frame.frame_number for frame in gp_layer.frames]
            if existing_frames:
                last_frame = max(existing_frames)
            else:
                last_frame = -1  # So that the first frame will be at -1 + spacing = 1

            # Frames where to insert blank keyframes
            frames = [last_frame + spacing + i * spacing for i in range(frame_count)]
            for frame_num in frames:
                # Set the current frame
                context.scene.frame_current = frame_num
                # Insert a blank frame
                bpy.ops.grease_pencil.insert_blank_frame()
            return f"Blank keyframes added at frames: {frames}"
        else:
            return "No active Grease Pencil layer selected."
    else:
        return "The active object is not a Grease Pencil object."


def draw_menu(self, context):
    """Draw the buttons in the Dope Sheet header menu."""
    self.layout.operator("grease_pencil.add_5_keyframes", text="+5")
    self.layout.operator("grease_pencil.add_10_keyframes", text="+10")


# Register and unregister functions
def register():
    bpy.utils.register_class(AddKeyframesOperator5)
    bpy.utils.register_class(AddKeyframesOperator10)
    bpy.types.DOPESHEET_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.types.DOPESHEET_MT_editor_menus.remove(draw_menu)
    bpy.utils.unregister_class(AddKeyframesOperator10)
    bpy.utils.unregister_class(AddKeyframesOperator5)


if __name__ == "__main__":
    register()
