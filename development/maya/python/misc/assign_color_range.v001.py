
# =============================================================================
#             Assign colorRange shaders to objects.
# =============================================================================
# Not going to spend much time on this one, but wanted to include it
# Randomizes colors based off a colorRange.

import maya.cmds as cmds
import colorsys

def DM_assignNewShader(DM_sel, shaderName='IDShader', *args):
    DM_tempShader = cmds.shadingNode('lambert', asShader=True, n=shaderName)
    DM_tempSet = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=DM_tempShader+'SG')
    cmds.connectAttr(DM_tempShader+'.outColor', DM_tempSet+'.surfaceShader', force=True)
    cmds.select(DM_sel)
    cmds.sets(edit=True, forceElement=DM_tempSet)
    return DM_tempShader

def DM_randomizeColor(DM_sel = cmds.ls(sl=True), *args):
    DM_itr = 1.000/len(DM_sel)
    DM_iterColor = 0.000

    for obj in DM_sel:
        DM_outColor = colorsys.hsv_to_rgb(DM_iterColor, 0.7, 1.0)
        DM_iterColor += DM_itr

        DM_tempShader = DM_assignNewShader(obj)
        cmds.setAttr(DM_tempShader+'.color', DM_outColor[0], DM_outColor[1], DM_outColor[2])

