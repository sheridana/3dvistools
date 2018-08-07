from . import batchimport, newwindow, viewmode
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
        row.operator("batch.import", text = "Batch import objects", icon = 'IMPORT')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("new.window", text = "New window", icon = 'SPLITSCREEN')

        row = layout.row(align = True)
        row.alignment = 'EXPAND'
        row.operator("view.mode", text = "View mode", icon = 'RESTRICT_VIEW_OFF')

def register():
    bpy.utils.register_module(__name__)
    

def unregister():
    bpy.utils.unregister_module(__name__)
   
if __name__ == '__main__':
    register()