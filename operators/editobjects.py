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

class editObjects(Operator):
    bl_idname = "edit.objects"
    bl_label = "Edit objects"
    bl_options = {'UNDO'}
    
    which_objects = EnumProperty( name = "Which Objects?", items = [('Selected','Selected','Selected'),('All','All','All'), ('By name','By name','By name')],  default = 'Selected', description = "Give selected objects a common material")
    
    by_name = StringProperty( name = "Object name(s)", description = "Search by object names. Separate multiple names with commas")
    
    partial_match = BoolProperty( name = "Allow partial matches?", default = False, description = "Allow partial matches for object names?")
    
    is_not = BoolProperty( name = "Is not named", default = False, description = "Filter by objects not named")
    
    edit_objects = BoolProperty(name = "Edit objects", default = False, description = "Edit object vertices, edges, or faces")
    
    edit_mode = EnumProperty(name = "Mode", items = [('Vertices', 'Vertices', '', 'VERTEXSEL', 0), ('Edges', 'Edges', '', 'EDGESEL', 1), ('Faces', 'Faces', '', 'FACESEL', 2)], default = 'Vertices', description = "Change edit mode to vertices, edges, or faces")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "which_objects")
        if self.which_objects == 'By name':
            row = box.row(align = False)
            row.prop(self, "by_name")
            row = box.row(align = False)
            row.prop(self, "partial_match")
            row.prop(self, "is_not")
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "edit_objects")
        row.prop(self, "edit_mode")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)