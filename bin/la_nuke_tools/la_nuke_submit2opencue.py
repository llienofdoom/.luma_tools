import os
import site
import sys
import json
import nuke

if '_comp_v' not in sys.argv[1]:
    print 'No Nuke File Supplied. Quitting. Idiot...'
    exit()

# Setup OpenCue libs
site.addsitedir('/opt/opencue/CURRENT/cuegui/venv/lib/python2.7/site-packages')
os.environ['PATH'] = '/opt/opencue/CURRENT/cuegui/venv/bin' + os.pathsep + os.environ['PATH']

from outline import Outline, cuerun
from outline.modules.shell import Shell
from cuesubmit import JobTypes
from cuesubmit import Layer

os.environ['CUEBOT_HOSTNAME']       = '192.168.34.2'
os.environ['CUEBOT_HOSTS']          = os.environ['CUEBOT_HOSTNAME']
os.environ['CUEBOT_HOSTNAME_OR_IP'] = os.environ['CUEBOT_HOSTNAME']

proj_path  = os.environ['IJ_LUMA_PROJ_ROOT']
shot_name  = os.environ['IJ_SHOT_NAME']
shot_num   = os.environ['IJ_SHOT']
shot_path  = os.environ['IJ_SHOT_PATH']
user       = os.environ['IJ_USER']
nukefile   = sys.argv[1]
nukename   = nukefile.split('/')[-1].split('.')[0]

json_file = open(os.path.join(os.environ['IJ_SHOT_PATH'], 'shot_info.json'), 'r')
json_data = json.load(json_file)[0]
json_file.close()
f_start = json_data['clip_start']
f_end   = json_data['clip_end'  ]
f_start = '%d' % f_start
f_end   = '%d' % f_end
f_range = '%s-%s' % (f_start, f_end)

# LAYERS ############################################################
# RENDER COMP
a = shot_num.split('-')[0].lstrip('0')
c = shot_num.split('-')[1].lstrip('0')
s = shot_num.split('-')[2].lstrip('0')
shot_str = '%s-%s-%s' % (a, c, s)
cmd  = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_nuke_render'
cmd += ' AUTO_Write_EXR'
cmd += ' %s' % nukefile
cmd += ' #ZFRAME#'
NUKE_RENDER_EXR = {
    'name': 'nuke_render_exr',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['nuke']
}
# GENERATE PRORES AND MP4
comp_path = os.path.join(shot_path, 'img', 'comp', nukename)
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' cd %s;' % comp_path
cmd += ' . la_cmd proresmp4;'
FFMPEG_LAYER = {
    'name': 'nuke_generate_videos',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['util'],
    'dependType': Layer.DependType.Layer
}
# POST TO DISCORD
a = shot_num.split('-')[0].lstrip('0')
c = shot_num.split('-')[1].lstrip('0')
s = shot_num.split('-')[2].lstrip('0')
cmd  = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' python /mnt/luma_i/_tools/luma_tools/bin/lab_cmds/la_discord_notify_comp.py %s %s %s;' % (user, '"' + shot_name + ' - Comp Complete! - Batch Render"', os.path.join(shot_path, 'img', 'comp', shot_name + '_comp_v00.mp4'))
NUKE_POST_TO_DISCORD = {
    'name': 'nuke_post_to_discord',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['util']
}
# POST TO FTRACK
a = shot_num.split('-')[0].lstrip('0')
c = shot_num.split('-')[1].lstrip('0')
s = shot_num.split('-')[2].lstrip('0')
shot_str = '%s-%s-%s' % (a, c, s)
cmd  = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' . la_cmd cfp %s;' % shot_str
NUKE_POST_TO_FTRACK = {
    'name': 'nuke_post_to_ftrack',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['util']
}
# UPDATE EDIT
edit_sources_path = os.path.join(proj_path, 'editorial', 'edit_sources_master', 'comp')
cmd  = 'echo source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' echo cd %s/img/comp;' % shot_path
cmd += ' echo cp %s_comp_v00.mov %s/%s.mov;' % (shot_name, edit_sources_path, shot_name)
NUKE_UPDATE_EDIT = {
    'name': 'nuke_update_edit_sources',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['util']
}

# JOB ###############################################################
jobData = {
    'name': nukename + '_comp_exr',
    'shot': shot_name + '_' + user,
    'show': 'inside_job',
    'username': user,
    'layers': [
        # Layer.LayerData.buildFactory(**NUKE_RENDER_EXR),
        # Layer.LayerData.buildFactory(**FFMPEG_LAYER),
        # Layer.LayerData.buildFactory(**NUKE_POST_TO_DISCORD),
        # Layer.LayerData.buildFactory(**NUKE_POST_TO_FTRACK),
        Layer.LayerData.buildFactory(**NUKE_UPDATE_EDIT),
        ]
}

# SUBMIT ############################################################
outline = Outline(jobData['name'], shot=jobData['shot'], show=jobData['show'], user=jobData['username'])
layers = []
for layerData in jobData['layers']:
    layer = Shell(layerData.name, command=layerData.cmd.split(), chunk='1',
                threads=float(layerData.cores), range=str(layerData.layerRange),
                threadable=True)
    layer.set_service(layerData.services[0])
    layers.append(layer)

layer_count = 0
for layer in layers:
    if layer_count > 0:
        layer.depend_all(layers[layer_count - 1])
    layer_count += 1
    outline.add_layer(layer)

jobs = cuerun.launch(outline, use_pycuerun=False)
for job in jobs:
    print(job.name())
    job.setPriority(10)
    job.setMaxCores(1500)
    job.setMaxRetries(3)
