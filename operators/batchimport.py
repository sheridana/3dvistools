import bpy
import os
import math
from math import pi, radians, degrees
import mathutils
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class batchImport(Operator):
    bl_idname = "batch.import"
    bl_label = "batch import"
    bl_options = {'UNDO'}
    
    which_operating_system = EnumProperty( name = "Operating system?", items = [('UNIX', 'UNIX', 'UNIX'), ('Windows', 'Windows', 'Windows')], default = 'UNIX', description = "Change the operating system?")
    
    which_import_method = EnumProperty( name = "Import method?", items = [('OBJ', 'OBJ', 'OBJ'), ('RAW', 'RAW', 'RAW')], default = 'OBJ', description = "Change the import method?")
    
    path_to_data = StringProperty( name="Path to data?", description="Choose a directory:", default="", maxlen=1024, subtype='DIR_PATH')

    memory_constraint = BoolProperty(name = "Memory constraint?", default = False, description = "If importing very large objects (vertex count) or a lot of objects, use this method")

    decimate_objects = BoolProperty(name = "Decimate?", default = False, description = "Decimate objects as they are imported (useful for objects with high vertex counts)")
    
    decimate_ratio = FloatProperty(name = "Ratio", default = 0.5, min = 0.0, max = 1.0, description = "Ratio of triangles to reduce to (uses collapse method, see useful modifiers for other decimation options)")

    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        if self.which_operating_system == 'UNIX':
            path_to_obj_dir = self.path_to_data
        elif self.which_operating_system == 'Windows':
            path_to_obj_dir = os.path.join(self.path_to_data)
            
        file_list = sorted(os.listdir(path_to_obj_dir))
        
        if self.which_import_method == 'RAW':
            obj_list = [item for item in file_list if item.endswith('.raw')]
        elif self.which_import_method == 'OBJ':
            obj_list = [item for item in file_list if item.endswith('.obj')]
        
        for item in obj_list:
            path_to_file = os.path.join(path_to_obj_dir, item)
            if self.which_import_method == 'RAW':
                from io_mesh_raw import import_raw
                import_raw.read(path_to_file)
                #print("Importing", item)
            else:
                bpy.ops.import_scene.obj(filepath = path_to_file)

            if self.decimate_objects:
                if self.memory_constraint:
                    for obj in bpy.context.selected_objects:
                        bpy.context.scene.objects.active = obj
                        bpy.ops.object.modifier_add(type='DECIMATE')
                        #print("(method 1) Added decimate modifier to", item)
                        dec = obj.modifiers['Decimate']
                        dec.ratio = self.decimate_ratio
                        bpy.ops.object.modifier_apply(modifier='Decimate')
                        #print("(method 1) Applying decimate modifier to", item)

        if not self.memory_constraint:        
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    obj.select = True
                bpy.context.scene.objects.active = obj

            bpy.ops.object.modifier_add(type='DECIMATE')
            #print("(method 2) Added decimate modifier to", obj.name)
            dec = obj.modifiers['Decimate']
            dec.ratio = self.decimate_ratio
            bpy.ops.object.make_links_data(type='MODIFIERS')
            #print("(method 2) linking modifiers")
            bpy.ops.object.convert(target='MESH')
            #print("(method 2) converting to mesh")
                
        return {'FINISHED'}
                
                    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Change")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "which_operating_system")
        row = box.row(align = False)
        row.prop(self, "which_import_method")
        row = box.row(align = False)
        row.prop(self, "path_to_data")
        row = box.row(align = False)
        row.prop(self, "decimate_objects")
        if self.decimate_objects:
            row.prop(self, "memory_constraint")
            row.prop(self, "decimate_ratio")
        
        
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)
    
def register():
    bpy.utils.register_module(__name__)
    

def unregister():
    bpy.utils.unregister_module(__name__)
   
if __name__ == '__main__':
    register()