import json
import os
import sys
import pprint
import csv
from sys import platform
from shutil import copyfile
import glob

if len(sys.argv) != 4:
    print "You're an idiot. Please RTFM."
    sys.exit()

scenefile          = ''
outpath            = ''
assetType          = ''
doExportMatDict    = 0
doExportShaderDict = 0
doExportAlembic    = 0
doExportAssetDict  = 0
doExportAssetTex   = 0
doExportRibDict    = 0

ask = raw_input('Customize? : (Y/n)')
if 'y' in ask.lower():
    scenefile = sys.argv[1]
    outpath   = sys.argv[2]
    assetType = sys.argv[3]
    print 'Please enter binary string for options. [doMat | doShad | doAlem | doAssDic | doAssTex | doRibDic]'
    print '\teg : 101101.'
    choice = raw_input('GO :')
    doExportMatDict    = int(choice[0])
    doExportShaderDict = int(choice[1])
    doExportAlembic    = int(choice[2])
    doExportAssetDict  = int(choice[3])
    doExportAssetTex   = int(choice[4])
    doExportRibDict    = int(choice[5])

elif 'n' in ask.lower():
    scenefile = sys.argv[1]
    outpath   = sys.argv[2]
    assetType = sys.argv[3]
    doExportMatDict    = 1
    doExportShaderDict = 1
    doExportAlembic    = 1
    doExportAssetDict  = 0
    doExportAssetTex   = 0
    doExportRibDict    = 1
    
else:
    print 'do NOTHING'
    sys.exit()

print('\n===================================== RUNNING MAYA FROM COMMAND LINE ========================================')

import maya.standalone
import sys
import maya.cmds as cmds
maya.standalone.initialize()
cmds.loadPlugin("AbcExport")
# cmds.loadPlugin("RenderMan_for_Maya")

# boobs scenefile outpath assetType {domat(1) doshad(1) doalemb(1) doassdic(0) doasstex(0) doribdic(1)}

# pprint.pprint(sys.argv)
# scenefile = sys.argv[1]
# outpath = sys.argv[2]
# assetType = sys.argv[3]

# doExportMatDict = int(sys.argv[4])
# doExportShaderDict = int(sys.argv[5])
# doExportAlembic = int(sys.argv[6])
# doExportAssetDict = int(sys.argv[7])
# doExportAssetTex = int(sys.argv[8])
# doExportRibDict = int(sys.argv[9])


#scenefile = r"U:/ij_luma/_tools/_dev/Stephen/testscenes/chr_ij_mst_norman_chr_9.mb"
#doExportMatDict = 1
#doExportAlembic = 1
#assetType = 'chr'
#outpath = r'U:/ij_luma/_tools/_dev/Stephen/testoutput/' + assetType

print('\nOPENING SCENE FILE: %s' % (scenefile))
#cmds.file(new=True, force=True)
#cmds.file(scenefile, open=True)

cmds.file(new=True, force=True)
cmds.file(scenefile, open=True)

filepath = cmds.file(q=True, sn=True)
filenameext = os.path.basename(filepath)
filename, extension = os.path.splitext(filenameext)

# - removed scenefile to outpath
# - original - (outpath = outpath + assetType + '/' + scenefile + '/')
if 'chr' in str(assetType):
    #outpath = outpath + assetType + '/' + filename + '/' + "render" + "/"
    outpath = outpath + assetType + '/' + "render" + "/" + filename + '/'
else:
    outpath = outpath + assetType + '/' + filename + '/'

outpath = outpath.replace(' ', '')

# Create outpath Directory if don't exist
if not os.path.exists(outpath):
    print("HERE:"+outpath+"DONE")
    os.makedirs(outpath)

print("outpath:"+outpath)
print("filenameext:"+filenameext)
print("filename:"+filename)


