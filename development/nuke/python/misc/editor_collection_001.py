'''
Garbage collector for code snippitts I have not taken the time to add to a module.

Created: Aug 23, 2014

Company: Mikros Image - MUNE // TLP
@author: David Major
'''

********************************************************************************
********************************************************************************
>> # For climbing the node graph and copying all source images in read nodes
>> # to specified folders.
********************************************************************************
import nuke, re, shutil, glob, os

def globCopy(fileName, targetPath):
    globFile = fileName.split('%')[0] + '*'
    for item in glob.glob(globFile):
        shutil.copy(item, targetPath)

existingFileName = nuke.Root().name().split('/')[-1]
searchTerm = re.compile('sc\d*-sh\d*')
shotNumber = searchTerm.findall(existingFileName)[0]

#shotNumber = 'sc1410-sh01290'
#shotNumber = 'sc0000-sh99999'

currentPath = nuke.Root().name().rpartition('/')[0]
publishPath = currentPath
directoryContents = os.listdir(currentPath)
for obj in directoryContents:
    if obj.endswith('.ma'): continue
    if obj.startswith('mune_sh_%s_fx'%shotNumber):
        print obj
        publishPath = currentPath+'/'+obj

a = nuke.selectedNode()
nodesToSelect = []
#print a.dependencies() 
def climb(node):
    for n in node.dependencies():
        nodesToSelect.append(n)
        climb(n)
climb(a)
for x in nodesToSelect:
    x.setSelected(1)
readNodes = nuke.selectedNodes('Read')
for x in nuke.selectedNodes():
    x.setSelected(0)

for i in readNodes:
    fileName = i.knob('file').getValue()
    print 'FILENAME: ', fileName
    #renderFolder = fileName.rpartition('/')[0].rpartition('/')[2]
    #print renderFolder

    tempNestFolder = fileName.rpartition(shotNumber)[2].partition('/')[2].rpartition('/')[0]
    nestHeirarchy = tempNestFolder.split('/')
    targetPath = publishPath
    for x in nestHeirarchy:
        targetPath = targetPath + '/' + x
        #print 'MYPATH: ', targetPath
        if not os.path.exists(targetPath):
            print '####################making a new folder @ %s' % targetPath
            os.mkdir(targetPath)

    #targetPath = '%s/%s'%(publishPath, tempNestFolder)
    
    globCopy(fileName, targetPath)

'''
#os.listdir(publishPath)
#os.mkdir(
    

######### List file index & copy to publishPath directory

#nestFolders = list(set(tempNestFolders))
#print nestFolders
'''


********************************************************************************
********************************************************************************
>> # See header
********************************************************************************
'''
Utilities to be used by FX_makeDailies.py in Nuke

@author DMajor
'''

def dailiesPostRender(outputFolder, writeFiles, dailiesFolder, **args):
    import os
    print '>>>>>>>>>>>>>>>>>>>>> Entering dailiesPostRender script'

    print 'Output Directory...', outputFolder
    print 'Write Files...', writeFiles
    print 'Dailies Directory...', dailiesFolder

    print 'Take <files> from <outputDIR> through a ffmpeg and output in the <dailiesDIR>'
    print 'copy <files> using shutil'

    ffmpegInput = writeFiles
    ffmpegOutput = '%s/%s.mp4' % ( outputFolder.rpartition('/')[0], writeFiles.rpartition('/')[2].split('.')[0] )

    #print ffmpegInput
    #print ffmpegOutput

    processFrames = "ffmpeg -vcodec mjpeg -pix_fmt yuvj422p -f image2 -qscale 1 -r 24 -y -i %s %s" % (ffmpegInput, ffmpegOutput)
    print processFrames
    try:
        os.system(processFrames)
    except (OSError, RuntimeError), error:
        print error

