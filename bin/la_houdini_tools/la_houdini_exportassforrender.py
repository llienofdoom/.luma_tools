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

print 'Exporting ASS files to render, from', hipfile

print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile)
print "Loaded!"

"""
hou.parm('/obj/ij_stereo_camera_rig/ar_skip_license_check').set(0)

fs  = int(sys.argv[6])
fe  = int(sys.argv[8])
print "Setting frame range to %d - %d" % (fs, fe)

# RENDER
print "Starting to render...",
rop.render(frame_range=(fs, fe))
print "DONE!"

"""
print 'Done. Exiting.'
quit()
