import sys
import os
import time
import hou

hipfile = sys.argv[1]
frame = int(sys.argv[2])
mode = int(sys.argv[3])
final = sys.argv[4]

print 'Exporting ASS files to render, from %s.' % hipfile
print 'Doing frame %04d.' % frame

time_start = time.time()
print "Loading file %s" % (hipfile)
hou.hipFile.load(hipfile, suppress_save_prompt=True, ignore_load_warnings=True)
print "Loaded!"
time_end = time.time() - time_start
print 'Scene loading took %d seconds.' % (time_end + 1)

print 'Setting global settings...'

print 'Render Mode is %d' % (mode)

#Update to latest render hda ver
print 'Updating to latest render hda...'
rendernode = hou.node("/obj/ij_stereo_camera_rig/")
library_filepath = rendernode.type().definition().libraryFilePath()
all_definitions = hou.hda.definitionsInFile(library_filepath)
nodename = all_definitions[-1].nodeTypeName()
nodetype = rendernode.type()
if nodetype != nodename:
    rendernode.changeNodeType(all_definitions[-1].nodeTypeName())
    rendernode = hou.node("/obj/ij_stereo_camera_rig/")

#Lock hda
rendernode.matchCurrentDefinition()

#GLOABAL SETTINGS
hou.parm('/obj/ij_stereo_camera_rig/ar_skip_license_check').set(0)
hou.parm('/obj/ij_stereo_camera_rig/enable_volumes').set(0)
hou.parmTuple('/obj/ij_stereo_camera_rig/f').deleteAllKeyframes()
hou.parm('/obj/ij_stereo_camera_rig/f1').set(frame)
hou.parm('/obj/ij_stereo_camera_rig/f2').set(frame)
hou.parm('/obj/ij_stereo_camera_rig/view_cache').set(1)
hou.parm('/obj/ij_stereo_camera_rig/rendertype').set(mode)

#FORCE FINAL RENDER PARAMETERS
if final != 'N' and final != 'n':
    print 'Rendering with final parameters forced on.'
    #Final render settings (WIP)
    # TODO: MAKE SURE SIMS ARE ON FOR MAIN CHARACTERS
    #CHARACTER SETTINGS
    print("Setting up characters...")
    shotname = hou.expandString("$HIPNAME")
    shotname = shotname.split("_render")[0]
    noderoot = "/obj/ij_shot_builder_" + shotname

    #Charlene
    try:
        hou.parm(
            noderoot +
            '/shot_render_geo/chr_charlene_master/hair_deform_switch').set(1)
        hou.parm(noderoot +
                 '/shot_render_geo/chr_charlene_master/deform_switch').set(1)
    except:
        print('Charlene not found')
        pass

    #Frankie

    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_frankie_master/hair_deform_switch').set(
                     1)
        hou.parm(noderoot +
                 '/shot_render_geo/chr_frankie_master/deform_switch').set(1)
    except:
        print('Frankie not found')
        pass

    #Ale
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_alejandro_master/deform_switch').set(1)
    except:
        print('Alejandro not found')
        pass

    #Norman
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_norman_master/deform_switch').set(1)
    except:
        print('Norman not found')
        pass

    #Anderson
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_anderson_master/deform_switch').set(1)
    except:
        print('Anderson not found')
        pass

    #Mike
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_mike_master/deform_switch').set(1)
    except:
        print('Mike not found')
        pass

    #Witherington
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_witherington_master/deform_switch').set(
                     1)
    except:
        print('Witherington not found')
        pass

    #Hernandez
    try:
        hou.parm(noderoot +
                 '/shot_render_geo/chr_hernandez_master/deform_switch').set(1)
    except:
        print('Hernandez not found')
        pass

    print 'Setting final render settings...'
    hou.parm('/obj/ij_stereo_camera_rig/enable_secondary').set(0)
    hou.parm('/obj/ij_stereo_camera_rig/main_res').set("1.0")
    hou.parm('/obj/ij_stereo_camera_rig/ar_ignore_subdivision').set(0)
    hou.parm('/obj/ij_stereo_camera_rig/force_vol').set(0)
else:
    print 'Rendering with current hipfile parameters.'

# RENDER
time_start = time.time()
print "Caching Scene..."
hou.parm('/obj/ij_stereo_camera_rig/ropnet_RENDER/brain_extra_passes/execute'
         ).pressButton()

time_end = time.time() - time_start

print "Done."
print ""
print ""
print 'Ass file exports took %d seconds.' % (time_end + 1)
print " "
print 'Exports complete.'
quit()