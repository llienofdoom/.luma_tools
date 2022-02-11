#####################################################################
# H:\_distros\hfs.windows-x86_64_16.5.473\bin\hython.exe
# H:\_distros\_lumatools\lumatools\luma_houdiniHythonRender.py
# -h X:\_studiotools\TMP\HQ\mantra_test\mantra_test_103.hip
# -r "/out/rop_hm_base"
# -fs 1
# -fe 10
#####################################################################

import sys
import hou

hipfile = sys.argv[1]

print 'Exporting render camera, from %s.' % hipfile

print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"

print 'Exporting Camera...'
hou.parm('/obj/ij_stereo_camera_rig/execute8').pressButton()
print 'Done. Exiting.'
quit()
