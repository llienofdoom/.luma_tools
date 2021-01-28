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

print 'Opening fake file'
cmds.file('/mnt/luma_i/assets/chr/rig/ij_chr_alejandro/50/characters_ij_chr_alejandro_50.mb', open=True, force=True, resetError=True)
print 'Opening ', anim_file_path
cmds.file(anim_file_path, open=True, force=True, resetError=True)
cmds.loadPlugin('AbcExport')

# The fun starts here... ######################################################
print '\n' * 5
print '*' * 80
print 'Starting Animation Shot Scene Export... Good luck!'

# OPEN UNDO CHUNK
cmds.undoInfo( openChunk=True )

# PREP ########################################################################
shot_root  = os.environ['IJ_SHOT_PATH']
json_file  = open( os.path.join(shot_root, 'shot_info.json') )
json_data  = json.load( json_file )[0]
chars      = json_data['assets']['chars']
char_props = json_data['assets']['props']
env        = json_data['assets']['env'  ]
frame_s    = int(json_data['clip_start'])
frame_e    = int(json_data['clip_end'  ])
print '\tWorking in %s' % shot_root

# Delete Static Channels
cmds.delete( all=True, sc=True )

# ENV ROOT ####################################################################
print '\tEnvironment starting.'
env_root = ''
try:
    env_root = cmds.ls(env + '*')[0]
except:
    print 'Failed to get ENV root node.'
    sys.exit()
print '\t\tLooked for %s, and got %s.' % (env, env_root)

# LIST OF PROPS ###############################################################
list_of_props = []
props         = []
try:
    list_of_props = cmds.ls('ij_prp_*')
    if len(char_props) > 0:
        for prp in char_props:
            matching = fnmatch.filter(list_of_props, prp + '*')
            if len(matching) > 0:
                for i in matching:
                    list_of_props.remove(i)
    props = list_of_props
except:
    print 'Failed to get list of props.'
    sys.exit()

# GET geo for env #############################################################
env_geo_anim   = []
env_geo_static = cmds.listRelatives(env_root, allDescendents=True, fullPath=True,  type='mesh')
print '\t\tFound %d geos to export for the base environment.' % len(env_geo_static)
# cmds.select(env_geo, replace=True)

# GET geo for props ###########################################################
print '\t\tContinuing with props...'
for prop in props:
    prop_geo = cmds.listRelatives(prop, allDescendents=True, fullPath=True,  type='mesh')
    prop_ctl = cmds.listRelatives(prop, allDescendents=True, fullPath=True,  type='transform')
    anim_curves = cmds.findKeyframe( prop_ctl, curve=True )
    if anim_curves != None:
        print '\t\t\tANIMATED - ' + prop
        env_geo_anim   += prop_geo
    else:
        print '\t\t\tSTATIC   - ' + prop
        env_geo_static += prop_geo
print '\t\tTotal of %d geos to export for the STATIC environment.' % len(env_geo_static)
print '\t\tTotal of %d geos to export for the ANIMATED environment.' % len(env_geo_anim)

# EXPORT ######################################################################
abc_export_path = os.path.join(shot_root, 'geo', 'anim_export')
print '\n\tWriting environment to %s:' % abc_export_path
try:
    if not os.path.exists(abc_export_path):
        os.mkdir(abc_export_path)
except:
    print 'Failed to create folders for export.'
    sys.exit()
# EXPORT STATIC ###############################################################
if len(env_geo_static) > 0:
    print '\t\t\tStarting Alembic Export of STATIC geo... ',
    abc_static_name = 'anim_export_env_static.abc'
    export_string = ''
    print 'Creating unique names...',
    for i in env_geo_static:
        try:
            transform  = cmds.listRelatives(i, parent=True, fullPath=True)[0]
            parentname = cmds.listRelatives(transform, parent=True, fullPath=True)[0].replace('|', '_').replace(':', '_')
            transform  = cmds.rename( transform, transform.replace('|', '_').replace(':', '_') + '_' + str(random.random()).replace('.', '') )
            transform  = cmds.rename( transform, transform.split(parentname)[-1][1:] )
            export_string += ' -root %s ' % transform
        except Exception as err:
            # print err, '\nFailed at rename STATIC', i
            pass
    print 'Done. Exporting... ',
    cmd  = '-frameRange %d %d' % (frame_s, frame_s)
    cmd += ' -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeCreases -writeUVSets -stripNamespaces -dataFormat ogawa '
    cmd += export_string
    cmd += ' -file %s' % os.path.join(abc_export_path, abc_static_name)
    cmds.AbcExport ( j=cmd )
    print 'Done'
# EXPORT ANIMATED #############################################################
if len(env_geo_anim) > 0:
    print '\t\t\tStarting Alembic Export of ANIMATED geo... ',
    abc_anim_name = 'anim_export_env_anim.abc'
    export_string = ''
    print 'Creating unique names...',
    for i in env_geo_anim:
        try:
            transform  = cmds.listRelatives(i, parent=True, fullPath=True)[0]
            parentname = cmds.listRelatives(transform, parent=True, fullPath=True)[0].replace('|', '_').replace(':', '_')
            transform  = cmds.rename( transform, transform.replace('|', '_').replace(':', '_') + '_' + str(random.random()).replace('.', '') )
            transform  = cmds.rename( transform, transform.split(parentname)[-1][1:] )
            export_string += ' -root %s ' % transform
        except Exception as err:
            # print err, '\nFailed at rename ANIMATED', i
            pass
    print 'Done. Exporting... ',
    cmd  = '-frameRange %d %d' % (frame_s - 1, frame_e + 1)
    cmd += ' -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeCreases -writeUVSets -stripNamespaces -dataFormat ogawa '
    cmd += export_string
    cmd += ' -file %s' % os.path.join(abc_export_path, abc_anim_name)
    cmds.AbcExport ( j=cmd )
    print 'Done'
print '\tDone with environment export!\n'

# CHARS #######################################################################
print '\tStarting on Characters...'
# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
cmds.undo()
print 'Done with export. If you see this, it worked. Cheers!'
