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
import hou

hipfile = sys.argv[1]

print 'Exporting STATIC ASS CACHE FILE, FOR %s.' % hipfile

print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"

print 'Scene loading done.'

print 'Setting settings...'

hou.parm('/obj/ij_stereo_camera_rig/view_cache').set(0)

# RENDER

print "Starting to render... ############################## ",
print "                      ############################## ",
print "# ",
print "# ",
print "Writing static geo... ############################## ",
print "                      ############################## ",
print "# ",
print "# ",
hou.parm('/obj/ij_stereo_camera_rig/writecache2').pressButton()
print "                      ############################## ",
print "# ",
print "# ",

print 'Static Export Done'
print "                      ############################## ",
print "# ",
print "# ",

print 'Done. Exiting.'
quit()
