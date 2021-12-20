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
print('*' * 80)
print('IJ SCENE SUBMITTER')
print('CURRENT ACT: ' + currentact)
print('CURRENT SCENE: ' + currentscene)
print('*' * 80)
print('')

allowcopy = raw_input('Save up version? (Y/N)')
sceneinfo = raw_input('show info only? (Y/N)')
final = raw_input('force final render settings? (Y/N)')
environment = raw_input(
    'Render only one environment?. (enter env name, empty for all): ')
specific = raw_input('Specific shot?. (enter shot no, empty for all): ')

print('Using current scene.')
a = currentact
c = currentscene
s = '*'

path = shots_root + '/%s/%s/%s' % (a, c, s)
list_of_shots = glob.glob(path)
list_of_shots.sort
num = len(list_of_shots)
c = 1

#warning/debug variables
nohip = []
foundhip = []
noenv = []
envlist = []
sciencetest = []

#############################
#SUBMISSION
###################################################################

#Run scene submitter for every shot found

for cur in list_of_shots:

    #init
    print('')
    print('*' * 80)
    print(colored('[shot %04d of %04d] - %s' % (c, num, cur), 'blue'))

    act = cur.split('/')[4][3:]
    scn = cur.split('/')[5][2:]
    sht = cur.split('/')[6][2:]

    hip_type = '*render_*.hip'
    hip_file = ''

    #SET SCENE
    os.environ['IJ_SHOT'] = '%s-%s-%s' % (act, scn, sht)
    os.environ['IJ_SHOT_PATH'] = cur
    os.environ['IJ_SHOT_NAME'] = 'act%s_sc%s_sh%s' % (act, scn, sht)
    os.chdir(os.environ['IJ_SHOT_PATH'])

    #import data from JSON file
    try:
        json_file = open(
            os.path.join(os.environ['IJ_SHOT_PATH'], 'shot_info.json'), 'r')
        json_data = json.load(json_file)[0]
        json_file.close()
    except:
        noenv.append(cur)
        print('JSON file missing or invalid.')

    render_set = json_data['assets']['env']

    if type(render_set) == list:
        render_set = render_set[0]

    if render_set == 'NaN':
        noenv.append(cur)
    print('enviro:' + environment)

    if environment:
        print('doing individual env')
        if not environment in render_set:
            print('skipping..')
            continue
        else:
            print('doing that other thing')

    if specific:
        print('doing individual shot')
        if not specific in cur:
            print(specific)
            print(cur)
            print('skipping..')
            continue
        else:
            print('doing that other thing')

    envlist.append(cur + '' + str(render_set))

    # debug variables for env cehcking
    if 'extschoolentrance' in render_set:
        mode = 0
    elif 'normanstreet' in render_set:
        mode = 0
    elif 'scienceclassroom' in render_set:
        mode = 1
    elif 'normanbedroom' in render_set:
        mode = 1
    elif 'normanentrance' in render_set:
        mode = 1
    elif 'sciencehallway' in render_set:
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
    else:
        mode = 0

    print('Environment in shot: ', render_set)
    print('')
    print('')

    #FIND HIP FILES
    hip_file_search = './%s_%s' % (os.environ['IJ_SHOT_NAME'], hip_type)
    hip_file = glob.glob(hip_file_search)

    #CHECK FOR NO FILES
    if len(hip_file) < 1:
        print(colored('No valid render file found.', 'red'))
        print('*' * 80 + '\n')
        print('')
        nohip.append(cur)
        continue

    #SORT NUMERICALLY
    hip_file = sorted(hip_file)
    hip_filenew = hip_file[-1]

    print('Total render hip files: ' + str(len(hip_file)))

    #Found render files
    if len(hip_file) > 0:
        foundhip.append(cur)
        hip_file = hip_file[-1].split('.')[1]
        hipfile = (cur) + (hip_file) + '.hip'
        hipname = hip_file.split('/')[1]
        print('')
        print('Latest render file found: ' + (cur) + (hip_file) + '.hip')
        print('Render mode: ' + str(mode))
        print('')

        #SAVE UP VERISION
        for file in hip_file:
            fileorig = hipfile
            file = fileorig.split('.')[0]
            file = file.split('_')[5]
            file = file.split('v')[1]
            version = int(file)
            version += 1

        #rebuild hip path string
        newstr = fileorig
        newstr = newstr.split('_')[0] + '_' + newstr.split(
            '_')[1] + '_' + newstr.split('_')[2] + '_' + newstr.split(
                '_')[3] + '_' + newstr.split('_')[4] + '_v' + str(
                    version).zfill(2) + '.hip'

        #create command
        copycmd = 'cp ' + fileorig + ' ' + newstr

        #Check if copying is allowed
        if allowcopy != 'N' and allowcopy != 'n':
            print('Saving up version enabled.')
            try:
                #Copy if allowed
                print('Saving up version....')
                print('Creating new file....')
                print('New hip file name: ' + newstr)
                os.system(copycmd)
                newhipname = newstr.split('/')[7]
                hipfile = (cur) + '/' + newhipname
                hipname = newhipname
                print(colored('Copy succesful! continuing...', 'green'))
                print('')
            except:
                print('error copying new file.')
                print('')
        else:
            print('Saving up version disabled.')
            print('')
        #######################################################################################################
        #Run submission script for shot

        if sceneinfo != "Y" and sceneinfo != "y":
            print('Starting render submission....')
            os.system(
                "python ~/.luma_tools/bin/lab_cmds/la_submit_shot_default.py "
                + hipfile + " " + final)
        else:
            print("showing info only")

        c += 1
        print('')

    else:
        continue
print('#' * 80)
print('###FINISHED###')
print('#' * 80 + '\n')

#list submitted
print(colored('The following shots were submitted:. ', 'blue'))
print('')
foundhip = sorted(foundhip)
for i in range(len(foundhip)):
    print(colored(foundhip[i], 'yellow'))

#Missing HIP files warning
if c != num:
    missing = num - (c - 1)
    print(colored(
        'WARNING: \n Not all shots submitted. \n A total of ' + str(missing) +
        ' shots do not have valid render hip files:. ', 'yellow'))
    print('')
    for i in range(len(nohip)):
        print(colored(nohip[i], 'red'))
else:
    print(colored('All shots sucessfully submitted.', 'green'))
    print('')
print('')

#Invalid JSON warning
if len(noenv) > 0:
    print(colored(
        'WARNING: \n The following shots have no env in json file or json file missing:',
        'yellow'))
    print('')
    for i in range(len(noenv)):
        print(colored(noenv[i], 'red'))
print('')
print(colored('Scene submission complete!', 'green'))
