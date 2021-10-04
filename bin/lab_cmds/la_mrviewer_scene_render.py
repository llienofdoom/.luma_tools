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
        list_of_vids = []
        for (dirpath, dirnames, filenames) in os.walk(scene_folder):
            for shot in dirnames:
                shot_path = scene_folder + os.sep + shot + os.sep + 'img/renders/act*_sc*_sh*_render_v*.mp4'
                vid = glob.glob(shot_path)
                if len(vid) > 0:
                    vid = vid[-1]
                    list_of_vids.append(vid)
                else:
                    continue
            break
        list_of_vids.sort()

        for i in list_of_vids:
            print 'Picked %s' % i
            command += ' %s' % i
        os.system(command)

else:
    print "Please specify a scene you want to watch."
    exit()