def exportMatDict():

    matDict, texDict = {}, {}

    print('\nEXAMINING SCENE OBJECTS')

    path2 = ''
    files = cmds.ls(type='PxrTexture')
    # Get all object nodes
    theNodes = cmds.ls(dag=True, s=True)

    # Create Material Dictionary
    for node in theNodes:

        # Get the nodes shadingEngine
        shadeEng = cmds.listConnections(node, type="shadingEngine")

        # Get the connected material name. This works but is slow.
        #materials = cmds.ls(cmds.listConnections(shadeEng), materials=True)

        # Get material. Naively assume all shaders ending in _sg have a material of the same name ending in _mat
        if shadeEng:
            mat = ''
            if len(shadeEng) > 0:
                mat = shadeEng[0]
                mat = mat.replace('_sg', '_mat')

            matDict[str(node)] = str(mat)

    count = len(matDict.keys())
    print('MATERIAL NODES FOUND: %d' % (count))

    # MATERIAL JSON and CSV ########################################################################
    outname = filename + '_matDict'
    print('\nOUTPATH: %s' % (outpath))

    print('WRITING JSON FILE TO: %s' % (outname + '.json'))
    with open(outpath + outname + '.json', 'w') as outfile:
        json.dump(matDict, outfile, indent=4)

    print('WRITING CSV FILE TO: %s' % (outname + '.csv'))
    with open(outpath + outname + '.csv', 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in matDict.items()]

    '''
    # Create Texture Dictionary
    for mat in matDict:
        if (matDict[mat].find('_mat') != -1):
            texDict[matDict[mat]] = ""
        else:
            continue
    # Create Texture Dictionary   
    for tex in texDict:
        for file in files:
            if(file.find(tex[:-4]) != -1):
                fpath = cmds.getAttr(file+".filename")
                path2 = path2+"&"+fpath   
                texDict[tex] = path2
            else:
                path2 = ""

    #pprint.pprint(texDict, width=1)

    
    # TEXTURE JSON and CVS ##########################################################################
    outname2 = filename + '_texDict'
    print('\nOUTPATH: %s'% (outpath))

    print('WRITING JSON FILE TO: %s' % (outname2 + '.json'))
    with open(outpath + outname2 + '.json', 'w') as outfile:
        json.dump(texDict, outfile, indent=4)

    print('WRITING CSV FILE TO: %s' % (outname2 + '.csv'))
    with open(outpath + outname2 + '.csv', 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in texDict.items()]    
    '''


def exportShaderDict():

    # Get all material/shader nodes in the scene. Filter out some default shader types
    default_shaders = ["lambert1", "particleCloud1", "shaderGlow1"]
    scene_shaders = []
    temp_shaders = cmds.ls(materials=True)

    for shader in temp_shaders:
        if shader in default_shaders:
            print("Skipping " + shader)
        else:
            scene_shaders.append(shader)

    # For each scene shader, build a dict of its internal nodes and connections
    nodeDict = {}
    for node in scene_shaders:
        shade_eng = cmds.listConnections(node, type="shadingEngine")
        try:  # ADDED due to some shading groups in MAYA not being iterable
            for s in shade_eng:
                nodesLen = 0
                nodes = cmds.listHistory(s, pdo=True, ha=True, groupLevels=True)
                nodesLen = len(nodes)
                nodeCountInLvl = 1
                nodeDict[s] = {}
                lvl = 1
                if nodesLen == 1:  # IF A SHADING GROUP ONLY HAS A SINGLE NODE CONNECTED.  IMPORTANT FOR FUTURE USE ON ENV,PRP ect
                    con = cmds.listHistory(s, pdo=True, lv=1, groupLevels=True, bf=False)
                    nodeDict[s]["nodes"] = {}
                    for c in con:
                        type = cmds.nodeType(c)
                        nodeDict[s]["nodes"][c] = {"type": type, "connections": "", "zAttributes": {}}

                else:
                    # if s == "charleneboots_sg":
                    while nodeCountInLvl < nodesLen:
                        con = cmds.listHistory(s, pdo=True, lv=lvl, groupLevels=True, bf=False)
                        currentlvl = lvl
                        lvl += 1
                        nodeCountInLvl = len(con)
                        nodeDict[s]["nodes"] = {}

                        for c in con:
                            texPath = ""
                            conec = cmds.listConnections(c, c=True, d=False)
                            type = cmds.nodeType(c)
                            if conec == None:
                                conec = ["noInput"]
                            if type == "PxrTexture":
                                texPath = cmds.getAttr("%s.filename" % c)
                            # ADD SHIT
                            nodeDict[s]["nodes"][c] = {"type": type, "connections": conec, "zAttributes": {"filePath": texPath}}
        except:
            print("Not iterable")
    # pprint.pprint(nodeDict)
    #
    outname = filename + '_shaderDict'
    print('\nOUTPATH: %s' % (outpath))

    print('WRITING JSON FILE TO: %s' % (outname + '.json'))
    with open(outpath + outname + '.json', 'w') as outfile:
        json.dump(nodeDict, outfile, indent=4)


