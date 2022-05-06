from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from termcolor import colored
import os
import site
import sys
import json
import glob
import re

#############################
#GET SHOTLIST
###################################################################

#init
shots_root = '/mnt/luma_i/shots'
list_of_shots = ''
shot_name = os.environ['IJ_SHOT_NAME']
shot_path = os.environ['IJ_SHOT_PATH']
currentact = shot_name.split('_')[0]
currentscene = shot_name.split('_')[1]

print('Using current scene.')
a = currentact
c = currentscene
s = shot_name

path = shots_root + '/%s/%s/%s' % (a, c, s)


#FIND HIP FILES
act = path.split('/')[4][3:]
scn = path.split('/')[5][2:]
sht = path.split('/')[6][2:]

hip_type = '*render_*.hip'
hip_file = ''

#SET SCENE
hip_file_search = './%s_%s' % (os.environ['IJ_SHOT_NAME'], hip_type)
hip_file = glob.glob(hip_file_search)

#CHECK FOR NO FILES
if len(hip_file) < 1:
    print(colored('No valid render file found.', 'red'))
    print('*' * 80 + '\n')
    print('')

hip_file = sorted(hip_file)
hip_filenew = hip_file[-1]

print('Total render hip files: ' + str(len(hip_file)))

#Found render files
if len(hip_file) > 0:
    hip_file = hip_file[-1].split('.')[1]
    hipfile = (path) + (hip_file) + '.hip'
    hipname = hip_file.split('/')[1]
    print('')
    print('Latest render file found: ' + (path) + (hip_file) + '.hip')
    print('')

print('Running Denoise Submission with AOVS')

os.system('python /home/christophe/.luma_tools/bin/la_houdini_tools/la_houdini_submit_denoise_only.py' + " " + hipfile)