import toolutils
import os
import subprocess
import sys
import shutil
import hou
from sys import platform
###### HIII
if len(sys.argv) != 3:
    print "You're an idiot. Please RTFM, and type lab ae [inputPath] [assetType]."
    sys.exit()

# boobs basefolder asset_type

# geoname = "chr_ij_mst_zolthard_chr_9"
# assetType = 'chr'
# inpath = "U:/ij_luma/_tools/_dev/Stephen/testoutput/" + assetType + '/' + geoname+'/'
# outpath = "U:/ij_luma/_tools/_dev/Stephen/testoutput/" + assetType + '/' + geoname + '/'
'''
geoname = "env_ij_env_normanbedroom_9"
assetType = 'env'
inpath = 'i:/_luma/ij_luma/_tools/_dev/Stephen/testoutput/' + assetType + '/' + geoname + '/'
outpath = 'i:/_luma/ij_luma/_tools/_dev/Stephen/testoutput/' + assetType + '/' + geoname + '/'
'''

inpath = sys.argv[1]
# output arg isn't getting used. We build the scene in the same folder as the input
#outpath = sys.argv[2]
assetType = sys.argv[2]


inpath = inpath.rstrip('/')
geoname = inpath.split('/')[-1]
print('\ninpath: %s' % (inpath))
#outpath = sys.argv[3]
inpath  = inpath + '/'
outpath = inpath


if not os.path.exists(outpath):
    print("CREATING OUTPATH: "+outpath)
    os.makedirs(outpath, exist_ok=True)


#change i:/ to $JOB for use in assets later
if "i:" in str(inpath):
    inpath = inpath.replace("i:", "$JOB")
elif "/mnt/luma_i/" in str(inpath):
    inpath = inpath.replace("/mnt/luma_i", "$JOB")

abcpath = inpath + geoname + '.abc'
csvpath = inpath + geoname + '_matDict.csv'
geopath = inpath + geoname + '.bgeo.sc'
hippath = outpath + geoname + '.hip'
shaderDictPath = inpath + geoname + '_shaderDict.json'
textureDictPath = inpath + geoname + '_texDict.json'

if "linux" in platform:
    rman_ar_dict = "$JOB/_tools/_dev/Stephen/ijtools/BuildMaterials/rman_ar_dictionary_v04.json"
    setJob = '/mnt/luma_i'
    hou.hscript('setenv JOB=' + setJob)
elif "win" in platform:
    rman_ar_dict = "$JOB/_tools/_dev/Stephen/ijtools/BuildMaterials/rman_ar_dictionary_v04.json"
    setJob = 'i:'
    hou.hscript('setenv JOB=' + setJob)

print('geoname: %s' % (geoname))
print('abcpath: %s' % (abcpath))
print('csvpath: %s' % (csvpath))
print('geopath: %s' % (geopath))
print('hippath: %s' % (hippath))


#hou.hscript('setenv JOB=' + setjob)
#elf.proj = hou.getenv('JOB') + "/"

#SAVING .HIP FILE FILE
hou.hipFile.save(hippath, save_to_recent_files=False)

#
# CHARACTER
#
if assetType == "chr":
    assetChrLookup = "$JOB/assets/chr/tools/asset_chr_lookup.hda"
    assetLookdev = "$JOB/assets/gen/tools/asset_lookdev_hda/asset_lookdev.hda"
          
    print('INSTALLING asset_char_lookup.hda: %s' % (assetChrLookup))
    hou.hda.installFile(assetChrLookup)
    print('Make nodes')
    obj = hou.node("/obj/")
       
    hda_chr = obj.createNode("la_ij::asset_chr_lookup", "asset_chr_lookup")
    print('set parms')
    hda_chr.parm("chr_name").set(geoname)
    hda_chr.parm("abcfile").set(abcpath)
    hda_chr.parm("csvfile").set(csvpath)
    hda_chr.parm("sdr_Dict_jsonfile").set(shaderDictPath)
    hda_chr.parm("tex_jsonfile").set(textureDictPath)
    hda_chr.parm("rman_ar_dict").set(rman_ar_dict)
    hda_chr.parm("unpackabc").set(1)
    
    hou.hda.installFile(assetLookdev)
    hda_lookdev = obj.createNode("asset_lookdev", "asset_lookdev")
    
#
# PROPS
#
if assetType == "prp":
    assetPrpLookup = "$JOB/assets/prp/tools/asset_prp_lookup.hda"
    #assetLookdev = "$JOB/assets/gen/tools/asset_lookdev_hda/asset_lookdev.hda"
          
    print('INSTALLING asset_prp_lookup.hda: %s' % (assetPrpLookup))
    hou.hda.installFile(assetPrpLookup)
    print('Make nodes')
    obj = hou.node("/obj/")
       
    hda_prp = obj.createNode("la_ij::asset_prp_lookup", "asset_prp_lookup")
    print('set parms')
    hda_prp.parm("chr_name").set(geoname)
    hda_prp.parm("abcfile").set(abcpath)
    hda_prp.parm("csvfile").set(csvpath)
    hda_prp.parm("sdr_Dict_jsonfile").set(shaderDictPath)
    hda_prp.parm("tex_jsonfile").set(textureDictPath)
    hda_prp.parm("rman_ar_dict").set(rman_ar_dict)
    hda_prp.parm("unpackabc").set(1)
    
    #hou.hda.installFile(assetLookdev)
    #hda_lookdev = obj.createNode("asset_lookdev", "asset_lookdev")