'''
ffmpeg data:
    OpenEXR support? - Use DPX, TIFF or JPEG for conversion to input
    metaTag: -map 0:0 -map 1:0 -metadata stereo_mode=left_right #Output to stereo
    codec: Prores - Photo JPEG? - H.264

 2k mono @ 48 fps (422)
ffmpeg 
        -y #overwrite output files (-n does not overwrite)
        -probesize 5000000 
        -f image2 
        -r 48 
        -force_fps 
        -i ${DPX_HERO} 
        -c:v mjpeg 
        -qscale:v 1 
        -vendor ap10 
        -pix_fmt yuvj422p 
        -s 2048x1152 
        -r 48 
        output.mov

To convert down to a .mov or .mp4 file, use external compiler.


#/norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_output/sc0000-sh99999_someThru.%04d.exr
#/norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_someThru.mp4

#ffmpeg -vcodec mjpeg -pix_fmt yuvj422p -f image2 -qscale 1 -r 24 -n -i /norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_output/sc0000-sh99999_someThru.%04d.exr /norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_someThru.mp4

#/norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_output/sc0000-sh99999_stuffThru.%04d.jpeg
#/norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_stuffThru.mp4

#ffmpeg -vcodec mjpeg -pix_fmt yuvj422p -f image2 -qscale 1 -r 24 -n -i 

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import os
import subprocess

print '>>>>>>>>>>>>>>>>>>>>> Entering dailiesPostRender script'

print 'Output Directory...', outputFolder
print 'Write Files...', writeFiles
print 'Dailies Directory...', dailiesFolder

print 'Take <files> from <outputDIR> through a ffmpeg and output in the <dailiesDIR>'
print 'copy <files> using shutil'

#ffmpegInput = writeFiles
#ffmpegOutput = '%s/%s.mp4' % ( outputFolder.rpartition('/')[0], writeFiles.rpartition('/')[2].split('.')[0] )

#print ffmpegInput
#print ffmpegOutput

processFrames = "ffmpeg -vcodec mjpeg -pix_fmt yuvj422p -f image2 -qscale 1 -r 24 -n -i /norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_output/sc0000-sh99999_sucessTest.%04d.jpeg /norman/work/dmajor/FX/Generic_Tests/nuke_dailiesTool/sc0000-sh99999_sucessTest.mp4"
print processFrames
try:
    #os.system("echo" + processFrames)
    process = subprocess.Popen(processFrames, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
except (OSError, RuntimeError), error:
    print error
'''

********************************************************************************
********************************************************************************
>> # See header
********************************************************************************
'''
FX Dailies - Create folders in dailies directories and write files to a local
    output folder. Prints/returns a ffmpeg command in the script editor for
    converting the output jpegs to an mp4.

Created: Feb 16, 2014
Updated: March 31, 2014
Updated: April 25, 2014
    - Fixed bug for deleting created write/retime nodes
    - Added a 'set up shot for stereo' to fix an error out

Company: Mikros Image - MUNE
@author: DMajor
'''

localSource = '/norman/work/dmajor/Scripting/Sandbox'
if sys.path.count(localSource) == 0:
    print 'adding localSource to sys.path'
    sys.path.append(localSource)
else:
    print 'localSource is already part of the sys.path'

###########################################
import nuke
import datetime, re, os, sys
import FX_nukeToolbox.WIP.nukeUtil as nukeUtil

def createOutputDirectories(dailiesState, currentDate, shotNumber, FXtype, **args):
    #print args
    print shotNumber

    rootFolder = nuke.Root().name().rpartition('/')[0]
    outputFolder = '%s/%s_output' % (rootFolder, shotNumber)
    
    if not os.path.exists(outputFolder): #Check to see if the folder already exists
        print 'making a new folder at: ', outputFolder
        os.mkdir(outputFolder) #make directory for the rest of the path names
    else: print 'folder already exists at: ', outputFolder

    dailiesFolder = '/s/prods/mune/Dailies/9_FX/%s/%s/%s/%s_%s' % (
                dailiesState, currentDate, shotNumber, shotNumber, FXtype)
    dailiesShotFolder = dailiesFolder.rpartition('/')[0]
    dailiesDateFolder = dailiesShotFolder.rpartition('/')[0]
    print dailiesFolder, dailiesShotFolder, dailiesDateFolder

    if not os.path.exists(dailiesFolder):
        print 'making a new folder at: ', dailiesFolder
        if not os.path.exists(dailiesShotFolder):
            if not os.path.exists(dailiesDateFolder):
                os.mkdir(dailiesDateFolder)
            os.mkdir(dailiesShotFolder)
        os.mkdir(dailiesFolder)
    else: print 'folder already exists at: ', dailiesFolder

    return outputFolder, dailiesFolder

