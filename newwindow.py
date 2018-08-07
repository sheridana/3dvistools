import bpy, blf
import os
import re
import random
import time
import datetime
import json
import math
from math import pi, radians, degrees
import colorsys
import mathutils
import sys
import numpy as np
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class newWindow(Operator):
    bl_idname = "new.window"
    bl_label = "new window"
    bl_options = {'UNDO'}
    
    duplicate_into_new_window = BoolProperty( name = "Duplicate active screen", default = False, description = "Duplicate active screen into new window?")
    
    new_window_type = EnumProperty( name = "Window type", items = [('3D view', '3D view', '', 'VIEW3D', 0), ('Text Editor', 'Text Editor', '', 'TEXT', 1), ('Timeline', 'Timeline', '', 'TIME', 2), ('Graph editor', 'Graph editor', '', 'IPO_BEZIER', 3), ('Dopesheet editor', 'Dopesheet editor', '', 'ACTION', 4), ('NLA editor', 'NLA editor', '', 'NLA', 5), ('Image editor', 'Image editor', '', 'IMAGE_COL', 6), ('Video sequence editor', 'Video sequence editor', '', 'SEQUENCE', 7), ('Movie clip editor', 'Movie clip editor', '', 'CLIP', 8), ('Node editor', 'Node editor', '', 'NODETREE', 9), ('Logic editor', 'Logic editor', '', 'LOGIC', 10), ('Properties', 'Properties', '', 'BUTS', 11), ('Outliner', 'Outliner', '', 'OOPS', 12), ('User preferences', 'User preferences', '', 'PREFERENCES', 13), ('Info', 'Info', '', 'INFO', 14), ('File browser', 'File browser', '', 'FILESEL', 15), ('Python console', 'Python console', '', 'CONSOLE', 16)], default = '3D view', description = "Change new window type")
    
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
            bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
            if self.new_window_type == 'Text Editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'TEXT_EDITOR'
            if self.new_window_type == '3D view':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'VIEW_3D'
            if self.new_window_type == 'Timeline':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'TIMELINE'
            if self.new_window_type == 'Graph editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'GRAPH_EDITOR'
            if self.new_window_type == 'Dopesheet editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'DOPESHEET_EDITOR'
            if self.new_window_type == 'NLA editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'NLA_EDITOR'
            if self.new_window_type == 'Image editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'IMAGE_EDITOR'
            if self.new_window_type == 'Video sequence editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'SEQUENCE_EDITOR'
            if self.new_window_type == 'Movie clip editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'CLIP_EDITOR'
            if self.new_window_type == 'Node editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'NODE_EDITOR'
            if self.new_window_type == 'Logic editor':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'LOGIC_EDITOR'
            if self.new_window_type == 'Properties':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'PROPERTIES'
            if self.new_window_type == 'Outliner':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'OUTLINER'
            if self.new_window_type == 'User preferences':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'USER_PREFERENCES'
            if self.new_window_type == 'Info':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'INFO'
            if self.new_window_type == 'File browser':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'FILE_BROWSER'
            if self.new_window_type == 'Python console':
                bpy.context.window_manager.windows[-1].screen.areas[0].type = 'CONSOLE'
            
        return {'FINISHED'}
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box()
        
        row = box.row(align = True)
        row.prop(self, "duplicate_into_new_window")
        row.prop(self, "new_window_type")
        
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)