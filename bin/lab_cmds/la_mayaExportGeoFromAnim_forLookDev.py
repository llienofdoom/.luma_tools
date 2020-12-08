import os
import glob
import json

import maya.standalone
import maya.cmds as cmds
maya.standalone.initialize( name='python' )

root = os.environ['IJ_SHOT_PATH']
anim_file_path = glob.glob(root + os.sep + '*_animation_v*.mb')

json_file = open(root + os.sep + 'shot_info.json', 'r')
json_data = json.load(json_file)
json_file.close()

f_start = json_data[0]['clip_start']
f_end   = json_data[0]['clip_end'  ]

if len(anim_file_path) != 0:
    anim_file_path.sort()
    anim_file_path = anim_file_path[-1]
else:
    exit()

cmds.loadPlugin('AbcExport')
cmds.loadPlugin('mgear_solvers')
cmds.loadPlugin('weightDriver')
print 'Opening fake file'
cmds.file('/mnt/luma_i/assets/chr/rig/ij_chr_alejandro/50/characters_ij_chr_alejandro_50.mb', open=True, force=True, resetError=True)
print 'Opening ', anim_file_path
cmds.file(anim_file_path, open=True, force=True, resetError=True)
cmds.loadPlugin('AbcExport')
cmds.loadPlugin('mgear_solvers')
cmds.loadPlugin('weightDriver')

geos = cmds.ls('*:*geo_set')

print '\n*10'

print 'Exporting...'
for geo in geos:
    name = geo.split(':')[0]
    print 'Exporting', name
    path = root + os.sep + 'geo' + os.sep + name + '_lookDev.abc'
    children = cmds.pickWalk(geo, direction='down')
    geoToExport = ''
    for i in children:
        geoToExport += '-root %s ' % i

    command  = '-frameRange %d %d' % (f_start - 70, f_end)
    command += ' -uvWrite'
    command += ' -writeColorSets'
    command += ' -writeFaceSets'
    command += ' -wholeFrameGeo'
    command += ' -worldSpace'
    command += ' -writeVisibility'
    command += ' -writeCreases'
    command += ' -writeUVSets'
    command += ' -dataFormat ogawa '
    command += geoToExport 
    command += ' -file %s' % path
    # print command
    cmds.AbcExport ( j=command )
