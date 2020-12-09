import sys
import os
import glob

if len(sys.argv) == 2:
    scene = 'sc%03d' % int(sys.argv[1])
    print 'Generating Stereo Scene Video', scene
    list_of_vids = glob.glob('/mnt/luma_i/shots/*/' + scene + '/*/img/camera/*_stereo.mp4')
    vid_file_path = os.environ['JOB'] + '/tmp/la_seqedit_files.txt'
    vid_file = open(vid_file_path, 'w')
    if len(list_of_vids) > 0:
        for vid in list_of_vids:
            vid_file.write('file %s\n' % (vid) )
    vid_file.close()

    cmd  = 'ffmpeg -y -f concat -safe 0'
    cmd += ' -i %s' % vid_file_path
    cmd += ' -c copy'
    cmd += ' %s' % (os.environ['JOB'] + '/tmp/' + scene + '_stereo.mp4')
    # print cmd
    os.system(cmd)

else:
    print "Please specify a scene you want to watch."
    exit()
