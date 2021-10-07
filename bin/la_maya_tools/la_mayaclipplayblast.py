import os
import sys
import glob
import json
import shutil

import maya.standalone
from maya import cmds
maya.standalone.initialize( name='python' )

shot_root = os.environ['IJ_SHOT_PATH']
shot_name = os.environ['IJ_SHOT_NAME']
date      = os.environ['IJ_DATE']
user      = os.environ['IJ_USER']
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
print 'Starting Animation Playblast and camera Exports.'

json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])

print 'Exporting renderCamera for render.'
try:
    renderCamera_path = os.path.join(shot_root, 'shot_data', 'camera_data', 'render_camera_from_maya.abc')
    renderCamera = cmds.ls('renderCamera')
    cmd  = '-frameRange %d %d' % (frame_s - 2, frame_e + 2)
    cmd += ' -wholeFrameGeo -worldSpace -dataFormat ogawa -root %s' %  renderCamera[0]
    cmd += ' -file %s' % renderCamera_path
    cmds.AbcExport ( j=cmd )
    print 'Done. Moving on...'
except Exception:
    print 'Couldn\'t export renderCamera.'

try:
    print 'Playblasting from %04d to %04d.' % (frame_s, frame_e)
    print 'Setting all cameras to NOT render.'
    cams = cmds.ls(type='camera')
    for cam in cams:
        print '\tDoing %s' % cam
        cmds.setAttr(cam + '.rnd', 0)
    print 'Done with that.'

    print 'Setting renderCamera to render.'
    renderCamera = cmds.ls('*renderCameraCenterCamShape')
    if renderCamera != None:
        print renderCamera[0]
        cmds.setAttr(renderCamera[0] + '.rnd', 1)
        playblast_path = os.path.join(shot_root, 'img', 'flip', 'playblast_temp', shot_name + '_animation')
        print 'Setting playblast path to: %s' % playblast_path
        print 'Running playblast...'
        cmds.playblast(f=playblast_path, fmt='image', compression='png', startTime=frame_s, endTime=frame_e, width=2048, height=1152, viewer=False)
        print 'Playblast Done.'
        
        print 'Converting to mp4... (Colour still magic O_o. To fix.)'
        video_path = os.path.join(shot_root, 'img', 'flip', shot_name + '_animation_CURRENT.mp4')
        cmd  = 'ffmpeg -y'
        cmd += ' -r 24'
        cmd += ' -start_number %d' % frame_s
        cmd += ' -i %s' % playblast_path + '.%04d.png'
        cmd += ' -s 2048x1152'
        cmd += ' -filter_complex "[0:v]eq=gamma=2.2:contrast=1.2[G];[G]curves=all=\'0/0.1 1/0.9\'[C];[C]drawtext=\'fontcolor=white:font=sans-serif:fontsize=12:x=6:y=555:text=  luma-film - 2020 - inside job %s - %s - %s - frame %%{frame_num}:box=1:boxborderw=5:boxcolor=black:start_number=%d\'[LT]"' % (date, shot_name, user, frame_s)
        cmd += ' -pix_fmt yuv420p -c:v libx264 -crf 25 -map "[LT]"'
        cmd += ' %s' % video_path
        os.system( cmd )

        print 'Done with mp4. Converting to Prores for edit, and moving.'
        prores_path = os.path.join('/mnt/luma_i/editorial/edit_sources_master/current_animation', shot_name + '.mov')
        cmd  = 'ffmpeg -y'
        cmd += ' -i %s' % video_path
        cmd += ' -c:v prores_ks -profile:v 3 -qscale:v 5 -vendor ap10 -pix_fmt yuv422p10le'
        cmd += ' %s' % prores_path
        os.system( cmd )

        print 'Done. Cleaning up images.'
        try:
            pass
            shutil.rmtree(os.path.dirname(playblast_path))
        except Exception:
                print 'Couldn\'t remove folder...'
                sys.exit()
    else:
        print 'No camera found...'
    print 'Done with all. Exiting.'
except Exception:
    print 'Couldn\'t export videos.'