import os
import sys
import glob
import json

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
    print '*' * 80
    print '[%04d/%04d] - %s' % (c, num, cur)
    print '*' * 80
    act = cur.split('/')[4][3:].lstrip('0')
    scn = cur.split('/')[5][2:].lstrip('0')
    sht = cur.split('/')[6][2:].lstrip('0')

    end = cur.find('/img')
    ij_shot_path = cur[:end]

    os.environ['IJ_SHOT']      = '%s-%s-%s' % ( cur.split('/')[4][3:], cur.split('/')[5][2:], cur.split('/')[6][2:])
    os.environ['IJ_SHOT_PATH'] = ij_shot_path
    print os.environ['IJ_SHOT'], os.environ['IJ_SHOT_PATH']
    cmd = 'la_cmd shotPrep;'
    os.system(cmd)
    c += 1
    print '\n' * 2
