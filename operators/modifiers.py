import bpy
import math
from math import pi, radians, degrees
import colorsys
import mathutils
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class neuronModifiers(Operator):
    bl_idname = "neuron.modifiers"
    bl_label = "Modifiers"
    bl_options = {'UNDO'}
    
    ### Add modifier
    add_modifier = BoolProperty( name = "Add modifier?", default = False, description = "Add modifier to active object?")
    
    remove_modifier = BoolProperty( name = "Remove modifier", default = False, description = "Remove modifier from active object?")
    
    which_modifier = EnumProperty( name = "Modifier", items = [('Boolean', 'Boolean', '', 'MOD_BOOLEAN', 0), ('Decimate', 'Decimate', '', 'MOD_DECIM', 1), ('Shrinkwrap', 'Shrinkwrap', '', 'MOD_SHRINKWRAP', 2), ('Smooth', 'Smooth', '', 'MOD_SMOOTH', 3), ('Wireframe', 'Wireframe', '', 'MOD_WIREFRAME', 4), ('None', 'None', 'None')], default = 'None', description = "Which modifier to add to active object?")
    
    ### decimate modifier
    
    which_decimate = EnumProperty( name = "Type", items = [('Collapse', 'Collapse', 'Collapse'), ('Un-subdivide', 'Un-subdivide', 'Un-subdivide'), ('Planar', 'Planar', 'Planar')], default = 'Collapse', description = "Which decimation method?")
    
    collapse_ratio = FloatProperty( name = "Ratio", default = 1, min = 0, max = 1, description = "Ratio of triangles to reduce to")
    
    collapse_triangulate = BoolProperty( name = "Triangulate", default = False, description = "Keep triangulated faces resulting from decimation")
    
    collapse_symmetry = BoolProperty( name = "Symmetry", default = False, description = "Maintain symmetry on an axis")
    
    collapse_symmetry_direction = EnumProperty( name = "", items = [('Z','Z', 'Z'), ('Y', 'Y', 'Y'), ('X', 'X', 'X')], default = 'X', description = "Symmetry axis")
    
    unsubdivide_iterations = FloatProperty( name = "Iterations", default = 0, min = 0, max = 100, description = "Number of times to reduce the geometry")
    
    angle_limit = FloatProperty( name = "Angle limit", default = 0, min = 0, max = 180, description = "Only dissolve angles below this threshold")
    
    all_boundaries = BoolProperty( name = "All boundaries", default = False, description = "Dissolve all vertices inbetween face boundaries")
    
    ### link modifier
    link_modifiers = BoolProperty( name = "Link modifiers", default = False, description = "Link active object modifiers to selected objects")
    
    convert_to_curve_from_mesh = BoolProperty( name = "Convert to curve", default = False, description = "Convert objects to curve from mesh (applies modifiers to all selected objects)")
    
    convert_to_mesh_from_curve = BoolProperty( name = "Convert to mesh", default = False, description = "Convert objects to mesh from curve (applies modifiers to all selected objects)")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        obj = bpy.context.active_object
        
        if self.add_modifier:
            bpy.ops.object.modifier_add(type=self.which_modifier.upper())
            dec = obj.modifiers['Decimate']
            if self.which_decimate == 'Collapse':
                dec.decimate_type = 'COLLAPSE'
                dec.ratio = self.collapse_ratio
                    
                if self.collapse_triangulate:
                    dec.use_collapse_triangulate = True
                else:
                    dec.use_collapse_triangulate = False
                    
                if self.collapse_symmetry:
                    dec.use_symmetry = True
                    if self.collapse_symmetry_direction == 'X':
                        dec.symmetry_axis = 'X'
                    if self.collapse_symmetry_direction == 'Y':
                        dec.symmetry_axis = 'Y'
                    if self.collapse_symmetry_direction == 'Z':
                        dec.symmetry_axis = 'Z' 
                else:
                    dec.use_symmetry = False   
                    
            elif self.which_decimate == 'Un-subdivide':
                dec.decimate_type = 'UNSUBDIV'
                dec.iterations = self.unsubdivide_iterations
                    
            elif self.which_decimate == 'Planar':
                dec.decimate_type = 'DISSOLVE'
                dec.angle_limit = self.angle_limit * pi / 180
                if self.all_boundaries:
                    dec.use_dissolve_boundaries = True
                else:
                    dec.use_dissolve_boundaries = False


            
        if self.remove_modifier:
            ob_list = bpy.context.selected_objects
            for ob in ob_list:
                ob.modifiers.remove(ob.modifiers.get(self.which_modifier))
        
        #ob_list = bpy.context.selected_objects
            
        
        if self.link_modifiers:
            bpy.ops.object.make_links_data(type='MODIFIERS')

        if self.convert_to_mesh_from_curve:
            bpy.ops.object.convert(target='MESH')
                
        if self.convert_to_curve_from_mesh:
            bpy.ops.object.convert(target='CURVE')
         
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Apply modifiers to active object")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "add_modifier")
        row.prop(self, "remove_modifier")
        row.prop(self, "which_modifier")
        if self.which_modifier == 'Decimate':
            row = box.row(align = False)
            row.prop(self, "which_decimate")
            if self.which_decimate == 'Collapse':
                row = box.row(align = False)
                row.prop(self, "collapse_ratio")
                row = box.row(align = False)
                row.prop(self, "collapse_triangulate")
                row.prop(self, "collapse_symmetry")
                row.prop(self, "collapse_symmetry_direction")
                row = box.row(align = False)
            elif self.which_decimate == 'Un-subdivide':
                row = box.row(align = False)
                row.prop(self, "unsubdivide_iterations")
            elif self.which_decimate == 'Planar':
                row = box.row(align = False)
                row.prop(self, "angle_limit")
                row.prop(self, "all_boundaries")
        
        layout.label(text = "Link modifiers to selected objects")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "link_modifiers")
        row.prop(self, "convert_to_curve_from_mesh")
        row.prop(self, "convert_to_mesh_from_curve")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)