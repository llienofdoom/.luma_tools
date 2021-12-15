import sys
import os
import json
import glob
from datetime import datetime
from pprint import pprint
import os.path


if os.environ['IJ_OS'] == 'mac':
    hfs = '/Applications/Houdini/Current/Frameworks/Houdini.framework/Versions/Current/Resources'
if os.environ['IJ_OS'] == 'lin':
    hfs = '/opt/houdini/hfs18.5.462'

sys.path.append(hfs + "/houdini/python%d.%dlibs" % sys.version_info[:2])
import hou


def buildClothSimHip(hip_file_path):
    
        print 'Building cloth sim scene...'
        
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
        print 'hip_file_path'
        hou.hipFile.save(hip_file_path)

        print 'Do Cloth Sim...'
def doClothSim(hip_file_path,parms=[]):

        startTime = datetime.now()
        print "X" * 80
        print "Start time: " + str(startTime) 
        #print hip_file_path
        hou.hipFile.load(hip_file_path, ignore_load_warnings=True)
        bits = os.environ['IJ_SHOT'].split('-')
        root = os.path.dirname(hou.hipFile.path())
        print "Cloth Sim Per Character"
        jsonfilePath = root + "/" + "shot_info.json"
        print jsonfilePath

        with open(jsonfilePath) as json_file:
            json_data = json.load(json_file)
            data = json_data[0]
            assets = data["assets"]
            chars = assets["chars"]
        
        #Open sim file
        sim_details_file = root + "/" + "clothSimInfo.txt"
        sim_details_output = open(sim_details_file, "w")
        sim_details_output.write("Simulation Info______________"+"\n")
        sim_details_output.write("Shot: " + 'act%s_sc%s_sh%s' % (bits[0], bits[1], bits[2]) + "\n")
        sim_start_time = sim_end_time = sim_total_time = None
        
        for char in chars:
                
                sim_start_time = datetime.now()
                shot = 'act%s_sc%s_sh%s' % (bits[0], bits[1], bits[2])
                print "char in shot: " + char
                
                
                if char == "ij_chr_norman":
                    
                    try:
                        print "_____________Norman Cloth Sim Begin________________"
                        norman_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_norman_master')
                        print "set parms, if any..."
                        for parm in parms:
                            print "current parm: "+parm
                        if "wz" in parms:
                            print "world zero parm, set world zero toggle"
                            norman_hda.parm("world_zero_sim").set(1)
                        if "gc" in parms:
                            print "golf cart parm, set golf cart collision toggle"
                            norman_hda.parm("golf_cart_collision") .set(1)   
                        print "- shirt sim begin"
                        norman_hda.parm('shirt_sim').pressButton()
                        print "- shirt sim done"
                        print "- jacket sim begin"
                        norman_hda.parm('jacket_sim').pressButton()
                        print "- jacket sim done"
                        print "______________Norman Cloth Sim Complete_______________"
                    except:
                        print "Norman sim error"
                   
                if char == "ij_chr_charlene":
                    try:
                        print "_____________Charlene Cloth Sim Begin________________"
                        shot = 'act%s_sc%s_sh%s' % (bits[0], bits[1], bits[2])
                        charlene_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_charlene_master')
                        print "set parms, if any..."
                        for parm in parms:
                            print "current parm: "+parm
                        if "wz" in parms:
                            print "world zero parm, set world zero toggle"
                            charlene_hda.parm("world_zero_sim").set(1)
                        if "gc" in parms:
                            print "golf cart parm, set golf cart collision toggle"
                            charlene_hda.parm("golf_cart_collision") .set(1) 
                        print "- dressshirt sim begin"
                        charlene_hda.parm('dressshirt_sim').pressButton()
                        print "- dressshirt sim done"
                        print "- buttonshirt sim begin"
                        charlene_hda.parm('buttonshirt_sim').pressButton()
                        print "- buttonshirt sim done"
                        print "- hair guides sim begin"
                        charlene_hda.parm('hair_guides_sim').pressButton()
                        print "- hair guides sim done"
                        print "______________Charlene Cloth Sim Complete_______________"
                        
                    except:
                        print "Charlene sim error"
                        
                if char == "ij_chr_anderson":
                    try:
                        print "_____________Anderson Cloth Sim Begin________________"
                        anderson_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_anderson_master')
                        print "- shirt sim begin"
                        anderson_hda.parm('shirt_sim').pressButton()
                        print "- dressshirt sim done"
                        print "- pullover sim begin"
                        anderson_hda.parm('pullover_sim').pressButton()
                        print "- pullover sim done"
                        print "______________Anderson Cloth Sim Complete_______________"
                    except:
                        print "Anderson sim error"
                
                if char == "ij_chr_hernandez":
                    print "_____________Hernandez Cloth Sim Begin________________"
                    hernandez_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_hernandez_master')
                    print "- jacket sim begin"
                    hernandez_hda.parm('jacket_sim').pressButton()
                    print "- jacket sim done"
                    print "______________Hernandez Cloth Sim Complete_______________"
                
                if char == "ij_chr_witherington":
                    print "_____________Witherington Cloth Sim Begin________________"
                    witherington_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_witherington_master')
                    print "- pants sim begin"
                    witherington_hda.parm('pants_sim').pressButton()
                    print "- pants sim done"
                    print "- jacket sim begin"
                    witherington_hda.parm('jacket_sim').pressButton()
                    print "- jacket sim done"
                    print "______________Witherington Cloth Sim Complete_______________"
                
                if char == "ij_chr_alejandro":
                    print "_____________Alejandro Cloth Sim Begin________________"
                    alejandro_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_alejandro_master')
                    print "- shirt sim begin"
                    alejandro_hda.parm('shirt_sim').pressButton()
                    print "- shirt sim done"
                    print "______________Alejandro Cloth Sim Complete_______________"
                
                if char == "ij_chr_frankie":
                    try:
                        print "_____________Frankie Cloth Sim Begin________________"
                        frankie_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_frankie_master')
                        print "- jacket sim begin"
                        frankie_hda.parm('jacket_sim').pressButton()
                        print "- jacket sim done"
                        print "- hair guides sim begin"
                        frankie_hda.parm('hair_guides_sim').pressButton()
                        print "- hair guides sim done"
                        print "______________Frankie Cloth Sim Complete_______________"
                    except:
                        print "Frankie sim error"
                
                if char == "ij_chr_mike":
                    try:
                        print "_____________Mike Cloth Sim Begin________________"
                        mike_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_mike_master')
                        print "- jacket sim begin"
                        mike_hda.parm('jacket_sim').pressButton()
                        print "- jacket sim done"
                        print "______________Mike Cloth Sim Complete_______________"
                    except:
                        print "Mike sim error"
                
                if char == "ij_chr_virgil":
                    try:
                        print "_____________Virgil Cloth Sim Begin________________"
                        virgil_hda = hou.node('/obj/ij_shot_builder_'+shot+'/shot_render_geo/chr_virgil_master')
                        print "- cardigan sim begin"
                        virgil_hda.parm('cardigan_sim').pressButton()
                        print "- cardigan sim done"
                        print "______________Virgil Cloth Sim Complete_______________"
                    except:
                        print "Virgil sim error"
                
                
                sim_end_time = datetime.now()
                sim_total_time = sim_end_time - sim_start_time
                sim_details_output.write("Sim time for "+char+": "+str(sim_total_time)+"\n")
                
                    
                
        endTime = datetime.now()
        print "Cloth Sim Per Character COMPLETED"
        print "End Time: " + str(endTime)
        totalSimTime = endTime - startTime 
        print "Total sim time: " + str(totalSimTime)
        sim_details_output.write("Total sim time for shot: " + str(totalSimTime) +"\n")
        sim_details_output.close()
        print 'Done.'

