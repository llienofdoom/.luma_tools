import os
import sys
import glob
import json

import maya.standalone
from maya import cmds
maya.standalone.initialize( name='python' )

shot_root = os.environ['IJ_SHOT_PATH']
shot_name = os.environ['IJ_SHOT_NAME']
anim_file_path = glob.glob(shot_root + os.sep + '*_animation_v*.mb')
if len(anim_file_path) != 0:
    anim_file_path.sort()
    anim_file_path = anim_file_path[-1]

print 'Opening fake file'
cmds.file('/mnt/luma_i/assets/chr/rig/ij_chr_alejandro/50/characters_ij_chr_alejandro_50.mb', open=True, force=True, resetError=True)
print '\n' * 5
print '*' * 80
print 'Opening ', anim_file_path
cmds.file(anim_file_path, open=True, force=True, resetError=True)
cmds.loadPlugin('AbcExport')

# The fun starts here... ######################################################
print '\n' * 5
print '*' * 80
print 'Starting Animation Playblast Export.'

json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])

print 'Playblasting from %04d to %04d.' % (frame_s, frame_e)

print 'Setting all cameras to NOT render.'
cams = cmds.ls(type='camera')
for cam in cams:
    print '\tDoing %s' % cam
    cmds.setAttr(cam + '.rnd', 0)
print 'Done with that.'

print 'Setting renderCamera to render.'
renderCamera = cmds.ls('*renderCameraCenterCamShape')
print renderCamera
if renderCamera != None:
    print renderCamera[0]
    cmds.setAttr(renderCamera[0] + '.rnd', 1)
    playblast_path = os.path.join(shot_root, 'img', 'flip', 'playblast_temp', shot_name + '_animation')
    cmds.playblast(f=playblast_path, fmt='image', compression='png', startTime=frame_s, endTime=frame_e, width=2048, height=1152, viewer=False, offScreen=True)
    print 'Done with playblast. Converting...'
else:
    print 'No camera found...'
print 'Done with all. Exiting.'
