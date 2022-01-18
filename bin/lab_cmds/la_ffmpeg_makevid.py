import os
import sys
import glob
from datetime import datetime

# date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
date = os.environ['IJ_DATE']
shot_name = os.environ['IJ_SHOT_NAME']
user = os.environ['IJ_USER']

if len(sys.argv) == 2:
    search_pattern = sys.argv[1].split('.')[0]
    search_extention = sys.argv[1].split('.')[-1]
    search_string = search_pattern + '.*.' + search_extention
    list_of_files = glob.glob(search_pattern + '.*.' + search_extention)
    list_of_files.sort()
    first_frame = int(list_of_files[0].split('.')[1])

    burnin = '"[0:v]drawtext=\'fontcolor=white:font=sans-serif:fontsize=10:x=5:y=5:text=  luma-film - 2020 - inside job %s - %s - %s:box=1:boxborderw=5:boxcolor=black\'[LT]"' % (date, shot_name, user)

    cmd  = 'ffmpeg -y -hide_banner -r 24'
    cmd += ' -start_number %d' % first_frame
    cmd += ' -i %s.%s.%s' % (search_pattern, '%04d', search_extention)
    cmd += ' -s 2048x1152'
    cmd += ' -filter_complex %s' % burnin
    cmd += ' -pix_fmt yuv420p -c:v libx264 -crf 25 -map "[LT]"'
    cmd += ' %s.mp4' % search_pattern
    print cmd

    # os.system( cmd )
else:
    print 'Boo hoo! Please type lab mv [name of any file in sequence]'
