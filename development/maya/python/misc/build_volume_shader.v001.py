import maya.mel as mel
import maya.cmds as cmds

def loadMentalRay():
    if not cmds.pluginInfo('Mayatomr', query=True, loaded=True):
        print 'mental ray is unloaded'
        cmds.loadPlugin('Mayatomr')
        mel.eval('mentalrayUI add')
        mel.eval('updateRendererUI')
        mel.eval('mentalrayAddTabs')
    else: print 'mental ray is already loaded'

def build_volume_shader():
    '''
    Build volume shader with selected lights and bounding box geometry.
    '''
    loadMentalRay() # Only works with mental ray nodes present in scene

    selLightList = []
    selGeoList = []
    for x in cmds.ls(selection=True, dag=True):
        print 'processing: ', x, cmds.objectType(x)
        if cmds.objectType(x).startswith('mesh'):
            selGeoList.append(x)
        if cmds.objectType(x).endswith('Light'):
            selLightList.append(x)

    volumeMAT = cmds.shadingNode('lambert', asShader=True, name='volume_MAT')
    volumeSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='%s_SG'%volumeMAT.split('_')[0])
    volumeTMAT = cmds.shadingNode('transmat', asShader=True, name='volume_TMAT')
    volumeParti = cmds.shadingNode('parti_volume', asShader=True, name='partiVolume_MAT')

    cmds.connectAttr(volumeMAT+'.outColor', volumeSG+'.surfaceShader', force=True)
    cmds.connectAttr(volumeTMAT+'.outValue', volumeSG+'.miMaterialShader', force=True)
    cmds.connectAttr(volumeTMAT+'.outValue', volumeSG+'.miShadowShader', force=True)
    cmds.connectAttr(volumeParti+'.outValue', volumeSG+'.miVolumeShader', force=True)

    cmds.setAttr(volumeParti+'.scatter', 1,1,1)

    for light in selLightList:
        lightTransform = cmds.listRelatives(light, parent=True)[0]
        cmds.connectAttr(lightTransform+'.message', '%s.lights[%d]'%(volumeParti, selLightList.index(light)))
        cmds.setAttr(light+'.useRayTraceShadows', 1)
        cmds.setAttr(light+'.lightRadius', 0.2)
        cmds.setAttr(light+'.shadowRays', 5)
        cmds.setAttr(light+'.rayDepthLimit', 5)

    for geo in selGeoList:
        cmds.sets(geo, edit=True, forceElement=volumeSG)
        cmds.setAttr(geo+'.opposite', 1)

    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', 'string')
    mel.eval('rendererChanged')
    cmds.setAttr('miDefaultOptions.maxRayDepth', 10)
    cmds.setAttr('miDefaultOptions.maxShadowRayDepth', 10)
    cmds.setAttr('miDefaultOptions.autoVolume', 1)
    cmds.setAttr('miDefaultOptions.volumeShaders', 1)
    cmds.setAttr('miDefaultOptions.volumeSamples', 10)


build_volume_shader()


