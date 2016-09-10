# ===============================================================================
# I saw a script on creative crash a few months ago.
# Decided to write my script to do something similar as an academic study.

# Suggested usage:
#     - For any animated object, you can select points (mesh vertexes)
#     - This script will run through your timeline and cache all the point 
#         positions per frame on the timeline. once it's done collecting
#         points, it will generate a curve per point you had selected.
# Kind of useful for generating interesting curves/paths for use in FX/CFX
# Shortcoming: Might not work on geometry that has namespaces.

import maya.cmds as cmds

def DM_plotCurve(DM_sel = None):
    if not DM_sel:
        DM_sel = cmds.ls(sl=True)
    DM_reviseSel = []

    for DM_item in DM_sel:
        if DM_item.find(':') != -1: # prevents namespaces from working.
            DM_range = DM_item.rpartition('[')[2].rstrip(']')
            DM_first, DM_last = int(DM_range.split(':')[0]), int(DM_range.split(':')[1])
            DM_iterPoint = DM_first
            DM_preamble = DM_item.rpartition('[')[0]

            while DM_iterPoint <= DM_last:
                DM_entry = '%s[%d]' % (DM_preamble, DM_iterPoint)
                DM_reviseSel.append(str(DM_entry))
                DM_iterPoint += 1
        else:
            DM_reviseSel.append(str(DM_item))

    DM_pointDict = {}

    minTimeRange = int(cmds.playbackOptions(query=True, minTime=True))
    maxTimeRange = int(cmds.playbackOptions(query=True, maxTime=True))

    for DM_point in DM_reviseSel:
        DM_pointDict[DM_point] = []

    for time in range(minTimeRange, (maxTimeRange+1)):
        cmds.currentTime(time)
        for DM_point in DM_reviseSel:
            DM_pointPOS = cmds.pointPosition(DM_point, world=True)
            DM_pointDict[DM_point].append(DM_pointPOS)

    DM_resultCRVs = []
    for DM_key in DM_pointDict.keys():
        DM_pointList = DM_pointDict[DM_key]
        DM_pointCRV = cmds.curve(degree=3, point=DM_pointList)
        DM_resultCRVs.append(DM_pointCRV)

    return DM_resultCRVs

# DM_plotCurve()