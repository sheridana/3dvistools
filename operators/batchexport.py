import bpy
import os
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class batchExport(Operator):
    bl_idname = "batch.export"
    bl_label = "batch export objects"
    bl_options = {'UNDO'}
    
    which_operating_system = EnumProperty( name = "Operating system", items = [('UNIX', 'UNIX', 'UNIX'), ('Windows', 'Windows', 'Windows')], default = 'UNIX', description = "Change the operating system?")
    
    which_export_method = EnumProperty( name = "Export method", items = [('OBJ', 'OBJ', 'OBJ'), ('RAW', 'RAW', 'RAW'), ('JSON', 'JSON', 'JSON')], default = 'JSON', description = "Change the import method?")
    
    path_to_base_directory = StringProperty( name="Path to blender file", description="Path to blender file:", default="", maxlen=1024, subtype='DIR_PATH')
    
    path_to_single_export = StringProperty( name="Single folder export path", description="Single folder export path:", default="", maxlen=1024, subtype='DIR_PATH')
    
    path_to_algorithm_1 = StringProperty( name="Algorithm 1 export path", description="Algorithm 1 export path:", default="", maxlen=1024, subtype='DIR_PATH')
        
    path_to_algorithm_2 = StringProperty( name="Algorithm 2 export path", description="Algorithm 2 export path:", default="", maxlen=1024, subtype='DIR_PATH')
        
    path_to_algorithm_3 = StringProperty( name="Algorithm 3 export path", description="Algorithm 3 export path:", default="", maxlen=1024, subtype='DIR_PATH')
        
    path_to_ground_truth = StringProperty( name="Ground truth export path:", description="Ground truth export path", default="", maxlen=1024, subtype='DIR_PATH')
    
    def execute(self, context):
        
        
        return {'FINISHED'}
        
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Change:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "which_operating_system")
        row = box.row(align = False)
        row.prop(self, "which_export_method")
        row = box.row(align = False)
        row.prop(self, "path_to_base_directory")
        row = box.row(align = False)
        row.prop(self, "path_to_single_export")
        row = box.row(align = False)
        row.prop(self, "path_to_algorithm_1")
        row = box.row(align = False)
        row.prop(self, "path_to_algorithm_2")
        row = box.row(align = False)
        row.prop(self, "path_to_algorithm_3")
        row = box.row(align = False)
        row.prop(self, "path_to_ground_truth")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)