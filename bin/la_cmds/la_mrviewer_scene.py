import sys
import os
import glob

if len(sys.argv) == 2:
    scene = 'sc%03d' % int(sys.argv[1])
    print 'Viewing Mono Scene', scene
    scene_folder = glob.glob('/mnt/luma_i/shots/*/' + scene)
    if len(scene_folder) > 0:
        command = 'mrViewer --edl '
        scene_folder = scene_folder[0]
        for (dirpath, dirnames, filenames) in os.walk(scene_folder):
            for shot in dirnames:
                shot_path = scene_folder + os.sep + shot + os.sep + 'img/camera/*_assembly/mono.*.jpg'
                frame = glob.glob(shot_path)
                if len(frame) > 0:
                    frame = frame[0]
                else:
                    continue
                frame = frame[:-8] + '%04d.jpg '
                command += frame
            break
        os.system(command)

else:
    print "Please specify a scene you want to watch."
    exit()