def setShot(act,scene,shot):
    
    # INITIAL #####################################################################
    shots_root = '/mnt/luma_i/shots'
    list_of_shots = ''
    a = 'act' + act
    c = 'sc'  + scene
    s = 'sh'  + shot
    
    path = shots_root + '/%s/%s/%s' % (a, c, s)
    
    act = path.split('/')[4][3:]
    scn = path.split('/')[5][2:]
    sht = path.split('/')[6][2:]

    os.environ['IJ_SHOT']      = '%s-%s-%s' % ( act, scn, sht)
    os.environ['IJ_SHOT_PATH'] = path
    os.environ['IJ_SHOT_NAME'] = 'act%s_sc%s_sh%s' % (act, scn, sht)
    os.chdir(os.environ['IJ_SHOT_PATH'])

    act, scn, sht, = act.lstrip('0'), scn.lstrip('0'), sht.lstrip('0')
    shot_to_set = act+"-"+scn+"-"+sht
    cmd = 'la_cmd ss ' + shot_to_set
    os.system(cmd)
def clothGenerator(parms=[]):
    
    root = os.path.dirname(hou.hipFile.path())
    path_test = os.environ['IJ_SHOT_PATH']
    print "XXXXX ROOOT XXXXX: " + path_test
    bits = os.environ['IJ_SHOT'].split('-')
    name = 'act%s_sc%s_sh%s_clothsim.hip' % (bits[0], bits[1], bits[2])
    hip_file_path = path_test + os.sep + name

    print '*' * 80
    print 'hip_file_path: ' + hip_file_path
    if os.path.exists(hip_file_path):
        
        do_it = raw_input('File already exists. Do you want to overwrite? (y|n) else continue with sim : ')
        if 'y' in do_it:
            print 'Overwriting...'
        
            print "clothSimHip exists, overwritting it."
            buildClothSimHip(hip_file_path)
            print "Do cloth sim from overwritten hip"
            doClothSim(hip_file_path,parms)

        else:
        
            print "Not overwritting clothsim hip but do cloth sim with characters in hip"
            doClothSim(hip_file_path,parms)
    else:

        print "clothSimHip doesn't exist create it and sim characters"
        buildClothSimHip(hip_file_path)
        doClothSim(hip_file_path)

