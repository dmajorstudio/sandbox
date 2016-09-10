# =============================================================================
#             Assign random colors to faces on an object
# =============================================================================
# Quick little example of how to assign a randomized color to each face of an
#     object.
# Easily expandable exercise.
#     - Apply color to selected face
#     - Apply random color to selected face
#     - Apply random color to all faces of selected object
#     - Apply random color for unique ID of all selected objects
#     - Write up a 2-button UI which 
#         - assigns random colors to selected objects
#         - removes colors from selected objects

# Basic Command
# =============================================================================
# import maya.cmds as cmds
# cmds.polyColorPerVertex(colorRGB=[0.8,0.2,0.2], colorDisplayOption=True)

# =============================================================================

import maya.cmds as cmds
import random

myObj = cmds.ls(sl=True)[0]

faceCount = cmds.getAttr(myObj+'.face', size=1)
for face in range(faceCount):
    # cmds.currentTime(face)
    cmds.select(myObj+'.f[%d]' % face)
    myColor = [float(random.random()), float(random.random()), float(random.random())]
    cmds.polyColorPerVertex(colorRGB=myColor, colorDisplayOption=True)

cmds.select(myObj)

# Removing the colors
# =============================================================================

myObjShapes = cmds.ls(sl=True, dag=True, type='mesh')

for myShape in myObjShapes:
    cmds.setAttr(myShape+'.displayColors', 0)