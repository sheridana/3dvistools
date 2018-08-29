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
    
    create_new_material = BoolProperty( name = "Create new material?", default = False, description = "Create new material if none exist?")
    
    change_color = BoolProperty( name = "Single color", default = False, description = 'Change object color?')
    
    new_color = FloatVectorProperty( name = "", default = (0.0, 1.0, 0.0), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set color")
    
    change_diffuse_intensity = BoolProperty( name = "Diffuse intensity", default = False, description = "Change object diffuse intensity?")
    
    new_diffuse_intensity = FloatProperty( name = "", default = .8, min = 0, max = 1, description = "Set diffuse intensity value")
    
    change_specular_intensity = BoolProperty( name = "Specular intensity", default = False, description = "Change object specular intensity?")
    
    new_specular_intensity = FloatProperty( name = "", default = .5, min = 0, max = 1, description = "Set specular intensity value")
    
    change_emit = BoolProperty( name = 'Emit', default = False, description = "Change object light emit?")
    
    new_emit = FloatProperty( name = "", default = 1, min = 0, max = 5, description = "Set new emit value")
    
    change_transparency = BoolProperty( name = "Transparency", default = False, description = 'Change object transparency?')
    
    new_transparency = EnumProperty( name = "", items = [('Mask', 'Mask', 'Mask'), ('Z-Transparency', 'Z-Transparency', 'Z-Transparency'), ('Raytrace', 'Raytrace', 'Raytrace')], default = 'Z-Transparency', description = "Set new transparency type")
    
    change_alpha = BoolProperty( name = "Alpha", default = False, description = 'Change alpha value?')
    
    new_alpha = FloatProperty( name = "", default = 1, min = 0, max = 1, description = "Set new alpha value")
    
    change_specular = BoolProperty( name = "Specular", default = False, description = "Change specular value?")
    
    new_specular = FloatProperty( name = "", default = 1, min = 0, max = 1, description = "Set new specular value")
    
    change_fresnel = BoolProperty( name = "Fresnel", default = False, description = "Change fresnel value?")
    
    new_fresnel = FloatProperty( name = "", default = 0, min = 0, max = 5, description = "Set new fresnel value")
    
    change_material_type = BoolProperty( name = "Material type", default = False, description = "Change material type?")
    
    new_material_type = EnumProperty( name = "", items = [('Surface', 'Surface', 'Surface'), ('Wire', 'Wire', 'Wire')], description = "Set new material type")
    
    random_color =  BoolProperty( name = "Random color", default = False, description = "Generate random color?")
    
    red_start = FloatProperty( name = "Red start", default = 0, min = 0, max = 255, description = "set start red channel range")
    
    red_end = FloatProperty( name = "Red end", default = 255, min = 0, max = 255, description = "set end red channel range")
    
    green_start = FloatProperty( name = "Green start", default = 0, min = 0, max = 255, description = "set start green channel range")
    
    green_end = FloatProperty( name = "Green end", default = 255, min = 0, max = 255, description = "set end green channel range")
    
    blue_start = FloatProperty( name = "Blue start", default = 0, min = 0, max = 255, description = "set start blue channel range")
    
    blue_end = FloatProperty( name = "Blue end", default = 255, min = 0, max = 255, description = "set end blue channel range")

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
                    
            #for n in [x.strip() for x in self.by_name.split(',')]:
                #retrieve_by_name += n, self.partial_match
                
            #retrieve_by_name = [str(e) for e in retrieve_by_name]
            
        for ob in ob_list:
            
            mat = bpy.data.materials.get("Material")
            #mat.diffuse_color = self.new_color
            
            if self.create_new_material:
                
                mat = bpy.data.materials.new(name="Material")
                
                if ob.data.materials:
                    # assign to 1st material slot
                    ob.data.materials[0] = mat
                else:
                    # no slots
                    ob.data.materials.append(mat)
            
            if self.change_color:
                ob.active_material.diffuse_color = self.new_color
            
            if self.random_color:
                
                if self.create_new_material:
                    
                    matLen = len(ob.data.materials)
                    
                    r = random.randint( self.red_start, self.red_end)
                    g = random.randint( self.green_start, self.green_end)
                    b = random.randint( self.blue_start, self.blue_end)
                    
                    mat.diffuse_color = (r/255, g/255, b/255)
                
                else:
                    matLen = len(ob.data.materials)
                    
                    r = random.randint( self.red_start, self.red_end)
                    g = random.randint( self.green_start, self.green_end)
                    b = random.randint( self.blue_start, self.blue_end)
                    
                    mat = ob.active_material
                    
                    mat.diffuse_color = (r/255, g/255, b/255)
                    
                    
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.object.material_slot_assign()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    

            if self.change_emit:
                ob.active_material.emit = self.new_emit
            if self.change_transparency:
                if self.new_transparency == 'Mask':
                    ob.active_material.use_transparency = True
                    ob.active_material.transparency_method = 'MASK'
                if self.new_transparency == 'Z-Transparency':
                    ob.active_material.use_transparency = True
                    ob.active_material.transparency_method = 'Z_TRANSPARENCY'
                if self.new_transparency == 'Raytrace':
                    ob.active_material.use_transparency = True
                    ob.active_material.transparency_method = 'RAYTRACE'
            if self.change_alpha:
                ob.active_material.alpha = self.new_alpha
            if self.change_specular:
                ob.active_material.specular_alpha = self.new_specular
            if self.change_fresnel:
                ob.active_material.raytrace_transparency.fresnel = self.new_fresnel
            if self.change_material_type:
                if self.new_material_type == 'Surface':
                    ob.active_material.type = 'SURFACE'
                if self.new_material_type == 'Wire':
                    ob.active_material.type = 'WIRE' 
            if self.change_diffuse_intensity:
                ob.active_material.diffuse_intensity = self.new_diffuse_intensity
            if self.change_specular_intensity:
                ob.active_material.specular_intensity = self.new_specular_intensity
                
        self.report( {'INFO'}, '%i materials changed' % len(ob_list) )
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Apply to:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "which_objects")
        if self.which_objects == 'By name':
            row = box.row(align = False)
            row.prop(self, "by_name")
            row = box.row(align = False)
            row.prop(self, "partial_match")
            row.prop(self, "is_not")
        row = box.row(align = False)
        row.prop(self, "create_new_material")
        
        layout.label(text="Change:")
        box = layout.box()
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_color")
        col = row.column()
        col.prop(self, "new_color")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_diffuse_intensity")
        col = row.column()
        col.prop(self, "new_diffuse_intensity")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_specular_intensity")
        col = row.column()
        col.prop(self, "new_specular_intensity")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_emit")
        col = row.column()
        col.prop(self, "new_emit")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_material_type")
        col = row.column()
        col.prop(self, "new_material_type")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_transparency")
        if self.change_transparency:
            col = row.column()
            col.prop(self, "new_transparency")
            
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_alpha")
            col = row.column()
            col.prop(self, "new_alpha")
            
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_specular")
            col = row.column()
            col.prop(self, "new_specular")
            
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_fresnel")
            col = row.column()
            col.prop(self, "new_fresnel")
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "random_color")
        if self.random_color:
            row = box.row(align = False)
            row.prop(self, "red_start")
            row.prop(self, "red_end")
            row = box.row(align = False)
            row.prop(self, "green_start")
            row.prop(self, "green_end")
            row = box.row(align = False)
            row.prop(self, "blue_start")
            row.prop(self, "blue_end")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)