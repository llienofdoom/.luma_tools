import os
import sys
import glob

if len(sys.argv) == 2:
    search_pattern = sys.argv[1].split('.')[0]
    search_extention = sys.argv[1].split('.')[-1]
    search_string = search_pattern + '.*.' + search_extention
    list_of_files = glob.glob(search_pattern + '.*.' + search_extention)
    list_of_files.sort()
    first_frame = int(list_of_files[0].split('.')[1])

    cmd  = 'ffmpeg -y -hide_banner -r 24'
    cmd += ' -start_number %d' % first_frame
    cmd += ' -i %s.%s.%s' % (search_pattern, '%04d', search_extention)
    cmd += ' -pix_fmt yuv420p -c:v libx264 -crf 25'
    cmd += ' %s.mp4' % search_pattern

    os.system( cmd )
else:
    print 'Boo hoo! Please type lab mv [name of any file in sequence]'
