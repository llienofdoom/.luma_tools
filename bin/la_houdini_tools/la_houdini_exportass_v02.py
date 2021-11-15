#####################################################################
# H:\_distros\hfs.windows-x86_64_16.5.473\bin\hython.exe
# H:\_distros\_lumatools\lumatools\luma_houdiniHythonRender.py
# -h X:\_studiotools\TMP\HQ\mantra_test\mantra_test_103.hip
# -r "/out/rop_hm_base"
# -fs 1
# -fe 10
#####################################################################

import sys
import os
import time
from types import MethodDescriptorType
import hou

hipfile = sys.argv[1]
frame = int(sys.argv[2])
mode = int(sys.argv[3])

print 'Exporting ASS files to render, from %s.' % hipfile
print 'Doing frame %04d.' % frame

time_start = time.time()
print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"
time_end = time.time() - time_start
print 'Scene loading took %d seconds.' % (time_end + 1)

print 'Setting settings...'
hou.parm('/obj/ij_stereo_camera_rig/ar_skip_license_check').set(0)
hou.parm('/obj/ij_stereo_camera_rig/enable_volumes').set(0)
hou.parmTuple('/obj/ij_stereo_camera_rig/f').deleteAllKeyframes()
hou.parm('/obj/ij_stereo_camera_rig/f1').set(frame)
hou.parm('/obj/ij_stereo_camera_rig/f2').set(frame)
hou.parm('/obj/ij_stereo_camera_rig/view_cache').set(1)
hou.parm('/obj/ij_stereo_camera_rig/rendertype').set(mode)
hou.parm('/obj/ij_stereo_camera_rig/main_res').set(1)

# RENDER
time_start = time.time()
print "Starting to render... ############################## ",
print "                      ############################## ",
print "# ",
print "# ",
print "# ",
print "# ",
print "Caching Scene............. ##############################",
hou.parm(
    '/obj/ij_stereo_camera_rig/ropnet_RENDER/USECACHE/execute').pressButton()
print "                           ##############################",
print "# ",
print "# ",
print "Writing Passes............. ##############################",
hou.parm('/obj/ij_stereo_camera_rig/ropnet_RENDER/brain_extra_passes/execute'
         ).pressButton()

time_end = time.time() - time_start

print "Done",
print "# ",
print "# ",

print 'Ass file exports took %d seconds.' % (time_end + 1)
print "# ",
print 'Exports complete. Exiting..................'
quit()