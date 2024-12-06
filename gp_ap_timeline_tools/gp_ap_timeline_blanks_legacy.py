bl_info = {
    "name": "AP Keyframe Tools",
    "description": "Adds tools to append blank keyframes and displays playhead position in seconds and frames.",
    "author": "Phillips aka chluaid",
    "version": (0, 1, 0),
    "blender": (3, 6, 16),
    "location": "Dope Sheet > Header Menu, 3D View > N-panel",
    "category": "Animation",
    "support": "COMMUNITY",
    "doc_url": "https://bitey.com",
    "tracker_url": "https://github.com/35743/GreasePencil/issues",
    "warning": "",
    "license": "GPL-3.0"
}
import bpy

# Core Function to Add Keyframes
def add_keyframes(context, frame_count, spacing, start_from_playhead=False):
    """Core function to add blank keyframes with specified spacing."""
    gp_obj = context.active_object

    # Ensure the active object is a Grease Pencil object
    if gp_obj and gp_obj.type == 'GPENCIL':  # Adjusted type for legacy GPencil
        gp_layer = gp_obj.data.layers.active
        if gp_layer:
            # Determine the starting frame
            if start_from_playhead:
                start_frame = max(1, context.scene.frame_current)  # Ensure no keyframe at 0
            else:
                existing_frames = [frame.frame_number for frame in gp_layer.frames]
                start_frame = max(existing_frames) + spacing if existing_frames else 1

            # Frames where to insert blank keyframes
            frames = [start_frame + i * spacing for i in range(frame_count)]
            for frame_num in frames:
                # Check if a frame already exists by searching the collection
                if not any(frame.frame_number == frame_num for frame in gp_layer.frames):
                    gp_layer.frames.new(frame_num)  # Directly add a new blank frame
            return f"Blank keyframes added at frames: {frames}"
        else:
            return "No active Grease Pencil layer selected."
    else:
        return "The active object is not a Grease Pencil object."



# Operator for +5 Frames
class GP_OT_AddKeyframes5(bpy.types.Operator):
    bl_idname = "gpencil.add_5_keyframes"
    bl_label = "Add +5 Frames"
    bl_description = "Adds 5 blank keyframes spaced by 2 frames."

    def execute(self, context):
        spacing = 2
        frame_count = 5
        message = add_keyframes(context, frame_count=frame_count, spacing=spacing, start_from_playhead=True)
        # Move playhead to the end of the sequence plus spacing
        final_frame = context.scene.frame_current + (frame_count - 1) * spacing + spacing
        context.scene.frame_current = final_frame
        self.report({'INFO'}, message)
        return {'FINISHED'}


# Operator for +10 Frames
class GP_OT_AddKeyframes10(bpy.types.Operator):
    bl_idname = "gpencil.add_10_keyframes"
    bl_label = "Add +10 Frames"
    bl_description = "Adds 10 blank keyframes spaced by 1 frame."

    def execute(self, context):
        spacing = 1
        frame_count = 10
        message = add_keyframes(context, frame_count=frame_count, spacing=spacing, start_from_playhead=True)
        # Move playhead to the end of the sequence plus spacing
        final_frame = context.scene.frame_current + (frame_count - 1) * spacing + spacing
        context.scene.frame_current = final_frame
        self.report({'INFO'}, message)
        return {'FINISHED'}



# Operator for N-panel with Custom Input
class GP_OT_AddKeyframesCustom(bpy.types.Operator):
    bl_idname = "gpencil.add_keyframes_custom"
    bl_label = "Add Keyframes"
    bl_description = "Adds blank keyframes based on the number and spacing defined."

    def execute(self, context):
        frame_count = context.scene.gp_frame_count
        spacing = context.scene.gp_spacing
        start_from_playhead = context.scene.gp_start_from_playhead

        gp_obj = context.active_object
        if not gp_obj or gp_obj.type != 'GPENCIL':
            self.report({'WARNING'}, "No active Grease Pencil object selected.")
            return {'CANCELLED'}

        # Determine the starting frame
        gp_layer = gp_obj.data.layers.active
        if not gp_layer:
            self.report({'WARNING'}, "No active Grease Pencil layer selected.")
            return {'CANCELLED'}

        if start_from_playhead:
            start_frame = max(1, context.scene.frame_current)  # Ensure no keyframe at 0
        else:
            existing_frames = [frame.frame_number for frame in gp_layer.frames]
            start_frame = max(existing_frames) + spacing if existing_frames else 1

        # Calculate the last frame in the sequence
        end_frame = start_frame + (frame_count - 1) * spacing

        # Add keyframes
        message = add_keyframes(context, frame_count, spacing, start_from_playhead)

        # Move playhead to the end of the sequence plus one spacing
        context.scene.frame_current = end_frame + spacing

        self.report({'INFO'}, message)
        return {'FINISHED'}



# Timeline Toolbar with Buttons and Readout
def draw_menu(self, context):
    layout = self.layout
    scene = context.scene

    # Add the +5 and +10 buttons
    layout.operator("gpencil.add_5_keyframes", text="+5")
    layout.operator("gpencil.add_10_keyframes", text="+10")

    # Display the playhead position as seconds and frames
    frame_rate = scene.render.fps
    frame_current = scene.frame_current
    seconds = frame_current // frame_rate
    remaining_frames = frame_current % frame_rate

    layout.label(text=f"Time: {seconds:02}:{remaining_frames:02}")


# N-panel for 3D View
class GP_PT_KeyframePanel(bpy.types.Panel):
    bl_label = "Grease Pencil Keyframes"
    bl_idname = "VIEW3D_PT_gp_keyframe_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Grease Pencil"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Input fields
        layout.prop(scene, "gp_frame_count", text="Keyframe Count")
        layout.prop(scene, "gp_spacing", text="Spacing")
        layout.prop(scene, "gp_start_from_playhead", text="Start from Playhead")

        # Add keyframes button
        layout.operator("gpencil.add_keyframes_custom", text="Add Keyframes")


# Registration
def register():
    bpy.types.Scene.gp_frame_count = bpy.props.IntProperty(
        name="Keyframe Count",
        default=5,
        min=1,
        description="Number of blank keyframes to add"
    )
    bpy.types.Scene.gp_spacing = bpy.props.IntProperty(
        name="Spacing",
        default=2,
        min=1,
        description="Spacing between keyframes"
    )
    bpy.types.Scene.gp_start_from_playhead = bpy.props.BoolProperty(
        name="Start from Playhead",
        default=False,
        description="If checked, keyframes start from the current playhead position"
    )

    bpy.utils.register_class(GP_OT_AddKeyframes5)
    bpy.utils.register_class(GP_OT_AddKeyframes10)
    bpy.utils.register_class(GP_OT_AddKeyframesCustom)
    bpy.utils.register_class(GP_PT_KeyframePanel)
    bpy.types.DOPESHEET_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.types.DOPESHEET_MT_editor_menus.remove(draw_menu)
    bpy.utils.unregister_class(GP_PT_KeyframePanel)
    bpy.utils.unregister_class(GP_OT_AddKeyframesCustom)
    bpy.utils.unregister_class(GP_OT_AddKeyframes10)
    bpy.utils.unregister_class(GP_OT_AddKeyframes5)
    del bpy.types.Scene.gp_frame_count
    del bpy.types.Scene.gp_spacing
    del bpy.types.Scene.gp_start_from_playhead


if __name__ == "__main__":
    register()