def dailiesWriteNode(shotNumber, outputFolder, FXtype, dailiesFolder, **args):
    firstFrame = nuke.Root()['first_frame'].value() - 100
    lastFrame = nuke.Root()['last_frame'].value() - 100

    dailiesRetime = nuke.createNode('Retime')
    tempName = dailiesRetime.fullName()
    nuke.toNode(tempName).setName('dailiesRetime')
    retimeName = dailiesRetime.fullName()

    dailiesRetime.knob('input.first_lock').setValue(1)
    dailiesRetime.knob('output.first_lock').setValue(1)
    dailiesRetime.knob('output.first').setValue(1)

    #userWork = os.environ['APERO_WORK']
    writeFiles = '%s/%s_%s.%s.jpeg' % (outputFolder, shotNumber, FXtype, '%04d')
    dailiesOutputWrite = nuke.createNode('Write')

    dailiesOutputWrite.knob('file').setValue(writeFiles)
    dailiesOutputWrite.knob('views').setValue('left')

    nuke.toNode(dailiesOutputWrite.fullName()).setName('exportDailies_NEW')
    writeNode = dailiesOutputWrite.fullName()

    #print writeNode

    dailiesOutputWrite.knob('afterRender').setValue(
            "nukeUtil.dailiesPostRender('%s','%s','%s')"% (outputFolder, writeFiles, dailiesFolder) )

    return writeFiles, dailiesOutputWrite, firstFrame, lastFrame, dailiesRetime


'''
## GUI creation
def createPublishGUI():
    publishGUI = nuke.Panel('Submit files to publish folders:...', 450)

    existingFileName = nuke.Root().name().split('/')[-1]

    searchTerm = re.compile('sc\d*-sh\d*')
    fileName = searchTerm.findall(existingFileName)[0]

    publishGUI.addSingleLineInput('Shot Number:', fileName)


    #FXtype = <Pull from publish folder>
    # In case of multiple folders: Set up parse through read node inputs
'''


def createDailiesGUI():
    
    dailiesGUI = nuke.Panel('Export to Dailies folders:...', 450)

    #add elements to panel
    #name will be grabbed from existing file.

    existingFileName = nuke.Root().name().split('/')[-1]

    searchTerm = re.compile('sc\d*-sh\d*')
    fileName = searchTerm.findall(existingFileName)[0]
    #outputPathDirectory = 

    #Start content
    dailiesGUI.addSingleLineInput('Shot Number:', fileName)
    FXtype = dailiesGUI.addSingleLineInput('FX Type:', '<Effect>')

    #dailiesGUI.addFilenameSearch('Select output folder:', 'Choose output directory')
    dailiesState = dailiesGUI.addEnumerationPulldown(
                    'Output Dailies folder:',
                    '2_WFA 1_SUP 3_APP')

    dailiesGUI.addButton('Cancel')
    dailiesGUI.addButton('Export')
    
    result = dailiesGUI.show()
    if result == 1:
        if nuke.selectedNodes() == []:
            nuke.message('Please select the output node')
            return #Break the tool
        currentNode = nuke.selectedNodes()#[0]

        dailiesState = dailiesGUI.value('Output Dailies folder:')
        currentDate = datetime.datetime.now().strftime('%Y_%m_%d')
        shotNumber = dailiesGUI.value('Shot Number:')
        FXtype = dailiesGUI.value('FX Type:')
        outputFolder, dailiesFolder = createOutputDirectories(
                            dailiesState, currentDate, shotNumber, FXtype)
        
        writeFiles, writeNode, firstFrame, lastFrame, dailiesRetime = dailiesWriteNode(shotNumber, outputFolder, FXtype, dailiesFolder)

        nukescripts.stereo.setViewsForStereo()

        #print writeNode
        nuke.execute(writeNode, firstFrame, lastFrame)

        nuke.delete(writeNode)
        nuke.delete(dailiesRetime)

        #print dailiesFolder
    else:
        print 'nothing happened...'
        
def mainFunc():
    createDailiesGUI()

reload(nukeUtil)
mainFunc()

********************************************************************************
********************************************************************************
>> # For finding the shot code and creating BIG text on screen - Christine...
********************************************************************************
import nuke
import re

def deselectAll():
    nuke.selectAll()
    nuke.invertSelection()

def selectList(objList):
    deselectAll()
    for item in objList:
        item.setSelected(1)

existingFileName = nuke.Root().name().split('/')[-1]

searchTerm = re.compile('sc\d*-sh\d*')
fileName = searchTerm.findall(existingFileName)[0]

if nuke.nodesSelected():
    selectedNodes = nuke.selectedNodes()
    if len(selectedNodes) > 1:
        raise RuntimeError('You have more than a single node selected')
    currentNode = nuke.selectedNodes()[0]
    print 'Merging text with: %s...' % currentNode.name()
else:
    raise RuntimeError('You have nothing selected')

