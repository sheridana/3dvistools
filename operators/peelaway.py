import bpy, blf
import os
import re
import math
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class peelAway(Operator):
    bl_idname = "peel.away"
    bl_label = "peel away operator"
    bl_options = {'UNDO'}
    
    offset_planes = BoolProperty(name = "Offset planes?", default = False, description = "Offset planes in some direction")
    
    offset_direction = EnumProperty(name = "Offset", items = [('X', 'X', 'X'), ('Y', 'Y', 'Y'), ('Z', 'Z', 'Z')], default = 'Z', description = "Direction to offset planes")
    
    start_x = FloatProperty(name = "Start X", default = 0, max = 100000, min = -100000, description = "Starting x value")
    
    start_y = FloatProperty(name = "Start Y", default = 0, max = 100000, min = -100000, description = "Starting y value")
    
    start_z = FloatProperty(name = "Start Z", default = 0, max = 100000, min = -100000, description = "Starting z value")
    
    x_offset = FloatProperty(name = "X offset", default = 0, max = 100000, min = -100000, description = "X offset value")
    
    y_offset = FloatProperty(name = "Y offset", default = 0, max = 100000, min = -100000, description = "y offset value")
    
    z_offset = FloatProperty(name = "Z offset", default = 0, max = 100000, min = -100000, description = "Z offset value")
    
    peel_away = BoolProperty(name = "Peel away?", default = False, description = "Peel away planes?")
    
    number_of_planes = FloatProperty(name = "Number of planes", default = 707, max = 100000, min = -100000, description = "Number of planes")
    
    frame_step = FloatProperty(name = "Frame step", default = 1, max = 100000, min = -100000, description = "Number of frames to peel by")
    
    calculate_frames = BoolProperty(name = "Calculate frames?", default = False, description = "Calculate number of frames to peel away based on number of planes selected")
    
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        selected_objects = bpy.context.selected_objects
        
        i = self.number_of_planes
        
        x = self.start_x
        y = self.start_y
        z = self.start_z
        
        for obj in selected_objects:
            if self.offset_planes:
                if self.offset_direction ==  'X':
                    obj.location.x = x
                    x += self.x_offset
                if self.offset_direction == 'Y':
                    obj.location.y = y
                    y += self.y_offset
                if self.offset_direction == 'Z':
                    obj.location.z = z
                    z += self.z_offset
            if self.peel_away:
                obj.hide = False
                obj.hide_render = False
                obj.keyframe_insert(data_path = 'hide', frame = i)
                obj.keyframe_insert(data_path = 'hide_render', frame = i)
                obj.hide = True
                obj.hide_render = True
                obj.keyframe_insert(data_path = 'hide', frame = i + self.frame_step)
                obj.keyframe_insert(data_path = 'hide_render', frame = i + self.frame_step)
                        
                i -= 1
            
        return {'FINISHED'}
                
                    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column(align = False)
        col.prop(self, "offset_planes")
        if self.offset_planes:
            col.prop(self, "offset_direction")
            if self.offset_direction == 'X':
                col.prop(self, "start_x")
                col.prop(self, "x_offset")
            if self.offset_direction == 'Y':
                col.prop(self, "start_y")
                col.prop(self, "y_offset")
            if self.offset_direction == 'Z':
                col.prop(self, "start_z")
                col.prop(self, "z_offset")
                
        box = layout.box()
        col = box.column(align = False)
        col.prop(self, "peel_away")
        if self.peel_away:
            col.prop(self, "number_of_planes")
            col.prop(self, "frame_step")
            col.prop(self,"calculate_frames")
        if self.calculate_frames:
            self.number_of_planes = len(bpy.context.selected_objects)
        
                
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 600)