if len(sys.argv) < 2 : # if "lab cs" is input without extra shots 
 
    #DO CURRENT SET SHOT (hopefully you've set it correctly)
    bits = os.environ['IJ_SHOT'].split('-')
    act,scene,shot = bits[0], bits[1], bits[2]
    print "cloth generate for " + act,scene,shot
    parms = []
    clothGenerator(parms)

else:
    
    '''
    #DO Shots 
    shots = sys.argv[1]
    shots = shots.split(",")
    act,scene,shot = "","",""
    for shot in shots:
        act = shot.split("-")[0]
        scene = shot.split("-")[1]
        shot = shot.split("-")[2]

        setShot(act,scene,shot)
        print "cloth generate for " + act,scene,shot
        print "with parms"
        #clothGenerator()
    '''
    #DO Shots 
    sim_details = sys.argv[1]
    shot_parms = sim_details.split(",")
    act,scene,shot = "","",""
    for shot_parm in shot_parms:
        sht = shot_parm.split(".")[0]
        parms = shot_parm.split(".")[1:]

        act = sht.split("-")[0]
        scene = sht.split("-")[1]
        shot = sht.split("-")[2]

        print "shot: "+sht
        print "parms for shot: "
        for parm in parms:
            print parm
        
        setShot(act,scene,shot)
        clothGenerator(parms)
        
        '''
        shot = shot_parm.split(" ")[0]
        act = shot.split("-")[0]
        scene = shot.split("-")[1]
        shot = shot.split("-")[2]
        '''
        #setShot(act,scene,shot)
        #print "cloth generate for " + act,scene,shot
        #print "with parms"
        #clothGenerator()''

    