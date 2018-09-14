import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty
from bpy.types import Operator, AddonPreferences
import math
from math import pi, radians, degrees
import mathutils
import sys

class boundingBox(Operator):
    bl_idname = "bounding.box"
    bl_label = "Create bounding box"
    bl_options = {'UNDO'}
    
    bounding_box = EnumProperty( name = "Bounding box", items = [('Single', 'Single', 'Single'), ('Individual', 'Individual', 'Individual')], default = 'Single', description = "Type of bounding box(es) to generate")
    
    box_color = FloatVectorProperty( name = "Bbox color", default = (0.0, 1.0, 0.0), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set color")
    
    use_wireframe = BoolProperty( name = "Wireframe", default = False, description = "Use wireframe?")
    
    change_thickness = FloatProperty(name = "Thickness", default = 0.02, min = 0, max = 1, description = "Wireframe thickness")
    
    change_offset = FloatProperty(name = "Offset", default = 0, min = -5, max = 5, description = "Wireframe offset")
    
    relative_thickness = BoolProperty( name = "Relative thickness", default = False, description = "Use relative thickness?")
    
    apply_wireframe = BoolProperty( name = "Apply wireframe?", default = False, description = "If left unchecked, wireframe will be set but still manipulatable, if checked wireframe will be applied and no longer manipulatable (will remove modifier from modifier stack)")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        selected = context.selected_objects
        data = bpy.data.objects
        scene = context.scene
        layers = scene.render.layers
        active_layer = layers.active
        
        if self.bounding_box == 'Single':
            for ob in selected:
                new_ob = ob.copy()
                new_ob.data = ob.data.copy()
                scene.objects.link(new_ob)
                
                ob.select = False
            for ob in data:
                if active_layer:
                    scene.objects.active = ob
                    if ".00" in ob.name:
                        bpy.ops.object.join()
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                        bpy.ops.mesh.primitive_cube_add()
                        bounding_box = bpy.context.active_object
                    
                        bounding_box.dimensions = ob.dimensions
                        bounding_box.location = ob.location
                        bounding_box.rotation_euler = ob.rotation_euler
                        
                        bounding_box.select = False
                        ob.select = True
                        
            bpy.ops.object.delete()
             
            scene.objects.active = bounding_box
            mat = bpy.data.materials.new(name="Material")
            if bounding_box.data.materials:
                    # assign to 1st material slot
                    bounding_box.data.materials[0] = mat
            else:
                # no slots
                bounding_box.data.materials.append(mat)
                
            bounding_box.active_material.diffuse_color = self.box_color
            
            if self.use_wireframe:
                bpy.ops.object.modifier_add(type='WIREFRAME')
                wf = bounding_box.modifiers['Wireframe']
                if self.change_thickness:
                    wf.thickness = self.change_thickness
                if self.relative_thickness:
                    wf.use_relative_offset = self.relative_thickness
                if self.change_offset:
                    wf.offset = self.change_offset
                bounding_box.select = True
                if self.apply_wireframe:
                    bpy.ops.object.convert(target='MESH')
                
        elif self.bounding_box == 'Individual':
            for ob in selected:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                bpy.ops.mesh.primitive_cube_add()
                bounding_box = bpy.context.active_object
                bounding_box.dimensions = ob.dimensions
                bounding_box.location = ob.location
                bounding_box.rotation_euler = ob.rotation_euler
            
            for ob in data:
                if active_layer:
                    if "Cube" in ob.name:
                        ob.select = True
                        mat = bpy.data.materials.new(name="Material")
                        if ob.data.materials:
                            # assign to 1st material slot
                            ob.data.materials[0] = mat
                        else:
                            # no slots
                            ob.data.materials.append(mat)
                            
                        ob.active_material.diffuse_color = self.box_color
                        
            if self.use_wireframe:
                bpy.ops.object.modifier_add(type='WIREFRAME')
                wf = bounding_box.modifiers['Wireframe']
                if self.change_thickness:
                    wf.thickness = self.change_thickness
                if self.relative_thickness:
                    wf.use_relative_offset = self.relative_thickness
                if self.change_offset:
                    wf.offset = self.change_offset
                
            bpy.ops.object.make_links_data(type='MODIFIERS')
            if self.apply_wireframe:
                bpy.ops.object.convert(target='MESH')
                
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "bounding_box")
        row.prop(self, "box_color")
        row = box.row(align = False)
        row.prop(self, "use_wireframe")
        if self.use_wireframe:
            row.prop(self, "change_thickness")
            row.prop(self, "relative_thickness")
            row = box.row(align = False)
            row.prop(self, "change_offset")
            row.prop(self, "apply_wireframe")
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)

def register():
    bpy.utils.register_module(__name__)
    

def unregister():
    bpy.utils.unregister_module(__name__)
   
if __name__ == '__main__':
    register()
