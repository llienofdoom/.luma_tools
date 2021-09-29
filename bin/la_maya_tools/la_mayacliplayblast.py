import os
import sys
import glob
import json

import maya.standalone
from maya import cmds
maya.standalone.initialize( name='python' )

shot_root  = os.environ['IJ_SHOT_PATH']
anim_file_path = glob.glob(shot_root + os.sep + '*_animation_v*.mb')
if len(anim_file_path) != 0:
    anim_file_path.sort()
    anim_file_path = anim_file_path[-1]

print 'Opening fake file'
cmds.file('/mnt/luma_i/assets/chr/rig/ij_chr_alejandro/50/characters_ij_chr_alejandro_50.mb', open=True, force=True, resetError=True)
print 'Opening ', anim_file_path
cmds.file(anim_file_path, open=True, force=True, resetError=True)
cmds.loadPlugin('AbcExport')

# The fun starts here... ######################################################
print '\n' * 5
print '*' * 80
print 'Starting Animation Shot Character Export... Good luck!'

# OPEN UNDO CHUNK
cmds.undoInfo( openChunk=True )

shot_root  = os.environ['IJ_SHOT_PATH']
json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
chars      = json_data['assets']['chars']
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])


# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
print 'Done with export. If you see this, it worked. Cheers!'




# cmds.playblast(f='test.mov', fmt='image')
# cmds.lookThru('renderCamera')

cams = cmds.ls(type='camera')
for cam in cams:
    cmds.setAttr(cam + '.rnd', 0)

# Change the solo cam to renderable
cmds.setAttr(solo_cam + '.rnd', 1)