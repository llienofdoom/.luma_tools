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
print 'Starting Character Alembic Export...'

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

    print '\t\tGetting list of geos to include in export.'
    geos_json_path = os.path.join( os.environ['IJ_LUMA_PROJ_ROOT'], 'assets', 'chr', 'render', '*'+char_name+'*', 'asset_data', 'export_geo.json' )
    geos_json_file = glob.glob( geos_json_path )
    if len(geos_json_file) > 0:
        geos_json_file = geos_json_file[-1]
        print '\t\tFound export_geo.json file here: %s' % geos_json_file
        json_file       = open( geos_json_file, 'r' )
        geos_json_data  = json.load( json_file )[0]
        json_file.close()
        export_geo = geos_json_data['export_geo']
        print '\t\t%d geos to export.' % len(export_geo)

        all_meshes    = cmds.listRelatives(char_root, allDescendents=True, fullPath=True, type='mesh')
        needed_meshes = []
        for i in all_meshes:
            for j in export_geo:
                if j in i:
                    needed_meshes.append(i)
                    # print 'Found %s, adding.' % i
        cmds.select(needed_meshes, replace=True)
        cmds.pickWalk( direction='up' )

        abc_export_path = os.path.join(shot_root, 'geo', 'anim_export')
        if not os.path.exists(abc_export_path):
            os.mkdir(abc_export_path)

        abc_anim_name = 'anim_export_%s_anim.abc' % char_name
        export_string = ''
        for i in cmds.ls(sl=True, long=True):
            export_string += ' -root %s ' % i
        print '\t\tExporting ABC file...'
        cmd  = '-frameRange %d %d' % (frame_s - 61, frame_e + 1)
        cmd += ' -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeCreases -writeUVSets -stripNamespaces 0 -dataFormat ogawa '
        cmd += export_string
        cmd += ' -file %s' % os.path.join(abc_export_path, abc_anim_name)
        cmds.AbcExport ( j=cmd )
    else:
        print 'ERROR! No export_geo.json file for %s.' % char_name

# CLOSE UNDO CHUNK and RESET
cmds.undoInfo( closeChunk=True )
# cmds.undo()
cmds.playbackOptions(minTime=frame_s - 60)
cmds.currentTime(frame_s - 60)
print 'Done with Export.'