#
# ENV
#

if assetType == "env":
    assetEnvLookup = "$JOB/assets/env/_tools/asset_env_lookup.hda"
    #assetLookdev = "$JOB/assets/gen/tools/asset_lookdev_hda/asset_lookdev.hda"
          
    print('INSTALLING asset_env_lookup.hda: %s' % (assetEnvLookup))
    hou.hda.installFile(assetEnvLookup)
    print('Make nodes')
    obj = hou.node("/obj/")
       
    hda_prp = obj.createNode("la_ij::asset_env_lookup", "asset_env_lookup")
    print('set parms')
    hda_prp.parm("env_name").set(geoname)
    hda_prp.parm("abcfile").set(abcpath)
    hda_prp.parm("csvfile").set(csvpath)
    hda_prp.parm("sdr_Dict_jsonfile").set(shaderDictPath)
    #hda_prp.parm("tex_jsonfile").set(textureDictPath)
    hda_prp.parm("rman_ar_dict").set(rman_ar_dict)
    hda_prp.parm("unpackabc").set(0)
    
    #hou.hda.installFile(assetLookdev)
    #hda_lookdev = obj.createNode("asset_lookdev", "asset_lookdev")

'''
hda.parm("geofile").set(geopath)

hda.parm("execsavegeofile").pressButton()
hda.parm("loadfromdisk").set(1)
hda.parm("reloadgeofile").pressButton()


print('\nINIT TURNTABLE:')

hou.hda.installFile("H:/SITE/houdini17.5/otls/la_light_test_rig.hda")

center = obj.createNode('null', 'center')
center.setDisplayFlag(0)
light = obj.createNode('light_test_rig')
light.setInput(0, center, 0)
obj.layoutChildren()

geometry = geo.displayNode().geometry()
bb = geometry.boundingBox()

bbcenter = bb.center()
bbsize = bb.sizevec()
bblen = bbsize.length()

center.parmTuple('t').set(bbcenter)

distmult = 2
light.parm('tz2').set(bblen * distmult)
light.parm('rx2').set(15)
light.parm('ty2').set(0)
light.parm('camslices').set(24)
light.parm('showgeo').set(0)
light.parm('renderbg').set(0)
light.parm('vm_picture').set(outpath + '$HIPNAME/flip/01/$HIPNAME.$F4.jpg')

print('TurnTable Path: ' + outpath + '$HIPNAME/flip/01/$HIPNAME.$F4.jpg')

cam = light.node('Editable_Network/cam_TestRig')



#desktop = hou.ui.desktop('Build')
#desktop.setAsCurrent()
#scene_viewer = desktop.paneTabOfType(hou.paneTabType.SceneViewer)
#viewport = scene_viewer.findViewport('persp1')
#viewport.setCamera(cam)

print('\nRENDERING TURNTABLE OGL:!')

campath = '/obj/light_test_rig1/Editable_Network/cam_TestRig'
jpgpath = outpath + '/flip/01/' + geoname + '.$F4.png'
print(jpgpath)

ogl = hou.node('/out/').createNode('opengl')
ogl.parm("trange").set(1)
ogl.parm("f1").set(1)
ogl.parm("f2").set(24)
ogl.parm("camera").set(campath)
ogl.parm("alights").set('')

ogl.parm("picture").set(jpgpath)

#ogl.parm("execute").pressButton()

# print 'jippo capture'
# for i in range(1,25):
#     ogl.parm("f1").set(i)
#     ogl.parm("execute").pressButton()

print('jippo capture')
ogl.parm("trange").set(0)
for i in range(1,25):
    hou.setFrame(i)
    ogl.parm("execute").pressButton()

'''
hou.hipFile.save(hippath, save_to_recent_files=False)
print('\nASSET SAVED: %s' % (geoname))
'''
print('\nMAKING VIDEO: %s' % (outpath + '/flip/' + geoname + '.mp4'))
cmd = 'ffmpeg -y -r 12 -i '
cmd += outpath + '/flip/01/' + geoname + '.%04d.png'
cmd += ' -c:v libx264 '
cmd += outpath + '/flip/' + geoname + '.mp4'



subprocess.check_output(cmd, shell=False)

inpath = outpath + '/flip/' + geoname + '.mp4'
outpath = sys.argv[2]

if not os.path.exists(outpath):
    os.mkdir(outpath)

outpath = outpath + assetType

if not os.path.exists(outpath):
    os.mkdir(outpath)

outpath = outpath +'/'+ geoname + '.mp4'
shutil.copyfile(inpath, outpath)
'''
