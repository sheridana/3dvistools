import bpy
import os
import re
import random
import time
import math
from math import pi, radians, degrees
import colorsys
import mathutils
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty
        
class plugin(Operator):
    bl_idname = "test.plugin"
    bl_label = "plugin"
    bl_options = {'UNDO'}
    
    clear_scene = BoolProperty( name = "Clear scene?", default = False, description = "Clear default cube, lamp, and camera?")
    
    which_operating_system = EnumProperty( name = "Operating system?", items = [('UNIX', 'UNIX', 'UNIX'), ('Windows', 'Windows', 'Windows')], default = 'UNIX', description = "Change the operating system?")
    
    which_import_method = EnumProperty( name = "Import method?", items = [('OBJ', 'OBJ', 'OBJ'), ('RAW', 'RAW', 'RAW')], default = 'OBJ', description = "Change the import method?")
    
    path_to_data = StringProperty( name="Path to data?", description="Choose a directory:", default="", maxlen=1024, subtype='DIR_PATH')
    
    decimate_objects = BoolProperty( name = "Decimate?", default = False, description = "Add decimate modifier to objects?")
    
    decimate_ratio = FloatProperty( name = "Ratio", default = 1, min = 0, max = 1, description = "Ratio of triangles to reduce to")
    
    #edit objects
    
    change_origin = BoolProperty( name = "Origin", default = False, description = "Change object origin?")
    
    new_origin = EnumProperty( name = "Set origin", items = [('Geometry to origin', 'Geometry to origin', 'Geometry to origin'), ('Origin to geometry', 'Origin to geometry', 'Origin to geometry'), ('Origin to 3D cursor', 'Origin to 3D cursor', 'Origin to 3D cursor'), ('Origin to center of mass (surface)', 'Origin to center of mass (surface)', 'Origin to center of mass (surface)'), ('Origin to center of mass (volume)', 'Origin to center of mass (volume)', 'Origin to center of mass (volume)')], default = 'Geometry to origin', description = "Set object origin")
    
    change_scale = BoolProperty( name = "Scale", default = False, description = "Change object scale?")
    
    new_scale = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new rotation")
    
    change_location = BoolProperty( name = "Location", default = False, description = "Change object location")
    
    new_location = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new location")
    
    change_rotation = BoolProperty( name = "Rotation", default = False, description = "Change object rotation?")
    
    new_rotation = FloatVectorProperty( name = "", default = (0.0, 0.0, 0.0), min = -100000, max = 100000, subtype = 'XYZ', description = "give object new rotation")
    
    smooth_objects = BoolProperty( name = "Smooth objects", default = False, description = "Render faces smooth, using interpolated vertex normals")
    
    
    #materials
    
    create_new_material = BoolProperty( name = "Create new material(s)?", default = False, description = "Create new material(s) for objects?")
    
    change_color = BoolProperty( name = "Single color", default = False, description = "Give objects single color?")
    
    random_color = BoolProperty( name = "Random colors", default = False, description = "Give objects random colors?")
    
    new_color = FloatVectorProperty( name = "", default = (0.033, 0.495, .827), min = 0.0, max = 1.0, subtype = 'COLOR', description = "Set color")
    
    red_start = FloatProperty( name = "Red start", default = 0, min = 0, max = 255, description = "set start red channel range")
    
    red_end = FloatProperty( name = "Red end", default = 255, min = 0, max = 255, description = "set end red channel range")
    
    green_start = FloatProperty( name = "Green start", default = 0, min = 0, max = 255, description = "set start green channel range")
    
    green_end = FloatProperty( name = "Green end", default = 255, min = 0, max = 255, description = "set end green channel range")
    
    blue_start = FloatProperty( name = "Blue start", default = 0, min = 0, max = 255, description = "set start blue channel range")
    
    blue_end = FloatProperty( name = "Blue end", default = 255, min = 0, max = 255, description = "set end blue channel range") 
    
    change_emit = BoolProperty( name = 'Emit', default = False, description = "Change object light emit?")
    
    new_emit = FloatProperty( name = "", default = 1, min = 0, max = 5, description = "Set new emit value")
    
    change_transparency = BoolProperty( name = "Transparency", default = False, description = 'Change object transparency?')
    
    new_transparency = EnumProperty( name = "", items = [('None', 'None', 'None'), ('Mask', 'Mask', 'Mask'), ('Z-Transparency', 'Z-Transparency', 'Z-Transparency'), ('Raytrace', 'Raytrace', 'Raytrace')], description = "Set new transparency type")
    
    change_alpha = BoolProperty( name = "Alpha", default = False, description = 'Change alpha value?')
    
    new_alpha = FloatProperty( name = "", default = 1, min = 0, max = 1, description = "Set new alpha value")
    
    change_specular = BoolProperty( name = "Specular", default = False, description = "Change specular value?")
    
    new_specular = FloatProperty( name = "", default = 1, min = 0, max = 1, description = "Set new specular value")
    
    change_fresnel = BoolProperty( name = "Fresnel", default = False, description = "Change fresnel value?")
    
    new_fresnel = FloatProperty( name = "", default = 0, min = 0, max = 5, description = "Set new fresnel value")
    
    change_material_type = BoolProperty( name = "Material type", default = False, description = "Change material type?")
    
    new_material_type = EnumProperty( name = "", items = [('Surface', 'Surface', 'Surface'), ('Wire', 'Wire', 'Wire')], description = "Set new material type")
    
    #select objects
    select_all_objects = BoolProperty( name = "Select all", default = False, description = "Selected all objects after import")
    
    #duplicate objects 
    
    duplicate_objects = BoolProperty( name = "Duplicate", default = False, description = "Duplicate objects")
    
    #edit vertices
    
    edit_mesh_vertices = BoolProperty( name = "Edit vertices", default = False, description = "Edit mesh vertices?")
    
    dilate_erode_vertices = BoolProperty( name = "Dilate/Erode mesh vertices", default = False, description = "Fatten/Shrink vertices of mesh")
    
    dilate_erode_copy_vertices = BoolProperty( name = "Dilate/Erode mesh copy vertices", default = False, description = "Fatten/shrink vertices of mesh copy")
    
    dilate_erode_value = FloatProperty( name = "Dilate/Erode value", default = 0, max = 50, min = -50, description = "Vertex dilation/erosion value")
    
    dilate_erode_copy_value = FloatProperty( name = "Dilate/Erode copy value", default = 0, max = 50, min = -50, description = "Vertex dilation/erosion value for copy")
    
    flip_normals = BoolProperty( name = "Flip normals", default = False, description = "Flip direction of face normals (need to do this if exporting to three.js)")
    
    print_output = BoolProperty( name = "Print output to terminal", default = False, description = "Print script output to terminal")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        if self.clear_scene:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
        
        if self.which_operating_system == 'UNIX':
            path_to_obj_dir = self.path_to_data
        elif self.which_operating_system == 'Windows':
            path_to_obj_dir = os.path.join(self.path_to_data)
            
        file_list = sorted(os.listdir(path_to_obj_dir))
        
        if self.which_import_method == 'RAW':
            obj_list = [item for item in file_list if item.endswith('.raw')]
        elif self.which_import_method == 'OBJ':
            obj_list = [item for item in file_list if item.endswith('.obj')]
        
        start_time = time.time()
        
        for item in obj_list:
            path_to_file = os.path.join(path_to_obj_dir, item)
            if self.which_import_method == 'RAW':
                from io_mesh_raw import import_raw
                import_raw.read(path_to_file)
                
                if self.print_output:
                    print('Importing', item)
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print('\n')
                
            else:
                bpy.ops.import_scene.obj(filepath = path_to_file)
             
            
            for obj in bpy.context.selected_objects:
            #obj = bpy.context.active_object
            
                bpy.context.scene.objects.active = obj
                #print(obj)

                if self.decimate_objects:
                    bpy.ops.object.modifier_add(type='DECIMATE')
                    '''print('Adding decimate modifier to', item)
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')'''
                    dec = obj.modifiers['Decimate']
                    dec.ratio = self.decimate_ratio
                    '''print('Decimating %s with a %s ratio' % (item, self.decimate_ratio))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')'''
                    
                    bpy.ops.object.modifier_apply(modifier='Decimate')
                    #bpy.ops.object.convert(target='MESH')
                    '''print('Applying decimate modifier to', item)
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')'''
                    
                    
                if self.change_origin:
                    if self.new_origin == 'Geometry to origin':
                        bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
                        print('Setting %s geometry to origin' % (item))
                        for i in range(21):
                            sys.stdout.write('\r')
                            # the exact output you're looking for:
                            sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                            sys.stdout.flush()
                            sleep(0.25)
                        print('  DONE')
                        print('\n')
                    if self.new_origin == 'Origin to geometry':
                        bpy.ops.object.origin_set(type ='ORIGIN_GEOMETRY')
                        print('Setting %s orgin to geometry' % (item))
                        for i in range(21):
                            sys.stdout.write('\r')
                            # the exact output you're looking for:
                            sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                            sys.stdout.flush()
                            sleep(0.25)
                        print('  DONE')
                        print('\n')
                    if self.new_origin == 'Origin to 3D cursor':
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                        print('Setting %s origin to 3d cursor' % (item))
                        for i in range(21):
                            sys.stdout.write('\r')
                            # the exact output you're looking for:
                            sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                            sys.stdout.flush()
                            sleep(0.25)
                        print('  DONE')
                        print('\n')
                    if self.new_origin == 'Origin to center of mass (surface)': 
                        bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_MASS')
                        print('Setting %s origin to center of mass(surface)' % (item))
                        for i in range(21):
                            sys.stdout.write('\r')
                            # the exact output you're looking for:
                            sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                            sys.stdout.flush()
                            sleep(0.25)
                        print('  DONE')
                        print('\n')
                    if self.new_origin == 'Origin to center of mass (volume)': 
                        bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_VOLUME')
                        print('Setting %s origin to center of mass(volume)' % (item))
                        for i in range(21):
                            sys.stdout.write('\r')
                            # the exact output you're looking for:
                            sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                            sys.stdout.flush()
                            sleep(0.25)
                        print('  DONE')
                        print('\n')
                        
                if self.change_scale:
                    obj.scale = self.new_scale
                    print('Changing %s scale to X: %s Y: %s  Z: %s' % (item, self.new_scale[0], self.new_scale[1], self.new_scale[2]))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')
                if self.change_location:
                    obj.location = self.new_location
                    print('Changing %s location to X: %s Y: %s Z: %s' % (item, self.new_location[0], self.new_location[1], self.new_location[2]))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')                  
                if self.change_rotation:
                    obj.rotation_euler = self.new_rotation * pi / 180
                    print('Changing %s rotation to X: %s Y: %s Z: %s' % (item, self.new_rotation[0], self.new_rotation[1], self.new_rotation[2]))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')
                if self.smooth_objects:
                    bpy.ops.object.shade_smooth()
                    print('Smoothing', item)
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')
                mat = bpy.data.materials.get("Material")
                #mat.diffuse_color = self.new_color
                
                if self.create_new_material:
                    mat = bpy.data.materials.new(name="Material")
                    print('Creating new material for', item)
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')
                    if obj.data.materials:
                        # assign to 1st material slot
                        obj.data.materials[0] = mat
                        
                    else:
                        # no slots
                        obj.data.materials.append(mat)
                        
                if self.change_color:
                    obj.active_material.diffuse_color = self.new_color
                    print('Changing %s color to R: %s G: %s B: %s' % (item, self.new_color[0], self.new_color[1], self.new_color[2]))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('  DONE')
                    print('\n')
                if self.random_color:
                    
                    
                    matLen = len(obj.data.materials)
                    
                    r = random.randint( self.red_start, self.red_end)
                    g = random.randint( self.green_start, self.green_end)
                    b = random.randint( self.blue_start, self.blue_end)
                    
                    #name material by hex value
    
                    #hexName = '%02x%02x%02x' % (r,g,b)
                    #mat.name = hexname
                    
                    mat.diffuse_color = (r/255, g/255, b/255)
                    
                    print('Changing %s color to R: %s G: %s B: %s' % (item, mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2]))
                    for i in range(21):
                        sys.stdout.write('\r')
                        # the exact output you're looking for:
                        sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
                        sys.stdout.flush()
                        sleep(0.25)
                    print('DONE')
                    print('\n')
                if self.change_emit:
                    obj.active_material.emit = self.new_emit
                if self.change_transparency:
                    if self.new_transparency == 'None':
                        obj.active_material.use_transparency = False
                    if self.new_transparency == 'Mask':
                        obj.active_material.use_transparency = True
                        obj.active_material.transparency_method = 'MASK'
                    if self.new_transparency == 'Z-Transparency':
                        obj.active_material.use_transparency = True
                        obj.active_material.transparency_method = 'Z_TRANSPARENCY'
                    if self.new_transparency == 'Raytrace':
                        obj.active_material.use_transparency = True
                        obj.active_material.transparency_method = 'RAYTRACE'
                if self.change_alpha:
                    obj.active_material.alpha = self.new_alpha
                if self.change_specular:
                    obj.active_material.specular_alpha = self.new_specular
                if self.change_fresnel:
                    obj.active_material.raytrace_transparency.fresnel = self.new_fresnel
                if self.change_material_type:
                    if self.new_material_type == 'Surface':
                        obj.active_material.type = 'SURFACE'
                    if self.new_material_type == 'Wire': 
                        obj.active_material.type = 'WIRE' 
                
                if self.duplicate_objects:
                    scene = bpy.context.scene
                    new_obj = obj.copy()
                    new_obj.data = obj.data.copy()
                    scene.objects.link(new_obj)
                
                if self.edit_mesh_vertices:
                    bpy.ops.object.mode_set(mode = 'EDIT', toggle = False)
                    bpy.ops.mesh.reveal()
                    bpy.ops.mesh.select_all(action = 'SELECT')
                    if self.dilate_erode_vertices:
                        bpy.ops.transform.shrink_fatten(value = self.dilate_erode_value, mirror=False)
                    if self.dilate_erode_copy_vertices:
                        if ".00" in obj.name:
                            bpy.ops.transform.shrink_fatten(value = self.dilate_erode_copy_value, mirror=False)
                    if self.flip_normals:
                        bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT', toggle = False)
                    
                if self.print_output:    
                    print('///////////////////////////////////////////////////////////// \n')
                    print("--- %s seconds ---" % (time.time() - start_time))
                    
        if self.select_all_objects:
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    obj.select = True
                
                
        return {'FINISHED'}
                
                    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Import objects:")
        box = layout.box()
        row = box.row(align = False)
        row = box.row(align = False)
        row.prop(self, "which_operating_system")
        row = box.row(align = False)
        row.prop(self, "which_import_method")
        row = box.row(align = False)
        row.prop(self, "path_to_data")
        row = box.row(align = False)
        row.prop(self, "clear_scene")
        row.prop(self, "decimate_objects")
        row.prop(self, "decimate_ratio")
        
        layout.label(text = "Edit objects:")
        box = layout.box()
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "change_origin")
        col = row.column()
        col.prop(self, "new_origin")
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
        row = box.row(align = False)
        row.prop(self, "smooth_objects")
        
        layout.label(text = "Materials:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "create_new_material")
        if self.create_new_material:
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_color")
            if self.change_color:
                col = row.column()
                col.prop(self, "new_color")
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
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_emit")
            col = row.column()
            col.prop(self, "new_emit")
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_transparency")
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
            row = box.row(align = False)
            col = row.column()
            col.prop(self, "change_material_type")
            col = row.column()
            col.prop(self, "new_material_type")
            
        layout.label(text = "Select objects:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "select_all_objects")
        row.prop(self, "duplicate_objects")
    
        layout.label(text = "Vertex edit:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "edit_mesh_vertices")
        if self.edit_mesh_vertices:
            row = box.row(align = False)
            row.prop(self, "dilate_erode_vertices")
            row.prop(self, "dilate_erode_value")
            row = box.row(align = False)
            row.prop(self, "dilate_erode_copy_vertices")
            row.prop(self, "dilate_erode_copy_value")
            row = box.row(align = False)
            row.prop(self, "flip_normals")
        
        layout.label(text = "Export objects:")
        box = layout.box()
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "print_output")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 800)
    
        
def register():
    bpy.utils.register_module(__name__)
    

def unregister():
    bpy.utils.unregister_module(__name__)
   
if __name__ == '__main__':
    register()