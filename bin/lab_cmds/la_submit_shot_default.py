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

comments = 'Full Scene Render'

shot_name = os.environ['IJ_SHOT_NAME']
shot_path = os.environ['IJ_SHOT_PATH']
user = os.environ['IJ_USER']
hipfile = sys.argv[1]
print('Render hip: ' + hipfile)
hipname = hipfile.split('/')[-1].split('.')[0]
final = sys.argv[2]
night = sys.argv[3]

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
render_set = json_data['assets']['env']
if type(render_set) == list:
    render_set = render_set[0]
currentjobname = shot_name + '_render'
mode = 0

if 'extschoolentrance' in render_set:
    mode = 1
elif 'normanstreet' in render_set:
    mode = 1
elif 'betelgeuse' in render_set:
    mode = 1          
elif 'scienceclassroom' in render_set:
    mode = 1
elif 'normanbedroom' in render_set:
    mode = 1
elif 'normanentrance' in render_set:
    mode = 1
elif 'sciencehallway' in render_set:
    if night != "N" and night != "n":
        print("its night time!")
        mode = 1
    else:
        mode = 0
elif 'brain' in render_set:
    mode = 3
elif 'airlock' in render_set:
    mode = 1
elif 'nailbridge' in render_set:
    mode = 5
elif 'props' in render_set:
    mode = 1
elif 'girlsbathroom' in render_set:
    mode = 2
elif 'witheringoffice' in render_set:
    mode = 1     
else:
    mode = 0

print('Render mode: ' + str(mode))
###########
#Determine scene

# LAYERS ############################################################
#######################################################
#we now build all layers regardless, only choosing layers on submission
###################################################################################################
######################  EXPORT SHOT STATIC ################################################

cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_hython /mnt/luma_i/_tools/luma_tools/bin/la_houdini_tools/la_houdini_exportstaticcache.py'
cmd += ' %s' % hipfile
cmd += ' #ZFRAME#'
HOUDINI_EXPORT_STATIC_CACHE_LAYER = {
    'name': 'houdini_export_static_cache',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    # 'layerRange': f_start,
    'cores': '8',
    'services': ['houdini']
}

###################################################################################################
######################  EXPORT ASS FILES FOR RENDER ################################################
# NOTE :
# la_hython /home/neill/.luma_tools/bin/la_houdini_tools/la_houdini_exportassforrender.py act00_sc999_sh0010_render_v01.hip 0005
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_hython /mnt/luma_i/_tools/luma_tools/bin/la_houdini_tools/la_houdini_exportass_v02.py'
cmd += ' %s' % hipfile
cmd += ' #ZFRAME#'
cmd += ' %s' % str(mode)
cmd += ' %s' % str(final)
cmd += ' %s' % str(shot_name)
HOUDINI_EXPORT_LAYER = {
    'name': 'houdini_export_ass_files',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['houdini'],
    'dependType': Layer.DependType.Layer,
}
#######################################################
# NOTE :
# MAIN
# #######
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_main.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_MAIN_LAYER = {
    'name': 'arnold_render_ass_files_main',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}
