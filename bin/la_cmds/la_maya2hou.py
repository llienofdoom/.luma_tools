import os
import sys
import glob
import json
import subprocess

# INITIAL #####################################################################
shots_root = '/mnt/luma_i/shots'
list_of_shots = ''
if len(sys.argv) != 2:
    print 'Please specify either [ ALL ] or [ ##-###-#### ].'
    exit()
else:
    if 'all' in sys.argv[1].lower():
        list_of_shots = glob.glob(shots_root + '/*/*/*/img/animatic/*.mp4')
    else:
        if len(sys.argv[1]) == 11:
            a = 'act' + sys.argv[1].split('-')[0]
            c = 'sc'  + sys.argv[1].split('-')[1]
            s = 'sh'  + sys.argv[1].split('-')[2]
            if '*' in a:
                a = '*'
            if '*' in c:
                c = '*'
            if '*' in s:
                s = '*'
            path = shots_root + '/%s/%s/%s/img/animatic/*.mp4' % (a, c, s)
            list_of_shots = glob.glob(path)
        else:
            print 'Please specify either [ ALL ] or [ ##-###-#### ].'
            exit()
num = len(list_of_shots)

c=1
for cur in list_of_shots:
    act = cur.split('/')[4][3:].lstrip('0')
    scn = cur.split('/')[5][2:].lstrip('0')
    sht = cur.split('/')[6][2:].lstrip('0')

    cmd = 'la_cmd ss %s-%s-%s;' % (act, scn, sht)
    # os.system(cmd)
    subprocess.call( cmd, shell=True )
    cmd = 'la_cmd shotPrep;'
    # os.system(cmd)
    subprocess.call( cmd, shell=True )
