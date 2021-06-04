import os
import sys
import glob
import shutil

job_root = os.environ['IJ_LUMA_PROJ_ROOT']
edit_sources_master = os.path.join(job_root, 'editorial', 'edit_sources_master')
shot_root = os.path.join(job_root, 'shots')

def usage():
    print 'usage : lab eus [a|f|m|s|r|c] [ALL|ME|**-***-****]'
    print 'a:animatic | f:animation | m:mono | s:stereo | r:render | c:comp'

if len(sys.argv) != 3:
    usage()
    sys.exit()
else:
    print 'Doing it! Finding all files...'
    update_type = sys.argv[1]
    update_shot = sys.argv[2]
    if 'all' in update_shot.lower():
        update_shot = '**-***-****'
    if 'me' in update_shot.lower():
        update_shot = os.environ['IJ_SHOT']
    update_shot = update_shot.split('-')
    for i in range(0, len(update_shot)):
        if '*' in update_shot[i]:
            update_shot[i] = '*'
    
    if 'a' in update_type.lower():
        update_type = 'animatic'
    elif 'f' in update_type.lower():
        update_type = 'flip'
    elif 'm' in update_type.lower():
        update_type = 'mono'
    elif 's' in update_type.lower():
        update_type = 'stereo'
    elif 'r' in update_type.lower():
        update_type = 'render'
    elif 'c' in update_type.lower():
        update_type = 'comp'
    else:
        sys.exit()

    filename = '*.mp4'
    if update_type == 'flip':
        filename = '*animation*.mp4'
    shot_search_string = os.path.join( shot_root, 'act%s' % update_shot[0], 'sc%s' % update_shot[1], 'sh%s' % update_shot[2], 'img', update_type, filename )
    list_of_shot_videos = glob.glob( shot_search_string )
    print 'Done. Sorting files into latest...'
    
    list_of_shot_videos.sort()
    list_of_uniques = []
    for i in range(0, len(list_of_shot_videos)):
        current = os.path.basename(list_of_shot_videos[i])
        nextone = ''
        if i < len(list_of_shot_videos) - 1:
            nextone = os.path.basename(list_of_shot_videos[i + 1])
            if current[:18] not in nextone:
                print 'adding', list_of_shot_videos[i]
                list_of_uniques.append(list_of_shot_videos[i])
        if i == len(list_of_shot_videos) - 1:
            print 'adding', list_of_shot_videos[i]
            list_of_uniques.append(list_of_shot_videos[i])
    print 'Done! Processing Remaining...'

    for i in list_of_uniques:
        if update_type == 'flip':
            update_type = 'animation'
        act = os.path.basename(i).split('_')[0]
        scn = os.path.basename(i).split('_')[1]
        sht = os.path.basename(i).split('_')[2]
        new_name = '%s_%s_%s' % (act, scn, sht)
        new_path = os.path.join(edit_sources_master, update_type, new_name)
        print '\tUpdating %s' % new_path
        print '\tCopying mp4...'
        print i, new_path + '.mp4'
        shutil.copy2(i, new_path + '.mp4')
        print '\tDone! Converting to ProRes...'
        cmd  = 'ffmpeg -y -hide_banner -loglevel panic'
        # cmd  = 'ffmpeg -y'
        cmd += ' -i %s' % i
        cmd += ' -c:v prores_ks -profile:v 3 -qscale:v 5 -vendor ap10 -pix_fmt yuv422p10le'
        cmd += ' %s' % new_path + '.mov'
        os.system( cmd )
        print '\tDone! On the the next one!'

print 'Done Updating %s videos for %s-%s-%s-! Exiting.' % (update_type, update_shot[0], update_shot[1], update_shot[2])
