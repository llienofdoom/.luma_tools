import os
import sys
import glob
import json

# INITIAL #####################################################################
shots_root = '/mnt/luma_i/shots'
list_of_shots = ''
if len(sys.argv) != 4:
    print 'Please type lab mps (m)(s)(b) (ass)(cam)(ren) [ ALL ] or [ ##-###-#### ].'
    exit()
else:
    if 'all' in sys.argv[3].lower():
        path = shots_root + '/act*/sc*/sh*'
        list_of_shots = glob.glob(path)
    else:
        if len(sys.argv[3]) == 11:
            a = 'act' + sys.argv[3].split('-')[0]
            c = 'sc'  + sys.argv[3].split('-')[1]
            s = 'sh'  + sys.argv[3].split('-')[2]
            if '*' in a:
                a = '*'
            if '*' in c:
                c = '*'
            if '*' in s:
                s = '*'
            path = shots_root + '/%s/%s/%s' % (a, c, s)
            list_of_shots = glob.glob(path)
        else:
            print 'Please type lab mps (m)(s)(b) (ass)(cam)(ren) [ ALL ] or [ ##-###-#### ].'
            exit()
num = len(list_of_shots)

c=1
for cur in list_of_shots:
    print '*' * 80
    print '[%04d/%04d] - %s' % (c, num, cur)
    print '*' * 80
    act = cur.split('/')[4][3:]
    scn = cur.split('/')[5][2:]
    sht = cur.split('/')[6][2:]

    hip_type = ''
    if 'ass' in sys.argv[2].lower():
        hip_type = '*assembly.hip'
    if 'cam' in sys.argv[2].lower():
        hip_type = '*camera_*.hip'
    if 'ren' in sys.argv[2].lower():
        hip_type = '*render_*.hip'

    os.environ['IJ_SHOT']      = '%s-%s-%s' % ( act, scn, sht)
    os.environ['IJ_SHOT_PATH'] = cur
    os.environ['IJ_SHOT_NAME'] = 'act%s_sc%s_sh%s' % (act, scn, sht)
    os.chdir(os.environ['IJ_SHOT_PATH'])

    hip_file_search = './%s_%s' % (os.environ['IJ_SHOT_NAME'], hip_type)
    hip_file = glob.glob(hip_file_search)[-1]

    cmd = 'la_cmd mp %s %s;' % (sys.argv[1].lower(), hip_file)
    # print cmd
    os.system(cmd)
    c += 1
    print '\n' * 2
