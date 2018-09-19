from . operators import *
import bpy, blf
import bmesh
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

class importPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = '3D visualization tools'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("batch.import", text = "Batch import", icon = 'IMPORT')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("new.window", text = "New window", icon = 'SPLITSCREEN')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("view.mode", text = "View mode", icon = 'RESTRICT_VIEW_OFF')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("world.background", text = "World background", icon = 'WORLD')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("neuron.modifiers", text = "Modifiers", icon = 'MODIFIER')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("jump.fix", text = "Jump fix", icon = "IPO_ELASTIC")

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("bounding.box", text = "Bounding box", icon = "BBOX")

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("neuron_scale_rotation.location", text = "Object manipulation", icon = 'OUTLINER_OB_GROUP_INSTANCE')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("change.materials", text = "Materials", icon = 'MATERIAL')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("color.map", text = "Color map", icon = 'COLOR')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("edit.objects", text = "Edit objects", icon = 'EDIT')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("batch.export", text = "Batch export", icon = 'EXPORT')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("peel.away", text = "Peel away", icon = "MESH_PLANE")

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("simple.animation", text = "Simple animation", icon = 'RENDER_ANIMATION')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("test.plugin", text = "Automate", icon = "PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    

def unregister():
    bpy.utils.unregister_module(__name__)
   
if __name__ == '__main__':
    register()