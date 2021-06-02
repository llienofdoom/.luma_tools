import os
import sys
import glob
import shutil

if len(sys.argv) == 3:
    edit_sources_path = '/mnt/luma_i/editorial/edit_sources_master'
    search_path = '/mnt/luma_i/shots/act*/'
    search_type = ''
    if 'all' in sys.argv[2].lower():
        print 'Doing all...'
        search_path += 'sc*'
    else:
        print 'Doing scene %d...' % int(sys.argv[2])
        search_path += 'sc%03d' % int(sys.argv[2])
    search_path += '/sh*/img'

    if 'a' in sys.argv[1]:
        print 'Doing Animatics...'
        search_path += '/animatic'
        search_type = 'animatic'
    elif 'f' in sys.argv[1]:
        print 'Doing Anim Flip Files...'
        search_path += '/flip'
        search_type = 'animation'
    elif 'm' in sys.argv[1]:
        print 'Doing Mono Assembly...'
        search_path += '/camera'
        search_type = 'mono'
    elif 's' in sys.argv[1]:
        print 'Doing Stereo Assembly...'
        search_path += '/camera'
        search_type = 'stereo'
    elif 'r' in sys.argv[1]:
        print 'Doing Render Output...'
        search_path += '/renders'
        search_type = 'render'
    elif 'c' in sys.argv[1]:
        print 'Doing Comp Output...'
        search_path += '/comp'
        search_type = 'comp'
    else:
        print 'Boo Hoo! Please type lab eus [a|f|m|s|r|c] [SCENE NUMBER or ALL]'
        exit()

    print 'Looking in %s...' % search_path
    search_path += '/act*_sc*_sh*_%s.mp4' % search_type
    video_files  = glob.glob(search_path)
    if len(video_files) != 0:
        for vid in video_files:
            print 'Updating %s...' % vid,
            # print 'To %s/' % new_path
            old_name = os.path.basename(vid)
            parts    = old_name.split('_')
            new_name = '%s_%s_%s.mp4' % (parts[0], parts[1], parts[2])
            new_path = edit_sources_path + '/' +  search_type + '/' + new_name
            shutil.copyfile(vid, new_path)
            print 'Done.'
else:
    print 'Boo Hoo! Please type lab eus [a|f|m|s|r|c] [SCENE NUMBER or ALL]'
