import bpy, blf
import os
import re
import random
import time
import datetime
import json
import math
from math import pi, radians, degrees
import colorsys
import mathutils
import sys
import numpy as np
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class simpleAnimation(Operator):
    bl_idname = "simple.animation"
    bl_label = "simple animation"
    bl_options = {'UNDO'}
    
    #select objects
    
    which_objects = EnumProperty( name = "Which Objects?", items = [('Selected','Selected','Selected'), ('All','All','All'), ('By name' , 'By name', 'By name')],  default = 'Selected', description = "Edit object properties")
    
    by_name = StringProperty( name = "Object name(s)", description = "Search by object names. Separate multiple names with commas")
    
    partial_match = BoolProperty( name = "Allow partial matches?", default = False, description = "Allow partial matches for object names?")
    
    is_not = BoolProperty( name = "Is not named?", default = False, description = "Edit objects not named?")
    
    #add animations
    add_object_animation = BoolProperty(name = "Add object animation", default = False, description = "Add animation to objects")
    
    object_animation_type = EnumProperty(name = "Type", items = [('Fade (material)', 'Fade (material)', 'Fade (material)'), ('Fade (visibility)', 'Fade (visibility)', 'Fade (visibility)'), ('Expand', 'Expand', 'Expand')], default = 'Fade (visibility)', description = "Give objects a basic animation")
    
    add_camera_animation = BoolProperty(name = "Add camera animation", default = False, description = "Add animation to camera?")
    
    camera_animation_type = EnumProperty(name = "Type", items = [('Zoom', 'Zoom', 'Zoom'), ('Move', 'Move', 'Move')], default = 'Zoom', description = "Give active camera a basic animation")
    
    add_empty_animation = BoolProperty(name = "Add empty animation", default = False, description = "Give empty a basic animation")
    
    start_frame = FloatProperty(name = "Start frame", default = 0, max = 100000, min = 0, description = "Start frame of animation/video")
    
    end_frame = FloatProperty(name = "End frame", default = 0, max = 100000, min = 0, description = "End frame of animation/video")
    
    hold_frame = BoolProperty(name = "Hold?", default = False, description = "Hold objects after faded in before fade out?")
    
    fade_out = BoolProperty(name = "Fade out?", default = False, description = "Fade objects out after faded in?")
    
    fade_in_value = FloatProperty(name = "Fade in", default = 0, max = 100000, min = 0, description = "Number of frames to fade in")
    
    fade_out_value = FloatProperty(name = "Fade out", default = 0, max = 100000, min = 0, description = "Number of frames to fade out")
    
    hold_frame_value = FloatProperty(name = "Hold frame", default = 24, max = 100000, min = 0, description = "Number of frames to hold")
    
    render_image = BoolProperty(name = "Render image", default = False, description = "Render image")
    
    render_video = BoolProperty(name = "Render video", default = False, description = "Render video")
    
    first_alpha_value = FloatProperty(name = "1st alpha", default = 1, max = 1, min = 0, description = "Starting alpha value to be keyframed")
    
    second_alpha_value = FloatProperty(name = "2nd alpha", default = 1, max = 1, min = 0, description = "2nd alpha value to be keyframed")
    
    third_alpha_value =  FloatProperty(name = "3rd alpha", default = 1, max = 1, min = 0, description = "3rd alpha value to be keyframed")
    
    fourth_alpha_value = FloatProperty(name = "4th alpha", default = 1, max = 1, min = 0, description = "4th alpha value to be keyframed")
    
    first_specular_value = FloatProperty(name = "1st specular", default = 1, max = 1, min = 0, description = "Starting specular value to be keyframed")
    
    second_specular_value = FloatProperty(name = "2nd specular", default = 1, max = 1, min = 0, description = "2nd specular value to be keyframed")
    
    third_specular_value =  FloatProperty(name = "3rd specular", default = 1, max = 1, min = 0, description = "3rd specular value to be keyframed")
    
    fourth_specular_value = FloatProperty(name = "4th specular", default = 1, max = 1, min = 0, description = "4th specular value to be keyframed")
    
    first_fresnel_value = FloatProperty(name = "1st fresnel", default = 0, max = 5, min = 0, description = "Starting fresnel value to be keyframed")
    
    second_fresnel_value = FloatProperty(name = "2nd fresnel", default = 0, max = 5, min = 0, description = "2nd fresnel value to be keyframed")
    
    third_fresnel_value =  FloatProperty(name = "3rd fresnel", default = 0, max = 5, min = 0, description = "3rd fresnel value to be keyframed")
    
    fourth_fresnel_value = FloatProperty(name = "4th fresnel", default = 0, max = 5, min = 0, description = "4th fresnel value to be keyframed")
    
    hide_visibility = BoolProperty(name = "Hide visibility", default = False, description = "Restrict viewport visibility")
    
    hide_render = BoolProperty(name = "Hide render", default = False, description = "Restrict rendering")
    
    calculate_length = BoolProperty(name = "Calculate frames", default = False, description = "Calculate end frame based on start frame, # of objects, fade in/out frame count, hold frame count")
    
    expand_scale = FloatVectorProperty(name = "Expand scale", default = (0, 0, 0), min = -100000, max = 100000, subtype = 'XYZ', description = "Set expand scale (origin should be set to geometry or center of mass for all objects prior to this)")
    
    start_focal_length = FloatProperty(name =  "Start focal length", default = 35, max = 100000, min = -100000, description = "Change starting camera focal length")
    
    end_focal_length = FloatProperty(name = "End focal length", default = 35, max = 100000, min = -100000, description = "Change ending camera focal length")
    
    start_camera_location = FloatVectorProperty(name = "Start camera location", default = (0, 0, 0), max = 100000, min = -100000, subtype = 'XYZ', description = "change starting camera location")
    
    end_camera_location = FloatVectorProperty(name = "End camera location", default = (0, 0, 0), max = 100000, min = -100000, subtype = 'XYZ', description = "change ending camera location")
    
    start_camera_rotation = FloatVectorProperty(name = "Start camera rotation", default = (0, 0, 0), max = 100000, min = -100000, subtype = 'XYZ', description = "change starting camera rotation")
    
    end_camera_rotation = FloatVectorProperty(name = "End camera rotation", default = (0, 0, 0), max = 100000, min = -100000, subtype = 'XYZ', description = "change ending camera rotation")
    

    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        if self.which_objects == 'Selected':
            ob_list = bpy.context.selected_objects
        elif self.which_objects == 'All':
            ob_list = [ob for ob in bpy.data.objects if ob.type == 'MESH']
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
                        
        
        if self.add_object_animation:
            interval = round( (self.end_frame - self.start_frame)/ len(ob_list) )
            for i in range( len(ob_list) ):
                if self.object_animation_type == 'Fade (material)':
                    material = ob_list[i].active_material
                    material.use_transparency = True
                    
                    #first keyframes
                    material.alpha = self.first_alpha_value
                    material.specular_alpha = self.first_specular_value
                    material.raytrace_transparency.fresnel = self.first_fresnel_value
                    material.keyframe_insert( data_path = 'alpha', frame = self.start_frame + (i *interval) )
                    material.keyframe_insert( data_path = 'specular_alpha', frame = self.start_frame + (i *interval) )
                    material.keyframe_insert( data_path = 'raytrace_transparency.fresnel', frame = self.start_frame + (i *interval) )
                    
                    material.alpha = self.second_alpha_value
                    material.specular_alpha = self.second_specular_value
                    material.raytrace_transparency.fresnel = self.second_fresnel_value
                    material.keyframe_insert( data_path = 'alpha', frame = self.start_frame + (i *interval) + self.fade_in_value)
                    material.keyframe_insert( data_path = 'specular_alpha', frame = self.start_frame + (i *interval) + self.fade_in_value)
                    material.keyframe_insert( data_path = 'raytrace_transparency.fresnel', frame = self.start_frame + (i *interval) + self.fade_in_value)
                    
                    material.alpha = self.third_alpha_value
                    material.specular_alpha = self.third_specular_value
                    material.raytrace_transparency.fresnel = self.third_fresnel_value
                    material.keyframe_insert( data_path = 'alpha', frame = self.start_frame + (i *interval) + self.fade_in_value  + self.hold_frame_value)
                    material.keyframe_insert( data_path = 'specular_alpha', frame = self.start_frame + (i *interval) + self.fade_in_value + self.hold_frame_value)
                    material.keyframe_insert( data_path = 'raytrace_transparency.fresnel', frame = self.start_frame + (i *interval) + self.fade_in_value + self.hold_frame_value)
                    
                    material.alpha = self.fourth_alpha_value
                    material.specular_alpha = self.fourth_specular_value
                    material.raytrace_transparency.fresnel = self.fourth_fresnel_value
                    material.keyframe_insert( data_path = 'alpha', frame = self.start_frame + (i *interval) + self.fade_in_value  + self.hold_frame_value + self.fade_out_value)
                    material.keyframe_insert( data_path = 'specular_alpha', frame = self.start_frame + (i *interval) + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
                    material.keyframe_insert( data_path = 'raytrace_transparency.fresnel', frame = self.start_frame + (i *interval) + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
                
                if self.object_animation_type == 'Fade (visibility)':
                    if self.hide_visibility:
                        ob_list[i].hide = True
                        ob_list[i].keyframe_insert( data_path = 'hide', frame = self.start_frame + (i * interval) )
                        ob_list[i].hide = False
                        ob_list[i].keyframe_insert( data_path = 'hide', frame = self.start_frame + (i * interval) + self.fade_in_value)
                        
                        if self.hold_frame:
                            ob_list[i].hide = False
                            ob_list[i].keyframe_insert( data_path = 'hide', frame = self.start_frame + (i * interval) + self.fade_in_value + self.hold_frame_value)
                        
                        if self.fade_out:
                            ob_list[i].hide = True
                            ob_list[i].keyframe_insert( data_path = 'hide', frame = self.start_frame + (i * interval) + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
                            
                    
                    if self.hide_render:
                        ob_list[i].hide_render = True
                        ob_list[i].keyframe_insert( data_path = 'hide_render', frame = self.start_frame + (i * interval) )
                        ob_list[i].hide_render = False
                        ob_list[i].keyframe_insert( data_path = 'hide_render', frame = self.start_frame + (i * interval) + self.fade_in_value)
                        
                        if self.hold_frame:
                            ob_list[i].hide_render = False
                            ob_list[i].keyframe_insert( data_path = 'hide_render', frame = self.start_frame + (i * interval) + self.fade_in_value + self.hold_frame_value)
                        
                        if self.fade_out:
                            ob_list[i].hide_render = True
                            ob_list[i].keyframe_insert( data_path = 'hide_render', frame = self.start_frame + (i * interval) + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
              
        return {'FINISHED'}
    
    def draw(self, context):
        if self.which_objects == 'Selected':
            ob_list = bpy.context.selected_objects
        elif self.which_objects == 'All':
            ob_list = [ob for ob in bpy.data.objects if ob.type == 'MESH']
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
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "add_object_animation")
        if self.add_object_animation:
            row.prop(self, "object_animation_type")
            row.prop(self, "calculate_length")
            split = box.split()
            col = split.column()
            col.prop(self, "start_frame")
            col.prop(self, "end_frame")
            if self.object_animation_type == 'Fade (material)': 
                col.separator()
                col = split.column()
                col.prop(self, "fade_in_value")
                col.prop(self, "fade_out_value")
                col = split.column()
                col.prop(self, "hold_frame_value")   
                if self.calculate_length:
                    self.end_frame = len(ob_list) * (self.start_frame + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
                split = box.split()
                col = split.column()
                col.prop(self, "first_alpha_value")
                col.prop(self, "first_specular_value")
                col.prop(self, "first_fresnel_value")
                col = split.column()
                col.prop(self, "second_alpha_value")
                col.prop(self, "second_specular_value")
                col.prop(self, "second_fresnel_value")
                col = split.column()
                col.prop(self, "third_alpha_value")
                col.prop(self, "third_specular_value")
                col.prop(self, "third_fresnel_value")
                col = split.column()
                col.prop(self, "fourth_alpha_value")
                col.prop(self, "fourth_specular_value")
                col.prop(self, "fourth_fresnel_value")
            if self.object_animation_type == 'Fade (visibility)':
                col.separator()
                col = split.column()
                col.prop(self, "fade_in_value")
                row = col.row()
                row.prop(self, "fade_out")
                if self.fade_out:
                    row.prop(self, "fade_out_value")
                col = split.column()
                row = col.row()
                row.prop(self, "hold_frame")
                if self.hold_frame:
                    row.prop(self, "hold_frame_value")   
                row = box.row()
                row.prop(self, "hide_visibility")
                row.prop(self, "hide_render")
                if self.calculate_length:
                    if self.hold_frame and not self.fade_out:
                        self.end_frame = len(ob_list) * (self.start_frame + self.fade_in_value + self.hold_frame_value)
                    elif self.fade_out and not self.hold_frame:
                        self.end_frame = len(ob_list) * (self.start_frame + self.fade_in_value + self.fade_out_value)
                    elif self.hold_frame and self.fade_out:
                        self.end_frame = len(ob_list) * (self.start_frame + self.fade_in_value + self.hold_frame_value + self.fade_out_value)
                    else:
                        self.end_frame = len(ob_list) * (self.start_frame + self.fade_in_value)
                        
                        
                    
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "add_camera_animation")
        if self.add_camera_animation:
            row.prop(self, "camera_animation_type")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "add_empty_animation")
        
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "render_image")
        row = box.row(align = False)
        row.prop(self, "render_video")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1200)