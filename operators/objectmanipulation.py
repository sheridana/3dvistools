import bpy
import math
from math import pi, radians, degrees
import mathutils
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class neuronEditing(Operator):
    bl_idname = "neuron_scale_rotation.location"
    bl_label = "edit neuron scale, rotation, location"
    bl_options = {'UNDO'}
    
    which_objects = EnumProperty( name = "Which Objects?", items = [('Selected','Selected','Selected'), ('All','All','All'), ('By name' , 'By name', 'By name')],  default = 'Selected', description = "Edit object properties")
    
    by_name = StringProperty( name = "Object name(s)", description = "Search by object names. Separate multiple names with commas")
    
    partial_match = BoolProperty( name = "Allow partial matches?", default = False, description = "Allow partial matches for object names?")
    
    is_not = BoolProperty( name = "Is not named?", default = False, description = "Edit objects not named?")
    
    change_origin = BoolProperty( name = "Origin", default = False, description = "Change object origin?")
    
    new_origin = EnumProperty( name = "Set origin", items = [('Geometry to origin', 'Geometry to origin', 'Geometry to origin'), ('Origin to geometry', 'Origin to geometry', 'Origin to geometry'), ('Origin to 3D cursor', 'Origin to 3D cursor', 'Origin to 3D cursor'), ('Origin to center of mass (surface)', 'Origin to center of mass (surface)', 'Origin to center of mass (surface)'), ('Origin to center of mass (volume)', 'Origin to center of mass (volume)', 'Origin to center of mass (volume)')], default = 'Geometry to origin', description = "Set object origin")
    
    change_pivot_point = BoolProperty( name = "Pivot point", default = False, description = "Change object pivot point?")
    
    new_pivot_point = EnumProperty( name = "", items = [('Median point', 'Median point', 'Median point'), ('Active element', 'Active element', 'Active element'), ('Individual origins', 'Individual origins', 'Individual origins'), ('3D cursor', '3D cursor', '3D cursor'), ('Bounding box center', 'Bounding box center', 'Bounding box center')], default = 'Median point', description = "Set object pivot point")
    
    change_scale = BoolProperty(  name = "Scale", default = False, description = "Change object scale?")
    
    new_scale = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new rotation")
    
    change_location = BoolProperty( name = "Location", default = False, description = "Change object location?")
    
    new_location = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new location")
    
    change_rotation = BoolProperty( name = "Rotation", default = False, description = "Change object rotation?")
    
    new_rotation = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new rotation")
    
    smooth_objects = BoolProperty(name = "Smooth objects", default = False, description = "Smooth objects?")
    
    flat_objects = BoolProperty(name = "Flat objects", default = False, description = "Flat objects?")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        ob_count = 0
        
        for ob in bpy.data.objects:
            ob_count += 1
        
        #new_object = bpy.context.active_object
        #new_object.scale = self.new_scale
        #new_object.location = self.new_location
        #new_object.rotation_euler = self.new_rotation
        #bpy.ops.object.origin_set = self.new_origin
        retrieve_by_name = []
        objects_to_select = []
        
        if self.which_objects == 'Selected':
            ob_list = bpy.context.selected_objects
        elif self.which_objects == 'All':
            ob_list = [ob for ob in bpy.data.objects if ob.type == 'MESH' or 'CURVE']
        elif self.which_objects == 'By name':
            ob_list = [ob for ob in bpy.data.objects if ob.name == self.by_name]
            
            if self.partial_match:
     
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
        
        if self.change_origin:
            if self.new_origin == 'Geometry to origin':
                bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
            if self.new_origin == 'Origin to geometry':
                bpy.ops.object.origin_set(type ='ORIGIN_GEOMETRY')
            if self.new_origin == 'Origin to 3D cursor':
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            if self.new_origin == 'Origin to center of mass (surface)': 
                bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS')
            if self.new_origin == 'Origin to center of mass (volume)': 
                bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_VOLUME')
              
        if self.change_pivot_point:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D': 
                            if self.new_pivot_point == 'Median point':
                                space.pivot_point = 'MEDIAN_POINT'
                            if self.new_pivot_point == 'Active element':
                                space.pivot_point = 'ACTIVE_ELEMENT'
                            if self.new_pivot_point == 'Individual origins':
                                space.pivot_point = 'INDIVIDUAL_ORIGINS'
                            if self.new_pivot_point == '3D cursor':
                                space.pivot_point = 'CURSOR'
                            if self.new_pivot_point == 'Bounding box center':
                                space.pivot_point = 'BOUNDING_BOX_CENTER'
        
        for ob in ob_list: 
            if self.change_scale:
                ob.scale = self.new_scale
                #new_object.scale = self.new_scale
            if self.change_location:
                ob.location = self.new_location
                #new_object.location = self.new_location
            if self.change_rotation:
                ob.rotation_euler = self.new_rotation * pi / 180
                #new_object.rotation_euler = self.new_rotation * pi / 180
            if self.smooth_objects:
                bpy.ops.object.shade_smooth()
            if self.flat_objects:
                bpy.ops.object.shade_flat()
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Apply to:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "which_objects")
        
        row = box.row(align = False)
        row.prop(self, "by_name")
        
        row = box.row(align = False)
        row.prop(self, "partial_match")
        row.prop(self, "is_not")
        
        layout.label(text="Change:")
        box = layout.box()
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_origin")
        col = row.column()
        col.prop(self, "new_origin")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_pivot_point")
        col = row.column()
        col.prop(self, "new_pivot_point")
        
        
        box = layout.box()
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_scale")      
        col = row.column()
        col.prop(self, "new_scale")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_location")
        col = row.column()
        col.prop(self, "new_location")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_rotation")
        col = row.column()
        col.prop(self, "new_rotation")
        
        box = layout.box()
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "smooth_objects")
        col = row.column()
        col.prop(self, "flat_objects")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)