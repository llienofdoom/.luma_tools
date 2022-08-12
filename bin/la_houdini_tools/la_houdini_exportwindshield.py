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

print 'Exporting Nailbridge Windshield from %s.' % hipfile

print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"

print 'Finding Nailbridge node...'
nailbridge_node = ''
root = hou.node('/obj')
nodes = root.children()
for node in nodes:
    if 'shot_builder' in node.name():
        path = node.path() + '/shot_render_geo'
        shot_render_geo = hou.node(path)
        if shot_render_geo:
            children = shot_render_geo.children()
            for child in children:
                if 'env_nailbridge_master' in child.name():
                    print 'Found', child.name()
                    nailbridge_node = child

if nailbridge_node:
    print 'Exporting Windshield...'
    path = nailbridge_node.path() + '/export_screen'
    hou.parm(path).pressButton()
    print 'Done. Exiting.'
else:
    print 'Not Found. Quitting.'
quit()
