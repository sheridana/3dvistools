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
       
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        def IsInBoundingVectors(vector_check, vector1, vector2):
            for i in range(0, 3):
                if (vector_check[i] < vector1[i] and vector_check[i] < vector2[i]
                    or vector_check[i] > vector1[i] and vector_check[i] > vector2[i]):
                    return False
            return True
        
        def SelectVerticesInBound(object, vector1, vector2):
        # get the mesh data from the object reference
            for ob in bpy.context.selected_objects:    
                
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
        
        scene = context.scene
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
        
        for ob in bpy.context.selected_objects:   
            bpy.context.scene.objects.active = ob
             
            bpy.ops.object.mode_set(mode='EDIT')
            SelectVerticesInBound(ob, Vector((min_x, min_y, min_z)), Vector((max_x, max_y, max_z)))
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.mode_set(mode='OBJECT')
            ob.select = False
            
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene               
        layout.prop_search(scene, "theChosenObject", scene, "objects")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)