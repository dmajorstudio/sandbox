###############################################
# Root snapper
# 
# @author: David Major
# @created: ~2014


import maya.cmds as cmds

def snap_root_CV_to_mesh(*args):
    '''
    Snap root CV of curve to closest point on mesh for selected mesh
    and curves which are currently selected.
    '''
    initialSelection = cmds.ls(sl=True)
    scalpMesh = cmds.ls(sl=True, dag=True, type='mesh')[0]
    curveSet = cmds.listRelatives(cmds.ls(sl=True, dag=True, type='nurbsCurve'), parent=True)

    CPOM_A = cmds.createNode('closestPointOnMesh')
    CPOM_B = cmds.createNode('closestPointOnMesh')
    cmds.connectAttr(scalpMesh+'.outMesh', CPOM_A+'.inMesh')
    cmds.connectAttr(scalpMesh+'.outMesh', CPOM_B+'.inMesh')

    for CRV in curveSet:
        #CRV = curveSet[0]
        curveLen = int(cmds.arclen(CRV)/3+4)
        rebuildCRV = cmds.rebuildCurve(CRV, d=3, spans=curveLen)
        
        #print CRV
        CRVroot = cmds.pointPosition(CRV+'.cv[0]', world=True)
        CRVvec = cmds.pointPosition(CRV+'.cv[2]', world=True)
        
        abc = ['X', 'Y', 'Z']
        for x in abc:
            cmds.setAttr(CPOM_A+'.inPosition'+x, CRVroot[abc.index(x)])
            cmds.setAttr(CPOM_B+'.inPosition'+x, CRVvec[abc.index(x)])

        CPOM_rootPOS = cmds.getAttr(CPOM_A+'.position')[0]
        CPOM_vecPOS = cmds.getAttr(CPOM_B+'.position')[0]
        #print CRV, CRVroot, CPOM_POS
        
        
        cmds.reverseCurve(CRV)
        CRVcvs = cmds.getAttr(CRV+'.spans')
        #print CRV, curveLen, CRVcvs, rebuildCRV
        cmds.delete(CRV, constructionHistory=True)
        CRVshape = cmds.listRelatives(CRV, children=True)
        cmds.curve(CRVshape, a=True, ws=True, p=[CPOM_vecPOS, CPOM_rootPOS])#[(0,0,0) for x in range(CRVcvs/5)])
        cmds.reverseCurve(CRV)
        cmds.rebuildCurve(CRV, degree=3, spans=CRVcvs+2)
        cmds.smoothCurve(CRV+'.cv[*]', smoothness=10)
    #break

    cmds.select(initialSelection)


snap_root_CV_to_mesh()
