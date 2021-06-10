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
import hou

hipfile = sys.argv[1]
frame   = int(sys.argv[2])

print 'Exporting ASS files to render, from %s.' % hipfile
print 'Doing frame %04d.' % frame

print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"

print 'Setting settings...'
hou.parm('/obj/ij_stereo_camera_rig/ar_skip_license_check').set(0)
hou.parmTuple('/obj/ij_stereo_camera_rig/f').deleteAllKeyframes()
hou.parm('/obj/ij_stereo_camera_rig/f1').set(frame)
hou.parm('/obj/ij_stereo_camera_rig/f2').set(frame)

# RENDER
print "Starting to render...",
hou.parm('/obj/ij_stereo_camera_rig/render_to_disk_main').pressButton()

print 'Done. Exiting.'
quit()
