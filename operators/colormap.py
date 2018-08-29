import bpy
import bmesh
import os
import math
from math import pi, radians, degrees
import colorsys
import mathutils
import sys
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import FloatVectorProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

class ColorMap(Operator):
    bl_idname = "color.map"
    bl_label = "give objects a color map"
    bl_options = {'UNDO'}
    
    color_map = BoolProperty(name = "Color map", default = False, description = "Add color map to objects")
    
    object_type = EnumProperty(name = "Object type", items = [("Mesh", "Mesh", "Mesh"), ("Curve", "Curve", "Curve")], default = "Mesh", description = "Type of object to apply color map to")
    
    map_type = EnumProperty(name = "Map type", items = [("Vertex count", "Vertex count", "Vertex count"), ("Surface area", "Surface area", "Surface area")], default = "Vertex count", description = "Color map type to color objects by")
    
    hue_order = EnumProperty(name = "Order", items = [("Low to high", "Low to high", "Low to high"), ("High to low", "High to low", "High to low")], default = "Low to high", description = "Order of color mapping (red to violet/ violet to red")
    
    emit_order = EnumProperty(name = "Order", items = [("Low to high", "Low to high", "Low to high"), ("High to low", "High to low", "High to low")], default = "Low to high", description = "Order of emit mapping (0 to 5 / 5 to 0)")
    
    alpha_order = EnumProperty(name = "Order", items = [("Low to high", "Low to high", "Low to high"), ("High to low", "High to low", "High to low")], default = "Low to high", description = "Order of alpha mapping (0 to 1 / 1 to 0)")
    
    specular_order = EnumProperty(name = "Order", items = [("Low to high", "Low to high", "Low to high"), ("High to low", "High to low", "High to low")], default = "Low to high", description = "Order of specular mapping (0 to 1 / 1 to 0)")
    
    fresnel_order = EnumProperty(name = "Order", items = [("Low to high", "Low to high", "Low to high"), ("High to low", "High to low", "High to low")], default = "Low to high", description = "Order of fresnel mapping (0 to 5 / 5 to 0)")
    
    hue_map = BoolProperty(name = "Hue map", default = True, description = "Use a hue map (hsv values)")
    
    hue_start = FloatProperty(name = "Hue start", default = 0, min = 0, max = 1, description = "Start of hue range")
    
    hue_end = FloatProperty(name = "Hue end", default = .65, min = 0, max = 1, description = "End of hue range")
    
    emit_map = BoolProperty(name = "Emit map", default = False, description = "Use an emit map")
    
    emit_start = FloatProperty(name = "Emit start", default = .1, min = 0, max = 5, description = "Start of emit range")
    
    emit_end = FloatProperty(name = "Emit end", default = 2, min = 0, max = 5, description = "End of emit range")
    
    alpha_map = BoolProperty(name = "Alpha map", default = False, description = "Use an alpha map")
    
    alpha_start = FloatProperty(name = "Alpha start", default = .01, min = 0, max = 1, description = "Start of alpha range")
    
    alpha_end = FloatProperty(name = "Alpha end", default = 1, min = 0, max = 1, description = "End of alpha range")
    
    specular_map = BoolProperty(name = "Specular map", default = False, description = "Use a specular map")
    
    specular_start = FloatProperty(name = "Specular start", default = .01, min = 0, max = 1, description = "Start of specular range")
    
    specular_end = FloatProperty(name = "Specular end", default = 1, min = 0, max = 1, description = "End of specular range")
    
    fresnel_map = BoolProperty(name = "Fresnel map", default = False, description = "Use a fresnel map")
    
    fresnel_start = FloatProperty(name = "Fresnel start", default = 2, min = 0, max = 5, description = "Start of fresnel range")
    
    fresnel_end = FloatProperty(name = "Fresnel end", default = 5, min = 0, max = 5, description = "End of fresnel range")
    
    @classmethod
    def poll(cls, context):
        return context.object != []
    
    def check(self, context):
        return True
    
    def execute(self, context):
        
        hue_range = self.hue_end - self.hue_start
        emit_range = self.emit_end - self.emit_start
        alpha_range = self.alpha_end - self.alpha_start
        specular_range = self.specular_end - self.specular_start
        fresnel_range = self.fresnel_end - self.fresnel_start
        
        n_nodes = {}
        
        if self.color_map:
        
            for n in bpy.context.selected_objects:
                
                if self.object_type == 'Mesh':
                    if n.type != 'MESH':
                        continue
                    if self.map_type == 'Vertex count':
                        n_nodes[n] = len(n.data.vertices)
                    elif self.map_type == 'Surface area':
                        bm = bmesh.new()
                        bm.from_mesh(n.data)
                        n_nodes[n] = sum(f.calc_area() for f in bm.faces)
                
                if self.object_type == 'Curve':
                    if n.type != 'CURVE':
                        continue
                    n_splines = len(n.data.splines)
                    n_verts = sum([len(s.points) for s in n.data.splines])
                    n_nodes[n] = n_verts - n_splines + 1
                        
            max_n = max(n_nodes.values())
            min_n = min(n_nodes.values())
            
            corrected_hue_range = (max_n - min_n) * (1/hue_range)
            corrected_emit_range = (max_n - min_n) * (1/emit_range)
            corrected_alpha_range = (max_n - min_n) * (1/alpha_range)
            corrected_specular_range = (max_n - min_n) * (1/specular_range)
            corrected_fresnel_range = (max_n - min_n) * (1/fresnel_range)
                    
            if self.hue_order == 'Low to high':
                hmap = {n: colorsys.hsv_to_rgb(( self.hue_start + (v - min_n) / corrected_hue_range), 1, 1) for n, v in n_nodes.items()}
            elif self.hue_order == 'High to low':
                hmap = {n: colorsys.hsv_to_rgb(( self.hue_end - (v - min_n) / corrected_hue_range), 1, 1) for n, v in n_nodes.items()}
                
            if self.emit_order == 'Low to high':
                emap = {n: self.emit_start + ((v - min_n) / corrected_emit_range) for n, v in n_nodes.items()}
            elif self.emit_order == 'High to low':
                emap = {n: self.emit_end - ((v - min_n) / corrected_emit_range) for n, v in n_nodes.items()}
                
            if self.alpha_order == 'Low to high':
                amap = {n: self.alpha_start + ((v - min_n) / corrected_alpha_range) for n, v in n_nodes.items()}
            elif self.alpha_order == 'High to low':
                amap = {n: self.alpha_end - ((v - min_n) / corrected_alpha_range) for n, v in n_nodes.items()}
                
            if self.specular_order == 'Low to high':
                smap = {n: self.specular_start + ((v - min_n) / corrected_specular_range) for n, v in n_nodes.items()}
            elif self.specular_order == 'High to low':
                smap = {n: self.specular_end - ((v - min_n) / corrected_specular_range) for n, v in n_nodes.items()}
                
            if self.fresnel_order == 'Low to high':
                fmap = {n: self.fresnel_start + ((v - min_n) / corrected_fresnel_range) for n, v in n_nodes.items()}
            elif self.fresnel_order == 'High to low':
                fmap = {n: self.fresnel_end - ((v - min_n) / corrected_fresnel_range) for n, v in n_nodes.items()}
                
            if self.hue_map:
                for n in hmap:
                    n.active_material.diffuse_color = hmap[n]
            if self.emit_map:
                for n in emap:
                    n.active_material.emit = emap[n]
            if self.alpha_map:
                for n in amap:
                    n.active_material.use_transparency = True
                    n.active_material.alpha = amap[n]
            if not self.alpha_map:
                for n in amap:
                    n.active_material.use_transparency = False
            if self.specular_map:
                for n in smap:
                    n.active_material.use_transparency = True
                    n.active_material.specular_alpha = smap[n]
            if not self.specular_map:
                for n in smap:
                    n.active_material.use_transparency = False
            if self.fresnel_map:
                for n in fmap:
                    n.active_material.use_transparency = True
                    n.active_material.raytrace_transparency.fresnel = fmap[n]
            if not self.fresnel_map:
                for n in fmap:
                    n.active_material.use_transparency = False
                        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "Apply to:")
        box = layout.box()
        row = box.row(align = False)
        row.prop(self, "color_map")
        row.prop(self, "object_type")
        row.prop(self, "map_type")
        if self.color_map:
            #row.prop(self, "object_type")
            #row.prop(self, "map_type")
            row = box.row(align = False)
            row.prop(self, "hue_map")
            if self.hue_map:
                row.prop(self, "hue_order")
                row.prop(self, "hue_start")
                row.prop(self, "hue_end")
            row = box.row(align = False)
            row.prop(self, "emit_map")
            if self.emit_map:
                row.prop(self, "emit_order")
                row.prop(self, "emit_start")
                row.prop(self, "emit_end")
            row = box.row(align = False)
            row.prop(self, "alpha_map")
            if self.alpha_map:
                row.prop(self, "alpha_order")
                row.prop(self, "alpha_start")
                row.prop(self, "alpha_end")
            row = box.row(align = False)
            row.prop(self, "specular_map")
            if self.specular_map:
                row.prop(self, "specular_order")
                row.prop(self, "specular_start")
                row.prop(self, "specular_end")
            row = box.row(align = False)
            row.prop(self, "fresnel_map")
            if self.fresnel_map:
                row.prop(self, "fresnel_order")
                row.prop(self, "fresnel_start")
                row.prop(self, "fresnel_end")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 1000)