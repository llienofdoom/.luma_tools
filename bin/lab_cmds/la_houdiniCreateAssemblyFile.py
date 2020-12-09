import sys
import os

if os.environ['IJ_OS'] == 'mac':
    hfs = '/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources'
if os.environ['IJ_OS'] == 'lin':
    hfs = '/opt/houdini/hfs18.5.351'

sys.path.append(hfs + "/houdini/python%d.%dlibs" % sys.version_info[:2])
import hou

root = os.path.dirname(hou.hipFile.path())
bits = os.environ['IJ_SHOT'].split('-')
name = 'act%s_sc%s_sh%s_assembly.hip' % (bits[0], bits[1], bits[2])
hip_file_path = root + os.sep + name
print '*' * 80
# if os.path.exists(hip_file_path):
#     do_it = raw_input('File already exists. Do you want to overwrite? (y|n) : ')
#     if 'y' in do_it:
#         print 'Overwriting...'
#     else:
#         exit()

print 'Building scene...'
shot_builder_hda  = '/mnt/luma_i/assets/gen/tools/shot_builder_hda/ij_shot_builder.hda'
stereo_camera_rig = '/mnt/luma_i/assets/gen/tools/stereo_camera_rig/ij_stereo_camera_rig.hda'

hou.hda.installFile(shot_builder_hda)
hou.hda.installFile(stereo_camera_rig)

shot_builder  = hou.node('/obj').createNode('luma::ij_shot_builder', 'ij_shot_builder')
shot_builder.moveToGoodPosition()
stereo_camera = hou.node('/obj').createNode('luma::ij_stereo_camera_rig', 'ij_stereo_camera_rig')
stereo_camera.moveToGoodPosition()

print 'Loading data...'
shot_builder.parm('build').pressButton()
stereo_camera.parm('shot_builder').set(shot_builder.path())

print 'Saving HIP file...'
hou.hipFile.save(hip_file_path)

# print 'Exporting Mono View'
# stereo_camera.parm('execute4').pressButton()

# print 'Exporting Stereo View'
# stereo_camera.parm('execute2').pressButton()

print 'Done.'