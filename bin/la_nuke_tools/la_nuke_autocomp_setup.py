import os
import sys
import json
import glob
import nuke

if len(sys.argv) is 2:

    print 'Getting details from JSON file...'
    shot_path = os.environ['IJ_SHOT_PATH']
    json_file  = open( os.path.join(shot_path, 'shot_info.json'), 'r' )
    json_data  = json.load( json_file )
    json_file.close()
    frame_start = int(json_data[0]['clip_start'])
    frame_end   = int(json_data[0]['clip_end'])

    nuke_script = sys.argv[1]
    print '\nUpdating script : %s' % nuke_script

    print 'Loading Script...'
    nuke.scriptOpen(nuke_script)
    print 'Success. Carrying on.'

    all_nodes = nuke.allNodes()

    # Disconnect Viewer
    print 'Disconnecting Viewer Nodes... '
    viewers = []
    all_read_nodes = []
    for i in all_nodes:
        if 'Viewer' in i.Class():
            viewers.append(i)
        if 'AUTO_Read' in i.name():
            if 'AUTO_Read_ctl' in i.name():
                pass
            elif 'AUTO_Read_renderCamera' in i.name():
                pass
            else:
                all_read_nodes.append(i)
    for i in viewers:
        print 'Disconnecting %s.' % i.name()
        i.setInput(0, None)
    print 'Done.'

    # Update Root Frame Ranges
    print 'Updating frame range to %04d to %04d.' % (frame_start, frame_end)
    nuke.knob("root.first_frame", str(frame_start))
    nuke.knob("root.last_frame",  str(frame_end))
    print 'Done.'

    # Update Read Nodes
    print 'Finding the latest render folder...'
    renders_path = os.path.join(shot_path, 'img', 'renders')
    render_versions = []
    latest_renders = ''
    dir_listing = os.listdir(renders_path)
    if dir_listing:
        for i in dir_listing:
            if os.path.isdir(os.path.join(renders_path, i)):
                render_versions.append(i)
        render_versions.sort()
        latest_renders = render_versions[-1]
    else:
        print '\tERROR: There are no renders for this shot. Exiting.'
        sys.exit()
    print '\tFound latest renders at: %s.' % latest_renders
    latest_renders_path = os.path.join(renders_path, latest_renders)

    print '\tGetting all the Read Nodes to update...'
    for i in all_read_nodes:
        print '\t\tUpdating %s...' % i.name()
        pass_name = i.name()[10:]
        print '\t\tPass set to %s.' % pass_name
        search_str = os.path.join( latest_renders_path, '**', latest_renders + '-' + pass_name + '.*.exr' )
        pass_files = glob.glob(search_str)
        pass_str = ''
        if pass_files:
            pass_str = pass_files[0]
            pass_str = pass_str.split(shot_path)[1][1:-8] + r'%04d.exr'
        print '\t\tUpdating file path.'
        i['file'].setValue(pass_str)
        i['first'].setValue(frame_start)
        i['last'].setValue(frame_end)
        i['origfirst'].setValue(frame_start)
        i['origlast'].setValue(frame_end)
        print '\t\tDone.'

    # Save
    print 'Saving updated script.'
    nuke.scriptSave(nuke_script)
    print 'Done.'
