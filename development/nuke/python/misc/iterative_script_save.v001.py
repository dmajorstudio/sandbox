# ===============================================================================
#             Katana/Nuke: Iterative save scene [*/*_fur_####.nk/katana]
# ===============================================================================
# Using `DM_iterSaveShotScene('nuke//katana')` will save your scene
#     based off the above naming convention in your working directories.

import os

def DM_iterSaveShotScene(DM_package='nuke', *args):
    '''
    Looks into your directory and saves a new iteration of the package script
        based on the contents of that folder and the argument passed.
        ie. DM_iterSaveShotScene(string,*)
    '''
    DM_user = os.environ['USER']
    DM_job = os.environ['JOB']
    DM_shot = os.environ['SHOT']

    if DM_package == 'nuke':
        DM_packageFolder, DM_fileExtension = 'nuke', 'nk'
        DM_savePath = '/jobs/%s/%s/%s/techanim/%s/' % (DM_job, \
                DM_shot, DM_packageFolder, DM_user)
    if DM_package == 'katana':
        DM_packageFolder, DM_fileExtension = 'katana', 'katana'
        DM_savePath = '/jobs/%s/%s/%s/techanim/%s/' % (DM_job, \
                DM_shot, DM_packageFolder, DM_user)

    if not os.path.exists(DM_savePath):
        os.makedirs(DM_savePath)

    DM_pathContents = os.listdir(DM_savePath)

    DM_itr = int(1)
    DM_itrSet = []
    for DM_item in DM_pathContents:
        if DM_item.enswith('.'+DM_fileExtension) and (DM_item.find('_') != -1):
            DM_itrItem = int(DM_item.rpartition('.')[0].rpartition('_')[2])
            DM_itrSet.append(DM_itrItem)

    DM_itrSet.sort()
    if len(DM_itrSet) > 0:
        DM_itr = DM_itrSet[-1] + 1

    DM_fileName = '%s_fur_%04d.%s' % (DM_shot.rpartition('/')[2], \
            DM_itr, DM_fileExtension)

    if DM_package == 'nuke': nuke.scriptSaveAs(DM_savePath+DM_fileName)
    if DM_package == 'katana': KatanaFile.Save(DM_savePath+DM_fileName)