def exportAlembicScene():

    # Write out a single frame alembic from the whole scene geometry
    # Run below to see help file for AbcExport
    # cmds.AbcExport(h=True)

    start = str(1)
    end = str(1)
    #save_name = r'U:\ij_luma\_tools\_dev\Stephen\testoutput\alembicTest.abc'
    save_name = outpath + filename + '.abc'

    #added - (-writeCreases)
    command = "-frameRange " + start + " " + end + " -dataFormat ogawa -uvWrite -writeCreases -file " + save_name

    print("\nATTEMPTING TO EXPORT SCENE TO ALEMBIC:")
    print(command)

    cmds.AbcExport(j=command)

    print("\nABC SUCCESSFUL!... PROBABLY")


def exportAssetDict():
    from string import digits

    assemblies = cmds.ls(assemblies=True)
    # print node
    nodeDict = {}
    typeList = ['cameraAsset', 'sceneAsset', 'rigAsset', 'prp', 'env', 'lgt', 'hrs', 'chr', 'wrd']

    for node in assemblies:

        # Skip objects that are not Special Assets
        if not any(word.translate(None, digits) in node.split('_') for word in typeList):
            continue

        attsDict = {}

        atts = cmds.listAttr(node)
        # print atts[-9:-1]

        # Custom Node attributes:
        for att in atts[-9:-1]:
            value = cmds.getAttr(node + '.' + att)
            # print value
            attsDict[att] = value

        attsDict['localt'] = cmds.getAttr(node + '.' + 't')
        attsDict['localr'] = cmds.getAttr(node + '.' + 'r')
        attsDict['locals'] = cmds.getAttr(node + '.' + 's')
        transform = cmds.xform(node, q=True, ws=True, m=True)
        attsDict['xformws'] = transform

        nodeDict[node] = attsDict

    # print nodeDict

    outname = filename + '_AssetDict'

    #j = json.dumps(nodeDict, indent=4)
    # print j
    # \\192.168.35.30\ij_luma\_tools\Stephen\test.json
    with open(outpath + outname + '.json', 'w') as outfile:
        json.dump(nodeDict, outfile, indent=4)

    print("\nASSET DICT EXPORT SUCCESSFUL!... PROBABLY")


