import sys
import os
import glob

if len(sys.argv) == 4:
    scene = 'sc%03d' % int(sys.argv[3])
    print 'Generating Stereo Scene Video', scene
    
    type_of_vid  = ''
    if 'm' in sys.argv[1]:
        type_of_vid = '_mono.mp4'
    elif 's' in sys.argv[1]:
        type_of_vid = '_stereo.mp4'
    else:
        print "Please specify mono(m) or stereo(s), (ass)(cam)(ren), and a scene you want to watch."
        print "ie : lab se s cam 2."
        exit()
    
    type_of_shot = ''
    if 'ass' in sys.argv[2]:
        type_of_shot = 'assembly'
    elif 'cam' in sys.argv[2]:
        type_of_shot = 'camera'
    elif 'ren' in sys.argv[2]:
        type_of_shot = 'render'
    else:
        print "Please specify mono(m) or stereo(s), (ass)(cam)(ren), and a scene you want to watch."
        print "ie : lab se s cam 2."
        exit()
    
    search = '%s/shots/*/%s/*/img/%s/*%s' % (os.environ['JOB'], scene, type_of_shot, type_of_vid)
    list_of_vids = glob.glob(search)
    vid_file_path = os.environ['JOB'] + '/tmp/la_seqedit_files.txt'
    vid_file = open(vid_file_path, 'w')
    path = ''
    if len(list_of_vids) > 0:
        for vid in list_of_vids:
            vid_file.write('file %s\n' % (vid) )
        act  = list_of_vids[0].split('/')[4]
        path = list_of_vids[0][:24] + scene + '/' + act + '_' + scene + '_' + type_of_shot + type_of_vid
    vid_file.close()

    cmd  = 'ffmpeg -y -f concat -safe 0'
    cmd += ' -i %s' % vid_file_path
    cmd += ' -c copy'
    cmd += ' %s' % (path)
    # print cmd
    os.system(cmd)

else:
    print "Please specify mono(m) or stereo(s), (ass)(cam)(ren), and a scene you want to watch."
    print "ie : lab se s cam 2."
    exit()
