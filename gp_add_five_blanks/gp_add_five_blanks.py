bl_info = {
    "name": "GP +5 Blanks",
    "description": "A toolbar button to append 5 blank keyframes (on twos) to the active Grease Pencil layer",
    "author": "chluaid",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "Dope Sheet > Header Menu",
    "category": "Animation",
    "support": "COMMUNITY"
    "doc_url": "https://bitey.com"
    "tracker_url": "https://github.com/35743/GreasePencil/issues"
}

import bpy

class AddKeyframesOperator(bpy.types.Operator):
    bl_idname = "grease_pencil.add_custom_keyframes"
    bl_label = "Add 5 Blank Keyframes"
    bl_description = "Adds 5 new blank keyframes appended to the end of the current sequence."

    def execute(self, context):
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
                    last_frame = -1  # So that the first frame will be at -1 + 2 = 1

                # Frames where to insert blank keyframes
                frames = [last_frame + 2 + i * 2 for i in range(5)]
                for frame_num in frames:
                    # Set the current frame
                    context.scene.frame_current = frame_num
                    # Insert a blank frame
                    bpy.ops.grease_pencil.insert_blank_frame()
                self.report({'INFO'}, f"Blank keyframes added at frames: {frames}")
            else:
                self.report({'WARNING'}, "No active Grease Pencil layer selected.")
        else:
            self.report({'WARNING'}, "The active object is not a Grease Pencil object.")

        return {'FINISHED'}

def draw_menu(self, context):
    self.layout.operator("grease_pencil.add_custom_keyframes", text="Add 5 Blank Keyframes")

# Register and unregister functions
def register():
    bpy.utils.register_class(AddKeyframesOperator)
    bpy.types.DOPESHEET_MT_editor_menus.append(draw_menu)

def unregister():
    bpy.types.DOPESHEET_MT_editor_menus.remove(draw_menu)
    bpy.utils.unregister_class(AddKeyframesOperator)
