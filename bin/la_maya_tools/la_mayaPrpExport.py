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
print 'Starting Animation Shot Props Export... Good luck!'

# OPEN UNDO CHUNK
cmds.undoInfo( openChunk=True )

shot_root  = os.environ['IJ_SHOT_PATH']
json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
props      = json_data['assets']['props']
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])
prop_roots      = cmds.ls('*ij_prp_*')
rig_controllers = cmds.ls('*ij_prp_*_rig:propctl_set', sets=True)
rig_controllers_alt = cmds.ls('*ij_prp_*_rig:rig_controllers_set', sets=True)
print '\tWorking in %s' % shot_root

# cmds.delete( all=True, sc=True )

for prop in props:
    prop_name = prop.split('ij_prp_')[-1]
    print '\t****************************************'
    print '\tStarting export setup for', prop_name

    prop_root = ''
    for i in prop_roots:
        if prop_name in i.lower():
            prop_root = i
    print '\t\tFound root called %s' % prop_root

    ctl_set = ''
    for i in rig_controllers:
        if prop_name in i.lower():
            ctl_set = i
    if ctl_set == '':
        for i in rig_controllers_alt:
            if prop_name in i.lower():
                ctl_set = i
    print '\t\tFound set called %s' % ctl_set

    cmds.select(ctl_set, replace=True)
    controllers = cmds.ls(sl=True)
    global_ctl = ''
    for i in controllers:
        if 'global' in i:
            global_ctl = i
        if 'lunchbag' in prop_name:
            if 'bottom_001_ctl' in i:
                global_ctl = i
    print '\t\tFound %d controllers' % len(controllers)
    print '\t\tFound global controller %s' % global_ctl

    try:
        curves = cmds.listConnections(controllers, type='animCurve')
        print '\t\tFound %d animation curves' % len(curves)
    except Exception e:
        print '\t\tFound NO animation curves'

    print '\t\tSetting key on first frame...'
    cmds.currentTime(frame_s)
    cmds.setKeyframe()

    print '\t\tRemoving all keys before start.'
    cmds.cutKey(time=(-9999,frame_s-1))

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 1)
    cmds.setKeyframe()

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 10)
    cmds.setKeyframe()
    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 11)
    cmds.setKeyframe()

    print '\t\tSetting attributes for sim bind pose...'
    cmds.currentTime(frame_s - 30)
    cmds.select( global_ctl, d=True )
    for i in cmds.ls(sl=True):
        try:
            cmds.setAttr(i + '.tx', 0)
            cmds.setAttr(i + '.ty', 0)
            cmds.setAttr(i + '.tz', 0)
            cmds.setAttr(i + '.rx', 0)
            cmds.setAttr(i + '.ry', 0)
            cmds.setAttr(i + '.rz', 0)
        except:
            pass
    cmds.select(ctl_set, replace=True)
    cmds.setKeyframe()
    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 31)
    cmds.setKeyframe()

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 50)
    cmds.setKeyframe()
    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 51)
    cmds.setKeyframe()

    print '\t\tSetting attributes for world bind pose...'
    cmds.currentTime(frame_s - 60)
    for i in cmds.ls(sl=True):
        try:
            cmds.setAttr(i + '.tx', 0)
            cmds.setAttr(i + '.ty', 0)
            cmds.setAttr(i + '.tz', 0)
            cmds.setAttr(i + '.rx', 0)
            cmds.setAttr(i + '.ry', 0)
            cmds.setAttr(i + '.rz', 0)
        except:
            pass
    cmds.setKeyframe()

    cmds.filterCurve( curves )

    # all_meshes    = cmds.listRelatives(prop_root, allDescendents=True, fullPath=True, type='mesh')
    # cmds.select(all_meshes, replace=True)
    # cmds.pickWalk( direction='up' )

    abc_export_path = os.path.join(shot_root, 'geo', 'anim_export')
    if not os.path.exists(abc_export_path):
        os.mkdir(abc_export_path)

    abc_anim_name = 'anim_export_%s_anim.abc' % prop_name
    # export_string = ''
    # for i in cmds.ls(sl=True, long=True):
    #     export_string += ' -root %s ' % i
    export_string = ' -root %s' % prop_root
    print '\t\tExporting ABC file...'
    cmd  = '-frameRange %d %d' % (frame_s - 61, frame_e + 1)
    cmd += ' -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeCreases -writeUVSets -stripNamespaces 0 -dataFormat ogawa '
    cmd += export_string
    cmd += ' -file %s' % os.path.join(abc_export_path, abc_anim_name)
    cmds.AbcExport ( j=cmd )

# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
# cmds.undo()
cmds.currentTime(frame_s)
print 'Done with export. If you see this, it worked. Cheers!'
