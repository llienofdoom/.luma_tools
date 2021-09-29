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
    char_root = ''
    if char_name in i.lower():
        char_root = i
    abc_export_path = os.path.join(shot_root, 'geo', 'anim_export')
    abc_anim_name = 'anim_export_%s_anim.abc' % char_name
    path = '%s' % os.path.join(abc_export_path, abc_anim_name)
    cmd = 'la_blender /mnt/luma_i/_tools/blender/empty_scene.blend --python /mnt/luma_i/_tools/blender/blender_load_chr_abc.py -- ' + path
    os.system( cmd )
    
print 'Done with Export.'
