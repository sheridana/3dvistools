import bpy
import os
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class newWindow(Operator):
    bl_idname = "new.window"
    bl_label = "new window"
    bl_options = {'UNDO'}

    duplicate_into_new_window = BoolProperty(
            name = "Duplicate active screen",
            default = False,
            description = "Duplicate active screen into new window?")

    new_window_type = EnumProperty(
            name = "Window type",
            items = [
                ('VIEW_3D', 'VIEW_3D', '', 'VIEW3D', 0),
                ('TEXT_EDITOR', 'TEXT_EDITOR', '', 'TEXT', 1),
                ('TIMELINE', 'TIMELINE', '', 'TIME', 2),
                ('GRAPH_EDITOR', 'GRAPH_EDITOR', '', 'IPO_BEZIER', 3),
                ('DOPESHEET_EDITOR', 'DOPESHEET_EDITOR', '', 'ACTION', 4),
                ('NLA_EDITOR', 'NLA_EDITOR', '', 'NLA', 5),
                ('IMAGE_EDITOR', 'IMAGE_EDITOR', '', 'IMAGE_COL', 6),
                ('SEQUENCE_EDITOR', 'SEQUENCE_EDITOR', '', 'SEQUENCE', 7),
                ('CLIP_EDITOR', 'CLIP_EDITOR', '', 'CLIP', 8),
                ('NODE_EDITOR', 'NODE_EDITOR', '', 'NODETREE', 9),
                ('LOGIC_EDITOR', 'LOGIC_EDITOR', '', 'LOGIC', 10),
                ('PROPERTIES', 'PROPERTIES', '', 'BUTS', 11),
                ('OUTLINER', 'OUTLINER', '', 'OOPS', 12),
                ('USER_PREFERENCES', 'USER_PREFERENCES', '', 'PREFERENCES', 13),
                ('INFO', 'INFO', '', 'INFO', 14),
                ('FILE_BROWSER', 'FILE_BROWSER', '', 'FILESEL', 15),
                ('CONSOLE', 'CONSOLE', '', 'CONSOLE', 16)
                ],
            default = 'VIEW_3D',
            description = "Change new window type")

    def execute(self, context):

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break

        space = area.spaces[0]

        context = bpy.context.copy()
        context['area'] = area
        context['region'] = region
        context['space_data'] = space

        if self.duplicate_into_new_window:
            bpy.ops.screen.area_dupli(context,'INVOKE_DEFAULT')

            for i in self.new_window_type:
                bpy.context.window_manager.windows[-1].screen.areas[0].type = self.new_window_type

        return {'FINISHED'}

    def draw(self, context):

        layout = self.layout
        box = layout.box()

        row = box.row(align = True)
        row.prop(self, "duplicate_into_new_window")
        row.prop(self, "new_window_type")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)
