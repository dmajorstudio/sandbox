'''
FX Utility - Select Random from Selection

Created: April 25, 2014

Company: Mikros Image - MUNE
@author: David Major
'''
import maya.cmds as cmds
import random

def DMselectRandomFromSelection(baseSelection = cmds.ls(selection=True), *args):
    ######## For component/dag determination ########
    #  >>> ! This is pointless, though academically interesting.
    #  >>> Instead use: cmds.ls(selection=True, flatten=True)

    # componentSelectionSet = []
    # dagSelectionSet = []
    # for obj in baseSelection:
    #     if obj.endswith(']'):
    #         mesh, arg, extension = obj.partition('.')
    #         componentType = extension.partition('[')[0]
    #         typeIndex = extension[len(componentType)+1:len(extension)-1]
            
    #         if typeIndex.find(':') != -1:
    #             for x in range(int(typeIndex.partition(':')[0]), int(typeIndex.partition(':')[2])+1):
    #                 componentSelectionSet.append('%s.%s[%s]' % (mesh, componentType, x))
    #         else:
    #             componentSelectionSet.append(obj)
    #     else:
    #         dagSelectionSet.append(obj)

    # data = []
    # if len(componentSelectionSet) > 0:
    #     for component in componentSelectionSet:
    #         data.append(component)

    # if len(dagSelectionSet) > 0:
    #     for object in dagSelectionSet:
    #         data.append(object)
    
    data = cmds.ls(sl=True, fl=True)

    selectionList = []
    dataSize = len(data)

    cmds.promptDialog(title='Select random in Selection', 
                message='Of %r, how many items would you like to select?' % dataSize)
    try:
        numSel = int(cmds.promptDialog(query=True, text=True))
    except (ValueError), errorMessage:
        cmds.warning('Cancelled: Please specify a value for selection.')
        return

    dataIter = dataSize
    for x in range(numSel):
        if data != [] and numSel < dataSize:
            dataIter -= 1
            index = random.randrange(dataIter)
            item = data[index]
            data[index] = data[dataIter]
            data.pop()
            selectionList.append(item)
        else:
            pass

    if len(selectionList) > 0:
        cmds.select(selectionList)
        cmds.warning( 'You have selected %d items' % len(selectionList) )
    else:
        cmds.warning( 'You have not reduced your selection' )

    #cmds.ConvertSelectionToShell() #selects full geometry for component selection

DMselectRandomFromSelection()