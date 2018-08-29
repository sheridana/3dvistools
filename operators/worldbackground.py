import bpy
import random
import colorsys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class worldBackground(Operator):
    bl_idname = "world.background"
    bl_label = "world background"
    bl_options = {'UNDO'}

    current_world_name = StringProperty(name = "World to edit", default = 'World', description = "Choose which world to edit")

    horizon_color = FloatVectorProperty( name = "Horizon color", default = (0.0, 0.0, 0.0), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set horizon color")

    zenith_color = FloatVectorProperty( name = "Zenith color", default = (1.0, 1.0, 1.0), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set zenith color")

    ambient_color = FloatVectorProperty( name = "Ambient color", default = (0.0, 0.0, 0.0), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set ambient color")

    paper_sky = BoolProperty(name = "Paper sky", default = False, description = "Set paper sky")

    blend_sky = BoolProperty(name = "Blend sky", default = False, description = "Set blend sky")

    real_sky = BoolProperty(name = "Real sky", default = False, description = "Set real sky")

    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        world = bpy.data.worlds[self.current_world_name]

        if self.paper_sky:
            world.use_sky_paper = True
        if not self.paper_sky:
            world.use_sky_paper = False
        if self.blend_sky:
            world.use_sky_blend = True
            if self.zenith_color:
                world.zenith_color = self.zenith_color
        if not self.blend_sky:
            world.use_sky_blend = False
        if self.real_sky:
            world.use_sky_real = True
        if not self.real_sky:
            world.use_sky_real = False
        if self.horizon_color:
            world.horizon_color = self.horizon_color
        if self.ambient_color:
            world.ambient_color = self.ambient_color

        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "current_world_name")
        row = box.row(align = False)
        row.prop(self, "paper_sky")
        row.prop(self, "blend_sky")
        row.prop(self, "real_sky")
        row = box.row(align = False)
        row.prop(self, "horizon_color")
        if self.blend_sky:
            row.prop(self, "zenith_color")
        row.prop(self, "ambient_color")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1200)







