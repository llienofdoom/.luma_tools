import sys
import os

if len(sys.argv) != 3:
    print 'Please type either mono(m) or stereo(s) or both(b), followed by the hipfile.'
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
    print 'Opening HIP file...'
    hou.hipFile.load(hip_file_path, suppress_save_prompt=True, ignore_load_warnings=True)
    print 'Done loading file.'
    print 'Updating camera rig HDA...'
    stereo_camera   = hou.node('/obj/ij_stereo_camera_rig')
    stereo_hda_path = stereo_camera.type().definition().libraryFilePath()
    stereo_def      = hou.hda.definitionsInFile(stereo_hda_path)[-1]
    stereo_hda_name = stereo_def.nodeTypeName()
    stereo_camera   = stereo_camera.changeNodeType(stereo_hda_name)
    stereo_camera.matchCurrentDefinition()
    stereo_camera   = hou.node('/obj/ij_stereo_camera_rig')
    print 'Done. Moving along...'

    if ('mono' in sys.argv[1]) or ('m' in sys.argv[1]):
        print 'Exporting Mono preview'
        print '\tJPGS'
        stereo_camera.parm('execute4').pressButton()
        print '\tMP4'
        stereo_camera.parm('execute6').pressButton()
        print '\tCLEANUP'
        stereo_camera.parm('execute7').pressButton()
    elif ('stereo' in sys.argv[1]) or ('s' in sys.argv[1]):
        print 'Exporting Stereo preview'
        print '\tJPGS'
        stereo_camera.parm('execute2').pressButton()
        print '\tMP4'
        stereo_camera.parm('execute').pressButton()
        print '\tCLEANUP'
        stereo_camera.parm('execut5').pressButton()
    elif ('both' in sys.argv[1]) or ('b' in sys.argv[1]):
        print 'Exporting Mono preview'
        print '\tJPGS'
        stereo_camera.parm('execute4').pressButton()
        print '\tMP4'
        stereo_camera.parm('execute6').pressButton()
        print '\tCLEANUP'
        stereo_camera.parm('execute7').pressButton()
        print 'Exporting Stereo preview'
        print '\tJPGS'
        stereo_camera.parm('execute2').pressButton()
        print '\tMP4'
        stereo_camera.parm('execute').pressButton()
        print '\tCLEANUP'
        stereo_camera.parm('execute5').pressButton()
    else:
        exit()
print 'Done.'
