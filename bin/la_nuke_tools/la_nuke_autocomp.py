import os
import sys
import json
import shutil
import re

################################################################################
def nvNukeScriptParse(nuke_script):
    nuke_file = open(nuke_script, 'r')
    nuke_data = nuke_file.readlines()
    nuke_file.close()

    array_of_nodes_whole = []

    i = 0
    for line in nuke_data:
        if line.strip().endswith('{'):
            print line
        elif line.strip().startswith('}'):
            print line
        if i > 1000:
            exit()
        i += 1

################################################################################

print 'Starting AutoComp...'

# Get all env vars needed.
print '\tGetting Info...'
proj_path = os.environ['IJ_LUMA_PROJ_ROOT']
print '\tGot %s as project root.' % proj_path
shot_name = os.environ['IJ_SHOT_NAME']
print '\tGot %s as shot name' % shot_name
shot_nums = os.environ['IJ_SHOT']
shot_path = os.environ['IJ_SHOT_PATH']
print '\tGot %s as shot path.' % shot_path
# Read JSON file for comp info and frame ranges, etc.
json_file  = open( os.path.join(shot_path, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )
json_file.close()
frame_start = int(json_data[0]['clip_start'])
frame_end   = int(json_data[0]['clip_end'])
print '\tGot Frame Ranges as %04d to %04d.' % (frame_start, frame_end)
# Get Comp Template
comp_template = ''
try:
    comp_template = str(json_data[0]['comp_template'])
except:
    print '\tNo Comp Template Found! Using default.'
    comp_template = os.path.join( proj_path, 'assets', 'comp', 'templates', 'MASTER', 'ij_comp_template_MASTER.nk' )
print '\tSet Comp Template to %s.' % comp_template

# Copy template comp to shot location
comp_name = os.path.join( shot_path, shot_name + '_comp_v01.nk' )
print '\tSet Shot Comp to be %s.' % comp_name
if os.path.exists(comp_name):
    try:
        os.remove(comp_name)
    except:
        print 'ERROR! Could not remove old comp file. Exiting.'
        exit()
shutil.copy2(comp_template, comp_name)
# nvNukeScriptParse(comp_name)

# Edit comp paths to latest render version
