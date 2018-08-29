import bpy
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class viewMode(Operator):
    bl_idname = "view.mode"
    bl_label = "view mode"
    bl_options = {'UNDO'}

    
    interaction_mode = BoolProperty( name = "Object interaction mode", default = False, description = "Change the object interaction mode?")
    
    new_interaction_mode = EnumProperty( name = "", items = [('Object', 'Object', '', 'OBJECT_DATA', 0), ('Edit', 'Edit', '', 'EDITMODE_HLT', 1)], default = 'Object', description = "Set mode")
    
    display_method = BoolProperty( name = "Display method", default = False, description = "Change the display method?")
    
    new_display_method = EnumProperty( name = "", items = [('Solid', 'Solid', '', 'SOLID', 0), ('Material', 'Material', '', 'MATERIAL', 1), ('Rendered', 'Rendered', '', 'SMOOTH', 2), ('Textured', 'Textured', '', 'POTATO', 3), ('Wireframe', 'Wireframe', '', 'WIRE', 4), ('Bounding box', 'Bounding box', '', 'BBOX', 5)], default = 'Solid', description = "Set display method")
    
    change_view = BoolProperty( name = "Change view", default = False, description = "Change angle of view")
    
    view_mode = BoolProperty( name = "Switch persp/ortho", default = False, description = "Perspective camera")
    
    which_view = EnumProperty( name = "View", items = [('Camera', 'Camera', 'Camera'), ('Left', 'Left', 'Left'), ('Right', 'Right', 'Right'), ('Top', 'Top', 'Top'), ('Bottom', 'Bottom', 'Bottom'), ('Front', 'Front', 'Front'), ('Back', 'Back', 'Back')], default = 'Front', description = "Change view")
    
    quad_view = BoolProperty( name = "Toggle quad view", default = False, description = "Toggle quad view?")
    
    lock_view = BoolProperty( name = "Lock", default = False, description = "Lock view?")
    
    box_view = BoolProperty( name = "Box", default = False, description = "Box view?")
    
    clip_view = BoolProperty( name = "Clip", default = False, description = "Clip view?")
    
    '''maximize_3dview = BoolProperty( name = "Maximize view", default = False, description = "Maximize 3dview?")'''
    
    

    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
            
        if self.interaction_mode:
            if self.new_interaction_mode == 'Object':
                bpy.ops.object.mode_set(mode='OBJECT')
            if self.new_interaction_mode == 'Edit':
                bpy.ops.object.mode_set(mode='EDIT')
        
        if self.display_method:
            for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                if self.new_display_method == 'Solid':
                                    space.viewport_shade = 'SOLID'
                                if self.new_display_method == 'Material':
                                    space.viewport_shade = 'MATERIAL'
                                if self.new_display_method == 'Rendered':
                                    space.viewport_shade = 'RENDERED'
                                if self.new_display_method == 'Textured':
                                    space.viewport_shade = 'TEXTURED'
                                if self.new_display_method == 'Wireframe':
                                    space.viewport_shade = 'WIREFRAME'
                                if self.new_display_method == 'Bounding box':
                                    space.viewport_shade = 'BOUNDBOX'
                                    
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                break

        for region in area.regions:
            if region.type == "WINDOW":
                break

        space = area.spaces[0]

        context = bpy.context.copy()
        context['area'] = area
        context['region'] = region
        context['space_data'] = space

        if self.view_mode:
            bpy.ops.view3d.view_persportho(context, 'EXEC_DEFAULT')
        
        if self.change_view:
            if self.which_view == 'Camera':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='CAMERA')
            if self.which_view == 'Left':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='LEFT')
            if self.which_view == 'Right':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='RIGHT')
            if self.which_view == 'Top':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='TOP')
            if self.which_view == 'Bottom':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='BOTTOM')
            if self.which_view == 'Front':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='FRONT')
            if self.which_view == 'Back':
                bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type='BACK')
                
        if self.quad_view:
            bpy.ops.screen.region_quadview(context, 'EXEC_DEFAULT')
        if self.lock_view:
            space.region_3d.lock_rotation = True
        else:
            space.region_3d.lock_rotation = False
        if self.box_view:
            space.region_3d.show_sync_view = True
        else:
            space.region_3d.show_sync_view = False
        if self.clip_view:
            space.region_3d.use_box_clip = True
        else:
            space.region_3d.use_box_clip = False
        
        #this causes blender to crash for some reason        
        '''if self.maximize_3dview:
            bpy.ops.screen.screen_full_area(context, 'EXEC_DEFAULT')'''
            
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Change:")
        box = layout.box()
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "interaction_mode")
        col = row.column()
        col.prop(self, "new_interaction_mode")
        
        row = box.row(align = False)
        col = row.column()
        col.prop(self, "display_method")
        col = row.column()
        col.prop(self, "new_display_method")
        
        row = box.row(align = False)
        row.prop(self, "view_mode")
        row.prop(self, "change_view")
        if self.change_view:
            row.prop(self, "which_view")
        
        row = box.row(align = False)
        row.prop(self, "quad_view")
        row.prop(self, "lock_view")
        row.prop(self, "box_view")
        row.prop(self, "clip_view")
            
        '''row = box.row(align = False)
        row.prop(self, "maximize_3dview")'''
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)