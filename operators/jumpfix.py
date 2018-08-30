import bpy
import bmesh
import os
import math
import mathutils
from mathutils import Vector
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class jumpFixing(Operator):
    bl_idname = "jump.fix"
    bl_label = "fix neuron jumps"
    bl_options = {'UNDO'}
    
    delete_method = EnumProperty(name = "Method", items = [('Box', 'Box', 'Box'), ('Range', 'Range', 'Range')], default = 'Box', description = "Jump deletion method")

    convert_to_mesh = BoolProperty(name = "Convert to mesh?", default = True, description = "If using the box delete method, curves have to be converted to meshes for vertices to be selected and deleted")
    
    x_point = BoolProperty(name = "X point range", default = False, description = "Remove vertices on x axis")
    
    x_start = FloatProperty(name = "X start", default = -10, min = -100000, max = 100000, description = "Start of x coordinate range")
    
    x_end = FloatProperty(name = "X end", default = 10, min = -100000, max = 100000, description = "End of x coordinate range")
    
    y_point = BoolProperty(name = "Y point range", default = False, description = "Remove vertices on y axis")
    
    y_start = FloatProperty(name = "Y start", default = -10, min = -100000, max = 100000, description = "Start of y coordinate range")
    
    y_end = FloatProperty(name = "Y end", default = 10, min = -100000, max = 100000, description = "End of y coordinate range")
    
    z_point = BoolProperty(name = "Z point range", default = False, description = "Remove vertices on z axis")
    
    z_start = FloatProperty(name = "Z start", default = -10, min = -100000, max = 100000, description = "Start of z coordinate range")
    
    z_end = FloatProperty(name = "Z end", default = 10, min = -100000, max = 100000, description = "End of z coordinate range")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        ob_list = context.selected_objects
        scene = context.scene
        
        if self.delete_method == 'Box':
        
            def IsInBoundingVectors(vector_check, vector1, vector2):
                for i in range(0, 3):
                    if (vector_check[i] < vector1[i] and vector_check[i] < vector2[i]
                        or vector_check[i] > vector1[i] and vector_check[i] > vector2[i]):
                        return False
                return True
            
            def SelectVerticesInBound(object, vector1, vector2):
            # get the mesh data from the object reference
                for ob in ob_list:    
                    
                    mesh = ob.data

                    # get the bmesh data
                    if mesh.is_editmode:
                        bm = bmesh.from_edit_mesh(mesh)
                    else:
                        bm = bmesh.new()
                        bm.from_mesh(mesh)
                    
                    # cycle through all vertices
                    for vert in bm.verts:
                        # check if the vertice is in the bounding vectors
                        # if yes, select it
                        # if no, deselect it
                        if(IsInBoundingVectors(vert.co, vector1, vector2)):
                            vert.select = True
                        else:
                            vert.select = False

                    # update bmesh to mesh
                    if bm.is_wrapped:
                        bmesh.update_edit_mesh(mesh, False, False)
                    else:
                        bm.to_mesh(mesh)
                        mesh.update()
            
            target_object = scene.objects[scene.theChosenObject]
            
            data = target_object.data
            mw = target_object.matrix_world
            
            coords_x = []
            coords_y = []
            coords_z = []
            
            i = 0
            
            for i in range(7):
                i += 1
                lc = data.vertices[i].co
                world_coordinate = mw * lc
                
                coords_x.append(world_coordinate[0])
                coords_y.append(world_coordinate[1])
                coords_z.append(world_coordinate[2])
                
            min_x = min(coords_x)
            min_y = min(coords_y)
            min_z = min(coords_z)
            
            max_x = max(coords_x)
            max_y = max(coords_y)
            max_z = max(coords_z)
            
            for ob in ob_list:   
                scene.objects.active = ob
                
                if self.convert_to_mesh:
                    bpy.ops.object.convert(target='MESH')
                 
                bpy.ops.object.mode_set(mode='EDIT')
                SelectVerticesInBound(ob, Vector((min_x, min_y, min_z)), Vector((max_x, max_y, max_z)))
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.object.mode_set(mode='OBJECT')
                ob.select = False
                
        if self.delete_method == 'Range':
            for ob in ob_list:
                print(ob.type)
                if ob.type != 'CURVE':
                    continue
                
                scene.objects.active = ob
                bpy.ops.object.mode_set(mode='EDIT')
                print('Entered edit mode')
                
                for spline in ob.data.splines:
                    for point in spline.points:
                        if self.x_point:
                            if self.x_start < point.co.x < self.x_end:
                                point.select = True
                        if self.y_point:
                            if self.y_start < point.co.y < self.y_end:
                                point.select = True
                        if self.z_point:
                            if self.z_start < point.co.z < self.z_end:
                                point.select = True
                
                bpy.ops.curve.delete(type='VERT')
                bpy.ops.object.mode_set(mode='OBJECT')
                
                ob.select = False
            
        return {'FINISHED'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box = layout.box()
        row = box.row(align = False)
        
        row.prop(self, "delete_method")
        if self.delete_method == 'Box':
            row = box.row(align = False)
            row.prop(self, "convert_to_mesh")              
            layout.prop_search(scene, "theChosenObject", scene, "objects")
        if self.delete_method == 'Range':
            row = box.row(align = False)
            row.prop(self, "x_point")
            if self.x_point:
                row.prop(self, "x_start")
                row.prop(self, "x_end")
            row = box.row(align = False)
            row.prop(self, "y_point")
            if self.y_point:
                row.prop(self, "y_start")
                row.prop(self, "y_end")
            row = box.row(align = False)
            row.prop(self, "z_point")
            if self.z_point:
                row.prop(self, "z_start")
                row.prop(self, "z_end")
            
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)