#######################################################
# NOTE :
#Volume
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_volume.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_VOLUME_LAYER = {
    'name': 'arnold_render_ass_files_volume',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
# NOTE :
#Volume_A_BRAIN
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_volume_a.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_VOLUME_A_LAYER = {
    'name': 'arnold_render_ass_files_volume_a',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
# NOTE :
#Volume_B_BRAIN
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_volume_b.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_VOLUME_B_LAYER = {
    'name': 'arnold_render_ass_files_volume_b',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
# NOTE :
#mirror
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_mirror.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_MIRROR_LAYER = {
    'name': 'arnold_render_ass_files_mirror',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}
#crypto
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_cryptomatte.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_CRYPTO_LAYER = {
    'name': 'arnold_render_ass_files_crypto',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
# NOTE :
#FLOATIES_BRAIN
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ar_floaties.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_FLOATIES_LAYER = {
    'name': 'arnold_render_ass_files_floaties',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
#######################################################
# NOTE :
#SHIPEXTRA
########
ass_dir = os.path.join(
    '/mnt/luma_i/tmp/ass_files', hipname,
    hipname + '-rop_ship_aovs.#ZFRAME#.ass.gz'
)  # '/mnt/luma_i/tmp/ass_files/act00_sc000_sh0040_render_v07'
cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
cmd += ' la_kick -i'
cmd += ' %s' % ass_dir
ARNOLD_RENDER_SHIPEXTRA = {
    'name': 'arnold_render_ass_files_shipextra',
    'layerType': JobTypes.JobTypes.SHELL,
    'cmd': cmd,
    'layerRange': f_range,
    'cores': '8',
    'services': ['arnold'],
    'dependType': Layer.DependType.Frame,
}

#######################################################
# NOTE :
# LENTIL FIX OF DEATH
# #######

img_path = os.path.join(shot_path, 'img', 'renders', hipname,
                        hipname + '-rop_ar_main.#ZFRAME#.exr')
cp_path = os.path.join(shot_path, 'img', 'renders', hipname, "lentil",
                       hipname + '-rop_ar_main.#ZFRAME#.exr')
try:
    os.makedirs(os.path.join(shot_path, 'img', 'renders', hipname, 'lentil'))
    #shutil.move(img_path,cp_path)
except:
    pass

cmd = 'source /mnt/luma_i/_tools/luma_tools/env/ij_bashrc;'
#cmd += 'oiiotool %s --attrib "arnold/aovs/RGBA/filter" "RGBA" --attrib "arnold/aovs/variance/filter" "variance_filter" -o %s' %(cp_path,img_path)
cmd += ' python /home/christophe/.luma_tools/bin/lab_cmds/la_lentilfix.py'
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
if mode == 0:
    print('Submitting Default.')
    jobData = {
        'name':
        hipname + '_scene_render',
        'shot':
        shot_name + '_' + user,
        'show':
        'inside_job',
        'username':
        user,
        'layers': [
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_STATIC_CACHE_LAYER),
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MAIN_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_CRYPTO_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
            Layer.LayerData.buildFactory(**FFMPEG_LAYER),
            Layer.LayerData.buildFactory(**CLEANUP_LAYER)
        ]
    }

#Include volume
elif mode == 1:
    print('Submitting Include Volume.')
    jobData = {
        'name':
        hipname + '_scene_render',
        'shot':
        shot_name + '_' + user,
        'show':
        'inside_job',
        'username':
        user,
        'layers': [
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_STATIC_CACHE_LAYER),
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MAIN_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_VOLUME_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_CRYPTO_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
            Layer.LayerData.buildFactory(**FFMPEG_LAYER),
            Layer.LayerData.buildFactory(**CLEANUP_LAYER)
        ]
    }

#bathroom
elif mode == 2:
    print('Submitting Bathroom.')
    jobData = {
        'name':
        hipname + '_scene_render',
        'shot':
        shot_name + '_' + user,
        'show':
        'inside_job',
        'username':
        user,
        'layers': [
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_STATIC_CACHE_LAYER),
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MAIN_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MIRROR_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_VOLUME_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_CRYPTO_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
            Layer.LayerData.buildFactory(**FFMPEG_LAYER),
            Layer.LayerData.buildFactory(**CLEANUP_LAYER)
        ]
    }

#brain
elif mode == 3:
    print('Submitting Brain.')
    jobData = {
        'name':
        hipname + '_scene_render',
        'shot':
        shot_name + '_' + user,
        'show':
        'inside_job',
        'username':
        user,
        'layers': [
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_STATIC_CACHE_LAYER),
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MAIN_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_VOLUME_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_VOLUME_A_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_VOLUME_B_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_FLOATIES_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_CRYPTO_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
            Layer.LayerData.buildFactory(**FFMPEG_LAYER),
            Layer.LayerData.buildFactory(**CLEANUP_LAYER)
        ]
    }

#SPF
elif mode == 5:
    print('Submitting SPF.')
    jobData = {
        'name':
        hipname + '_scene_render',
        'shot':
        shot_name + '_' + user,
        'show':
        'inside_job',
        'username':
        user,
        'layers': [
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_STATIC_CACHE_LAYER),
            Layer.LayerData.buildFactory(**HOUDINI_EXPORT_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_MAIN_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_SHIPEXTRA),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_CRYPTO_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_RENDER_LENTIL_LAYER),
            Layer.LayerData.buildFactory(**ARNOLD_DENOISE_LAYER),
            Layer.LayerData.buildFactory(**FFMPEG_LAYER),
            Layer.LayerData.buildFactory(**CLEANUP_LAYER)
        ]
    }

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
layerData = jobData['layers']
for layer in layers:
    if layer_count > 0:
        if layerData[layer_count].dependType == 'Layer':

            if 'arnold_denoise' in str(layer):
                layer.depend_all(layers[layer_count - 1])
                print(str(layer) + ' is layer')

            if 'arnold_lentil_fix' in str(layer):
                layer.depend_all(layers[2])
            else:
                layer.depend_all(layers[layer_count - 1])
                print(str(layer) + ' is layer')

        if layerData[layer_count].dependType == 'Frame':
            if 'arnold_render_ass_files_volume' in str(
                    layer) or 'arnold_render_ass_files_crypto' in str(layer):
                layer.depend_on(layers[1])
                print(str(layer) + ' is FRAME')
            else:
                layer.depend_on(layers[layer_count - 1])
                print(str(layer) + ' is FRAME')
    layer_count += 1
    outline.add_layer(layer)

jobs = cuerun.launch(outline, use_pycuerun=False, pause=True)
for job in jobs:
    print(job.name())
    job.setPriority(priority)
    job.setMaxCores(1500)
    job.setMaxRetries(10)
print('')
print(colored('Shot successfully submitted to opencue', 'green'))
print('*' * 80 + '\n')
print('')
quit()
