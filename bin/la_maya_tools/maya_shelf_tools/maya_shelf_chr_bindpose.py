import os
import sys
import glob
import json

from maya import cmds

shot_root  = os.environ['IJ_SHOT_PATH']
cmds.loadPlugin('AbcExport')

# The fun starts here... ######################################################
print '\n' * 5
print '*' * 80
print 'Starting Character bind pose setup...'

# OPEN UNDO CHUNK
cmds.undoInfo( openChunk=True )

shot_root  = os.environ['IJ_SHOT_PATH']
json_file  = open( os.path.join(shot_root, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )[0]
json_file.close()
chars      = json_data['assets']['chars']
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])
char_roots      = cmds.ls('*IJ_CHR_*')
rig_controllers = cmds.ls('*ij_chr_*:rig_controllers_set', sets=True)

for char in chars:
    sel = cmds.ls(selection=True)
    if sel == None:
        continue
    sel = sel[0]
    if not 'IJ_CHR' in sel:
        continue
    name_part = sel.split('_')[-2]
    if not name_part.lower() in char:
        continue

    char_name = char.split('ij_chr_')[-1]
    print '\t****************************************'
    print '\tStarting export setup for', char_name

    char_root = ''
    for i in char_roots:
        if char_name in i.lower():
            char_root = i
    print '\t\tFound root called %s' % char_root

    ctl_set = ''
    for i in rig_controllers:
        if char_name in i.lower():
            ctl_set = i
    print '\t\tFound set called %s' % ctl_set

    cmds.select(ctl_set, replace=True)
    controllers = cmds.ls(sl=True)
    global_ctl = ''
    for i in controllers:
        if 'global_C0_ctl' in i:
            global_ctl = i
    print '\t\tFound %d controllers' % len(controllers)
    print '\t\tFound global controller %s' % global_ctl

    curves = cmds.listConnections(controllers, type='animCurve')
    print '\t\tFound %d animation curves' % len(curves)

    print '\t\tSetting key on first frame...'
    cmds.currentTime(frame_s)
    cmds.setKeyframe()

    print '\t\tRemoving all keys before start.'
    cmds.cutKey(time=(-9999,frame_s-1))

    print '\t\tRemoving all keys after end.'
    cmds.cutKey(time=(frame_e+1,100000))

    print '\t\tSetting hold keys...'
    cmds.currentTime(frame_s - 1)
    cmds.setKeyframe()
    cmds.currentTime(frame_e + 1)
    cmds.setKeyframe()

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 20)
    # UPDATE SHIT ###################################################
    # update for switching from IK to FK on the arms, to stop
    # intersections for use in sim export.
    for i in cmds.ls(sl=True):
        if 'shoulder_L0_ctl' in i:
            cmds.setAttr(i + '.arm_L0_blend', 0)
        if 'shoulder_R0_ctl' in i:
            cmds.setAttr(i + '.arm_R0_blend', 0)
    #################################################################
    cmds.setKeyframe()

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 21)
    # UPDATE SHIT ###################################################
    # update for switching from IK to FK on the arms, to stop
    # intersections for use in sim export.
    for i in cmds.ls(sl=True):
        if 'shoulder_L0_ctl' in i:
            cmds.setAttr(i + '.arm_L0_blend', 0)
        if 'shoulder_R0_ctl' in i:
            cmds.setAttr(i + '.arm_R0_blend', 0)
    #################################################################
    cmds.setKeyframe()

    print '\t\tSetting attributes for sim bind pose...'
    cmds.currentTime(frame_s - 40)
    cmds.select( global_ctl, d=True )
    for i in cmds.ls(sl=True):
        try:
            cmds.setAttr(i + '.tx', 0)
            cmds.setAttr(i + '.ty', 0)
            cmds.setAttr(i + '.tz', 0)
            cmds.setAttr(i + '.rx', 0)
            cmds.setAttr(i + '.ry', 0)
            cmds.setAttr(i + '.rz', 0)
            if 'shoulder_L0_ctl' in i:
                cmds.setAttr(i + '.arm_L0_maxstretch', 1)
            if 'shoulder_R0_ctl' in i:
                cmds.setAttr(i + '.arm_R0_maxstretch', 1)
            # UPDATE SHIT ###################################################
            # update for switching from IK to FK on the arms, to stop
            # intersections for use in sim export.
            if 'shoulder_L0_ctl' in i:
                cmds.setAttr(i + '.arm_L0_blend', 0)
            if 'shoulder_R0_ctl' in i:
                cmds.setAttr(i + '.arm_R0_blend', 0)
            #################################################################
        except:
            pass
    cmds.select(ctl_set, replace=True)
    cmds.setKeyframe()
    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 41)
    # UPDATE SHIT ###################################################
    # update for switching from IK to FK on the arms, to stop
    # intersections for use in sim export.
    for i in cmds.ls(sl=True):
        if 'shoulder_L0_ctl' in i:
            cmds.setAttr(i + '.arm_L0_blend', 0)
        if 'shoulder_R0_ctl' in i:
            cmds.setAttr(i + '.arm_R0_blend', 0)
    #################################################################
    cmds.setKeyframe()

    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 58)
    cmds.setKeyframe()
    print '\t\tSetting hold key...'
    cmds.currentTime(frame_s - 59)
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
            if 'shoulder_L0_ctl' in i:
                cmds.setAttr(i + '.arm_L0_maxstretch', 1)
            if 'shoulder_R0_ctl' in i:
                cmds.setAttr(i + '.arm_R0_maxstretch', 1)
            if 'foot_L0_fk0_ctl' in i:
                cmds.setAttr(i + '.foot_L0_toeLift', 0)
            if 'foot_R0_fk0_ctl' in i:
                cmds.setAttr(i + '.foot_R0_toeLift', 0)
            if 'foot_L0_fk0_ctl' in i:
                cmds.setAttr(i + '.foot_L0_ballBendLift', 0)
            if 'foot_R0_fk0_ctl' in i:
                cmds.setAttr(i + '.foot_R0_ballBendLift', 0)
            # UPDATE SHIT ###################################################
            # update for switching from IK to FK on the arms, to stop
            # intersections for use in sim export.
            if 'shoulder_L0_ctl' in i:
                cmds.setAttr(i + '.arm_L0_blend', 1)
            if 'shoulder_R0_ctl' in i:
                cmds.setAttr(i + '.arm_R0_blend', 1)
            #################################################################
        except:
            pass
    cmds.setKeyframe()
    cmds.filterCurve( curves )

# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
# cmds.undo()
cmds.playbackOptions(minTime=frame_s - 60)
cmds.currentTime(frame_s - 60)
cmds.select(char_root, replace=True)
print 'Done with bind pose setup.'