def exportRibDict():
    ribDict = {}

    theNodes = cmds.ls(dag=True, transforms=True)
    for child in theNodes:
        shapes = cmds.listRelatives(child, shapes=True)
        rib = ''
        frame = 1
        shapeType = ''

        if shapes:
            try:
                shapeType = str(cmds.nodeType(shapes[0]))
            except:
                continue

            # if shapeType == 'gpuCache':
            if shapeType != 'RenderManArchive':
                continue

            #print ('\n'+ child)
            #print ('shape: ' + shapes[0])
            #print( shapeType)
            try:
                rib = str(cmds.getAttr(shapes[0] + '.filename'))
                frame = cmds.getAttr(shapes[0] + '.frame')
            except:
                continue

        if rib == '':
            continue

        # print str(rib)
        # print str(frame)

        attsDict = {}

        attsDict['localt'] = cmds.getAttr(child + '.' + 't')
        attsDict['localr'] = cmds.getAttr(child + '.' + 'r')
        attsDict['locals'] = cmds.getAttr(child + '.' + 's')
        transform = cmds.xform(child, q=True, ws=True, m=True)
        attsDict['xformws'] = transform
        attsDict['ribArchive'] = rib
        attsDict['ribFrame'] = frame
        attsDict['shapeType'] = shapeType

        ribDict[child] = attsDict

    exportJson = 1
    dopprint = 0

    if dopprint:
        pprint.pprint(ribDict)

    if exportJson:
        outname = filename + '_ribDict'
        fullpath = outpath + outname + '.json'

        print('WRITING RIB JSON FILE TO: %s' % (fullpath))
        with open(fullpath, 'w') as outfile:
            json.dump(ribDict, outfile, indent=4)

        print("\nRIB DICT EXPORT SUCCESSFUL!... PROBABLY")



def exportAssetTex():

    fileTypes = ['tif', 'tiff', 'png', 'jpg', 'tga']
    counter = 0
    pathDict = {}
    extDict = {}
    texDict = {}
    destination_dir = outpath + "tex" + "/"
    #destination_dir = "/mnt/luma_i/assets/chr/render/chr_ij_mst_zolthard_chr_9/tex"

    # Get all Renderman texture nodes
    pxrFileList = cmds.ls(type='PxrTexture')

    for item in pxrFileList:

        # Get texnode filename and repoint to the new server
        filePathFull = cmds.getAttr(item + '.filename')
        # print fileDirectory

        texPath, texNameWithExt = os.path.split(filePathFull)
        texPath = texPath.replace("/job/", "/mnt/ij_fc/")

        texName, ext = os.path.splitext(texNameWithExt)  # preserves number or udim in name. eg. texture.Color.1001 + .jpg
        ext = ext.lstrip('.')  # '.jpg' to 'jpg'

        # check if map used is in a udim set
        if "MAPID" in texName:
            try:
                # Remove '.MAPID' in tex name because we don't know what texture numbers exist. eg. 1001, 1032 etc.
                texNameNoNumber = ('.'.join(texName.split('.')[:-1]))

                for file in os.listdir(texPath):
                    if file.split('.')[-1] in fileTypes:
                        if texNameNoNumber in file:
                            texDict[file] = texPath
            except:
                print("FAILED TO FIND UDIM TEXPATH ON DISK! : " + filePathFull)
        else:
            try:
                for file in os.listdir(texPath):
                    if texName in file:
                        # if file.endswith(".tif") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".tiff") or file.endswith(".tga"):
                        if file.split('.')[-1] in fileTypes:
                            texDict[file] = texPath
            except:
                print("FAILED TO FIND SINGLE TEXPATH ON DISK! : " + filePathFull)

    if not os.path.exists(destination_dir):
        print("CREATING DIRECTORY: " + destination_dir)
        os.makedirs(destination_dir)

    for texName, texPath in texDict.items():
        try:
            # print "copying: " + texName + " in " + texPath + " to directory: " + destination_dir

            source = os.path.join(texPath, texName)
            target = os.path.join(destination_dir, texName)
            print source
            print target
            copyfile(source, target)
        except:
            print("Failed to copy file: " + source)


if doExportMatDict == 1:
    print("do export mat dict")
    exportMatDict()

if doExportShaderDict == 1:
    print("do export shader dict")
    exportShaderDict()

if doExportAlembic == 1:
    print("do export Alembic")
    exportAlembicScene()

if doExportAssetDict == 1:
    print("do export asset dict")
    exportAssetDict()

if doExportAssetTex == 1:
    print("copy over asset textures")
    exportAssetTex()

if doExportRibDict == 1:
    print("copy export rib dict")
    exportRibDict()
