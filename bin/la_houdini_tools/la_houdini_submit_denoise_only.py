from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import site
import sys
import json

from termcolor import colored

site.addsitedir('/opt/opencue/CURRENT/cuegui/venv/lib/python2.7/site-packages')
os.environ[
    'PATH'] = '/opt/opencue/CURRENT/cuegui/venv/bin' + os.pathsep + os.environ[
        'PATH']

from outline import Outline, cuerun
from outline.modules.shell import Shell
from cuesubmit import JobTypes
from cuesubmit import Layer

os.environ['CUEBOT_HOSTNAME'] = '192.168.34.2'
os.environ['CUEBOT_HOSTS'] = os.environ['CUEBOT_HOSTNAME']
os.environ['CUEBOT_HOSTNAME_OR_IP'] = os.environ['CUEBOT_HOSTNAME']

comments = 'Denoise AOV Submission'

shot_name = os.environ['IJ_SHOT_NAME']
shot_path = os.environ['IJ_SHOT_PATH']
user = os.environ['IJ_USER']
hipfile = sys.argv[1]
print('Render hip: ' + hipfile)
hipname = hipfile.split('/')[-1].split('.')[0]

priority = 3

json_file = open(os.path.join(os.environ['IJ_SHOT_PATH'], 'shot_info.json'),
                 'r')
json_data = json.load(json_file)[0]
json_file.close()
f_start = json_data['clip_start']
f_end = json_data['clip_end']
f_start = '%04d' % f_start
f_end = '%04d' % f_end
f_range = '%s-%s' % (f_start, f_end)

# LAYERS ############################################################
#######################################################
#we now build all layers regardless, only choosing layers on submission
###################################################################################################
#######################################################
# NOTE :
# LENTIL FIX OF DEATH
# #######

img_path = os.path.join(shot_path, 'img', 'renders', hipname,
                        hipname + '-rop_ar_main.#ZFRAME#.exr')
print(img_path)
cp_path = os.path.join(shot_path, 'img', 'renders', hipname, "lentil",
                       hipname + '-rop_ar_main.#ZFRAME#.exr')
print(cp_path)
try:
    os.makedirs(os.path.join(shot_path, 'img', 'renders', hipname, 'lentil'))
    #shutil.move(img_path,cp_path)
except:
    pass

cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
#cmd += 'oiiotool %s --attrib "arnold/aovs/RGBA/filter" "RGBA" --attrib "arnold/aovs/variance/filter" "variance_filter" -o %s' %(cp_path,img_path)
cmd += 'python /home/christophe/.luma_tools/bin/lab_cmds/la_lentilfix_inclsssspec.py'
cmd += ' %s' % img_path
cmd += ' %s' % cp_path
cmd += ' %s' % shot_path
cmd += ' %s' % hipname
ARNOLD_RENDER_LENTIL_LAYER = {
    'name': 'arnold_lentil_fix',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '8',
    'services': ['shell'],
    'dependType': Layer.DependType.Layer,
}

#######################################################
# NOTE :
#DENOISE
########
img_path = os.path.join(shot_path, 'img', 'renders', hipname,
                        hipname + '-rop_ar_main.#ZFRAME#.exr')
try:
    os.makedirs(os.path.join(shot_path, 'img', 'renders', hipname, 'denoise'))
except:
    pass
dnz_path = os.path.join(shot_path, 'img', 'renders', hipname, 'denoise',
                        hipname + '-rop_ar_main_denoise.#ZFRAME#.exr')
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_noice -pr 5 -v 0.76 -ef 2 -l specular -l sss'
cmd += ' -i %s' % img_path
cmd += ' -o %s' % dnz_path
ARNOLD_DENOISE_LAYER = {
    'name': 'arnold_denoise',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['shell'],
    'dependType': Layer.DependType.Layer,
}
#######################################################
# NOTE :
#GENERATE MP4
#############
render_path = os.path.join(shot_path, 'img', 'renders', hipname, 'denoise')
mp4_path = os.path.join(shot_path, 'img', 'renders', hipname + '.mp4')
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' cd %s;' % render_path
cmd += ' . la_cmd mp4;'
cmd += ' cd ..;'
cmd += ' mv %s*.mp4 %s;' % (hipname, mp4_path)
FFMPEG_LAYER = {
    'name': 'generate_videos',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['shell'],
    'dependType': Layer.DependType.Layer
}
#######################################################
# NOTE :
#CLEANUP
########
#ass_dir_to_remove = os.path.dirname(ass_dir)
#cmd = 'rm -r %s;' % ass_dir_to_remove
cmd = 'python /mnt/luma_i/_tools/luma_tools/bin/lab_cmds/la_discord_notify.py %s %s %s;' % (
    user, '"' + shot_name + ' - Render Complete! - ' + comments + '"',
    mp4_path)
CLEANUP_LAYER = {
    'name': 'cleanup_files_and_notify',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_start,
    'cores': '1',
    'services': ['shell'],
    'dependType': Layer.DependType.Layer
}
######################################################################

# JOB ###############################################################
#Default

print('Submitting Default.')
jobData = {
    'name':
    shot_name + '_aov_denoise',
    'shot':
    shot_name + '_' + user,
    'show':
    'inside_job',
    'username':
    user,
    'layers': [
        Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
        Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
        Layer.LayerData.buildFactory(**FFMPEG_LAYER),
        Layer.LayerData.buildFactory(**CLEANUP_LAYER)
    ]}


print('Sending to opencue...')

#SUBMIT #######################

outline = Outline(jobData['name'],
                  shot=jobData['shot'],
                  show=jobData['show'],
                  user=jobData['username'])
layers = []
for layerData in jobData['layers']:
    layer = Shell(layerData.name,
                  command=layerData.cmd.split(),
                  chunk='1',
                  threads=float(layerData.cores),
                  range=str(layerData.layerRange),
                  threadable=True)
    layer.set_service(layerData.services[0])
    layers.append(layer)

layer_count = 0
for layer in layers:
    if layer_count > 0:
        layer.depend_all(layers[layer_count - 1])
    layer_count += 1
    outline.add_layer(layer)

jobs = cuerun.launch(outline, use_pycuerun=False, pause=False)
for job in jobs:
    print(job.name())
    job.setPriority(2)
    job.setMaxCores(1500)
    job.setMaxRetries(10)
print('')
print(colored('Shot successfully submitted to opencue', 'green'))
print('*' * 80 + '\n')
print('')
quit()
