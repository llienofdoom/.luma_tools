#!/usr/bin/env python3
import os
import glob
import datetime
import shutil


# GLOBALS
root_of_ij = os.environ['IJ_LUMA_PROJ_ROOT']
root_of_latest_movs = os.path.join(root_of_ij, 'editorial', 'edit_sources_master', '_latest_shot_mov')



################################################################################
def getListOfAllShots():
    print('  Getting a list of all viable shots...')
    list_of_shots = glob.glob( os.path.join(root_of_ij, 'shots', 'act*', 'sc*', 'sh*'))
    list_of_shots.sort()
    print('  Done. Found {} shots to process.'.format(len(list_of_shots)))
    return list_of_shots



################################################################################
def findLatestVideo(shot_root):
    list_of_vids_to_check = []
    very_latest_video = ''
    types_of_vids = ['flip', 'renders', 'comp']
    # Find Vids
    for type_of_vid in types_of_vids:
        search_path = os.path.join(shot_root, 'img', type_of_vid)
        if os.path.exists(search_path):
            # print('      Found {} folder at {}.'.format(type_of_vid, search_path))
            ext = 'mp4'
            if type_of_vid == 'comp':
                ext = 'mov'
            list_of_videos = glob.glob( os.path.join( search_path, '*.' + ext ) )
            if list_of_videos:
                list_of_videos.sort()
                # print('        Found {} videos.'.format(len(list_of_videos)))
                latest_video = list_of_videos[-1]
                # print('        Latest {} found at {}.'.format(type_of_vid, latest_video))
                list_of_vids_to_check.append(latest_video)
            # else:
                # print('        Did NOT find any videos. SKIPPING.')
        # else:
            # print('      Did NOT find {} folder at {}. SKIPPING.'.format(type_of_vid, search_path))
    # Check times
    if list_of_vids_to_check:
        latest_date = 0
        print('      Checking modification dates:')
        for vid in list_of_vids_to_check:
            mod_time = os.path.getmtime(vid)
            print('        {} - {}.'.format(os.path.basename(vid),datetime.datetime.fromtimestamp(mod_time)))
            if mod_time > latest_date:
                latest_date = mod_time
                very_latest_video = vid
        if latest_date > 0:
            print('        Found Latest Video:')
            print('        DATE = {} \t VIDEO = {}'.format(datetime.datetime.fromtimestamp(latest_date), os.path.basename(very_latest_video)))
            return very_latest_video
    else:
        print('      No vids to check. SKIPPING.')
        return ''



################################################################################
def transcodeVideo(in_vid):
    out_vid = in_vid[:-3] + 'mov'
    print('        Output Video = {}'.format(out_vid))
    cmd  = 'ffmpeg -y -hide_banner -loglevel panic'
    cmd += ' -i %s' % in_vid
    cmd += ' -c:v prores_ks -profile:v 3 -qscale:v 5 -vendor ap10 -pix_fmt yuv422p10le'
    cmd += ' %s' % out_vid
    # print(cmd)
    print('        Encoding...')
    try:
        os.system( cmd )
        print('        Encoding complete.')
    except Exception as e:
        print('ERROR')
        print(e)
    return out_vid



################################################################################
def iterateOverShots(list_of_shots):
    print('  Iterating over shots.')
    for i in range(0, len(list_of_shots)):
    # for i in range(0, 2):
        current_shot = list_of_shots[i]
        print()
        print()
        print('    --------')
        print('    Checking {}'.format(current_shot))
        latest_vid = findLatestVideo(current_shot)
        if latest_vid:
            print('    Checking Done. Processing...')
            print('      Using {} as source.'.format(latest_vid))
            if 'comp' in os.path.basename(latest_vid):
                print('      Not Transcoding.')
            else:
                print('      Transcoding first.')
                latest_vid = transcodeVideo(latest_vid)
            print('    Copying file to edit bin...')
            source_video = latest_vid
            shot_name = current_shot[18:].replace('/', '_') + '.mov'
            dest_video = os.path.join( root_of_latest_movs, shot_name )
            print('      SOURCE = {}.'.format(source_video))
            print('      DEST   = {}.'.format(dest_video))
            # TODO : COPY FILES
            try:
                shutil.copy2(source_video, dest_video)
                print('    Shot Updated.')
            except Exception as e:
                print('ERROR')
                print(e)
            print('    --------')



################################################################################
def main():
    print('\nCollecting Latest Renders for Edit...')
    print('Starting')
    print('*'*80)
    print()

    list_of_shots = getListOfAllShots()
    iterateOverShots(list_of_shots)
    print()

################################################################################
if __name__=='__main__':
    main()
