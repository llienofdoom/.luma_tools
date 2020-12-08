import sys
import os

if len(sys.argv) != 3:
    print 'Please type either mono or stereo, followed by the hipfile.'
    exit()

if os.environ['IJ_OS'] == 'mac':
    hfs = '/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources'
if os.environ['IJ_OS'] == 'lin':
    hfs = '/opt/houdini/hfs18.5.351'

sys.path.append(hfs + "/houdini/python%d.%dlibs" % sys.version_info[:2])
import hou

root = os.path.dirname(hou.hipFile.path())
bits = os.environ['IJ_SHOT'].split('-')
# name = 'act%s_sc%s_sh%s_assembly.hip' % (bits[0], bits[1], bits[2])
name = sys.argv[2]
hip_file_path = root + os.sep + name
print '*' * 80
if os.path.exists(hip_file_path):
    if ('mono' in sys.argv[1]) or ('m' in sys.argv[1]):
        print 'Exporting MONO view...'
        print 'Opening HIP file...'
        hou.hipFile.load(hip_file_path, suppress_save_prompt=True, ignore_load_warnings=True)
        print 'Exporting Mono View'
        stereo_camera = hou.node('/obj/ij_stereo_camera_rig')
        stereo_camera.parm('execute4').pressButton()
        stereo_camera.parm('execute6').pressButton()
        stereo_camera.parm('execute7').pressButton()

    elif ('stereo' in sys.argv[1]) or ('s' in sys.argv[1]):
        print 'Exporting STEREO view...'
        print 'Opening HIP file...'
        hou.hipFile.load(hip_file_path, suppress_save_prompt=True, ignore_load_warnings=True)
        print 'Exporting Stereo View'
        stereo_camera = hou.node('/obj/ij_stereo_camera_rig')
        print 'Exporting MP4...'
        stereo_camera.parm('execute2').pressButton()
        stereo_camera.parm('execute').pressButton()
        stereo_camera.parm('execut5').pressButton()
    else:
        exit()

print 'Done.'