deselectAll()
shotText = nuke.createNode('Text')
shotText['message'].setValue(fileName)
shotText['font'].setValue('/usr/share/fonts/truetype/trebucbi.ttf')
shotText['size'].setValue(100)

dilateNode = nuke.createNode('Dilate')

dilateGrade = nuke.createNode('Grade')

dilateNode['size'].setValue(6)
dilateGrade['blackpoint'].setValue(1)

textMerge = nuke.createNode('Merge')

textMerge.setInput(0, dilateGrade)
textMerge.setInput(1, shotText)

selectList([textMerge, currentNode])
mergeAll = nuke.createNode('Merge')

selectList([shotText, dilateNode, dilateGrade, textMerge])

********************************************************************************
********************************************************************************
>> # Parse through published folders to find latest sequence and import to read
>> # node for testing/compositing. Plus other things...
********************************************************************************
import nuke
import os, re

def runInitializeShot(shotNumber, *args):
    publishDir = os.environ['APERO_PUB'] + '/mune/sh/' + shotNumber

    shotType = ''
    if os.path.exists(publishDir + '/comp'):
        shotType = 'comp'
        print '\nUsing the comp publish'
    elif os.path.exists(publishDir + '/anf'):
        shotType = 'anf'
        print '\nComp publish does not exist. Using the anf publish'
    else:
        print 'Could not find anf or comp publishes for the shot requested.'
        
    directoryInQuestion = '%s/%s/' % (publishDir, shotType)
    if shotType != '':
        
        dirContents = os.listdir(directoryInQuestion)
        
        availableDirs = []
        availableSequence = []

        for item in dirContents:
            try:
                os.chdir(directoryInQuestion+item)
                availableDirs.append(item)
            except (OSError), err:
                pass
        
        print 'Using publish', availableDirs[-1].rpartition('.')[2]
        
        latestPublishDirContents = os.listdir(directoryInQuestion+availableDirs[-1])
        
        for item in latestPublishDirContents:
            if [item.rpartition('.')[2] == x for x in ['exr', 'jpeg', 'png']] != [False, False, False]:
                if item.count('right') != 0:
                    continue
                availableSequence.append(item)
        
        availableSequence.sort()

        sequenceName = availableSequence[-1].rpartition('.')[0].rpartition('.')[0]
        sequenceExtension = availableSequence[-1].rpartition('.')[2]
        sequenceIterationVariable = '%0{0}d'.format(len(availableSequence[-1].split('.')[-2]))
        startFrame = int(availableSequence[0].rpartition('.')[0].rpartition('.')[2])
        endFrame = int(availableSequence[-1].rpartition('.')[0].rpartition('.')[2])

        sourceSequence = '{0}{1}/{2}.{3}.{4}'.format(
                directoryInQuestion, availableDirs[-1], 
                sequenceName, sequenceIterationVariable, sequenceExtension)

    if sourceSequence:
        sourceRead = nuke.createNode('Read')
        sourceRead['file'].setValue(sourceSequence)
        sourceRead['first'].setValue(startFrame)
        sourceRead['last'].setValue(endFrame)

        nuke.createNode('Reformat')

        nuke.root()['first_frame'].setValue(startFrame)
        nuke.root()['last_frame'].setValue(endFrame)
        
        MUNEformat = '1552 650 MUNE'
        nuke.addFormat( MUNEformat )
        nuke.root()['format'].setValue( 'MUNE' )
        nukescripts.stereo.setViewsForStereo()

def createShotInitializationGUI():
    
    dailiesGUI = nuke.Panel('Initialize shot:... ', 450)

    existingFileName = nuke.Root().name().split('/')[-1]

    try:
        searchTerm = re.compile('sc\d*-sh\d*')
        fileName = searchTerm.findall(existingFileName)[0]
    except (IndexError), err:
        print err
        fileName = '<shotNumber>'
    
    #Start content
    dailiesGUI.addSingleLineInput('Shot Number:', fileName)    

    dailiesGUI.addButton('Cancel')
    dailiesGUI.addButton('Load')
    
    result = dailiesGUI.show()
    if result == 1:
        shotNumber = dailiesGUI.value('Shot Number:')
        runInitializeShot(shotNumber)

    else:
        print 'nothing happened...'
        
def mainFunc():
    createShotInitializationGUI()

mainFunc()

********************************************************************************
********************************************************************************
>> # See header
********************************************************************************


********************************************************************************
********************************************************************************
>> # See header
********************************************************************************


