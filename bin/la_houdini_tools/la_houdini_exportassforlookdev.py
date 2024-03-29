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
frame   = int(sys.argv[2])

print 'Exporting ASS files to render, from %s.' % hipfile
print 'Doing frame %04d.' % frame

time_start = time.time()
print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"
time_end = time.time() - time_start
print 'Scene loading took %d seconds.' % (time_end + 1)

print 'Setting settings...'
hou.parm('/obj/asset_lookdev/ar_skip_license_check').set(0)
hou.parmTuple('/obj/asset_lookdev/f').deleteAllKeyframes()
hou.parm('/obj/asset_lookdev/f1').set(frame)
hou.parm('/obj/asset_lookdev/f2').set(frame)

# RENDER
time_start = time.time()
print "Starting to render...",
hou.parm('/obj/asset_lookdev/render_to_disk_main').pressButton()
time_end = time.time() - time_start
print 'Ass file exports took %d seconds.' % (time_end + 1)

print 'Done. Exiting.'
quit()
