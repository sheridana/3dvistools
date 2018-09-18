import bpy
import os
import random
import math
from math import pi, radians, degrees
import colorsys
import mathutils
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class ChangeMaterials(Operator):
    bl_idname = "change.materials"
    bl_label = "change object materials"
    bl_options = {'UNDO'}
    
    which_objects = EnumProperty( name = "Which Objects?", items = [('Selected','Selected','Selected'),('All','All','All'), ('By name','By name','By name')],  default = 'Selected', description = "Give selected objects a common material")
    
    by_name = StringProperty( name = "Object name(s)", description = "Search by object names. Separate multiple names with commas")
    
    partial_match = BoolProperty( name = "Allow partial matches?", default = False, description = "Allow partial matches for object names?")
    
    is_not = BoolProperty( name = "Is not named", default = False, description = "Filter by objects not named")

    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        ob_count = 0
        
        for ob in bpy.data.objects:
            ob_count += 1
        
        #new_mat = bpy.data.materials.new('#Unified material')
        #new_mat.diffuse_color = self.new_color
        
        if self.which_objects == 'Selected':
            ob_list = bpy.context.selected_objects
        elif self.which_objects == 'All':
            ob_list = [ob for ob in bpy.data.objects if ob.type == 'MESH']
        elif self.which_objects == 'By name':
            ob_list = [ob for ob in bpy.data.objects if ob.name == self.by_name] 
            
            if self.partial_match:
                
                #ob_list = [ob for ob in bpy.data.objects if self.by_name.lower() in ob.name.lower() ]
                
                # create the list of names using split.
                names = self.by_name.split(",")
                
                # loop over the split names, concatenate them
                ob_list = []
                
                for name in names:
                    if self.is_not:
                        ob_list += [ob for ob in bpy.data.objects if name.strip().lower() not in ob.name.lower()]
                    else:
                        ob_list += [ob for ob in bpy.data.objects if name.strip().lower() in ob.name.lower()]
            else:
                names = self.by_name.split(",")
                for name in names:
                    if self.is_not:
                        ob_list = [ob for ob in bpy.data.objects if name.strip().lower() != ob.name.lower() ]

        return {'FINISHED'}
