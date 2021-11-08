import os
import sys
import json
import glob
import random
import fnmatch

# MAYA SHIT ###################################################################
import maya.standalone
from maya import cmds
maya.standalone.initialize( name='python' )

shot_root  = os.environ['IJ_SHOT_PATH']
anim_file_path = glob.glob(shot_root + os.sep + '*_animation_v*.mb')
if len(anim_file_path) != 0:
    anim_file_path.sort()
    anim_file_path = anim_file_path[-1]
print 'Opening ', anim_file_path
cmds.file(anim_file_path, open=True, force=True, resetError=True)
cmds.loadPlugin('AbcExport')

# The fun starts here... ######################################################
print '\n' * 5
print '*' * 80
print 'Starting Camera Export... Good luck!'

# OPEN UNDO CHUNK
cmds.undoInfo( openChunk=True )

# PREP ########################################################################
shot_root  = os.environ['IJ_SHOT_PATH']
json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])

try:
    renderCamera_path = os.path.join(shot_root, 'shot_data', 'camera_data', 'render_camera_from_maya.abc')
    renderCamera = cmds.ls('renderCamera')
    cmd  = '-frameRange %d %d' % (frame_s - 2, frame_e + 2)
    cmd += ' -wholeFrameGeo -worldSpace -dataFormat ogawa -root %s' %  renderCamera[0]
    cmd += ' -file %s' % renderCamera_path
    cmds.AbcExport ( j=cmd )
    print 'Done.'
except Exception:
    print 'Couldn\'t export renderCamera.'

# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
# cmds.undo()
print 'Done with export. If you see this, it worked. Cheers!'
