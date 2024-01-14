"""

This script contains the workflow for color coding a composite object given from an svg file
"""
from functions import *
import numpy as np


# Some example values normalised between 0 and 1
coefficients_A_X = [0.2374902,  0.36011206, 0.29299398, 0.9227212,  0.04891635, 1,
 0.57012938, 0.05536324, 0.0387932,  0.80208422, 0.53494057, 0.36618771,
 0,        0.15518429, 0.02364835, 0.0135818,  0.14016616, 0.05028362,
 0.0333129 ]

# Name of body parts that match corresponding shape names on svg gile
bodyParts = ['Pelvis', 'Ab', 'Chest', 'Neck', 'Head', 'LShoulder', 'LUArm', 
                      'LFArm', 'LHand', 'RShoulder', 'RUArm', 'RFArm', 'RHand',  'LThigh', 'LShin', 
                      'LFoot', 'RThigh', 'RShin', 'RFoot']


# Define some colours
light_blue = (173, 216, 230)  # Light blue 
dark_blue = (0, 0, 139)       # Dark blue

white =  (255, 255, 255) # White
dark_red = (255, 0, 0) # Red



# Set location and import body parts ( list of names of bodies that coefficients correspond to)
location = 'body.svg'

# Extract shape data from the svg file
elements,points,pathElements,partMapping = extractShapesFromSVG(location=location,parts=bodyParts)

# Set colours for each coefficient
colours = [get_color_hex(i,white,dark_blue) for i in coefficients_A_X]


# Draw the object 
drawObject(points,elements,colours,partMapping)
