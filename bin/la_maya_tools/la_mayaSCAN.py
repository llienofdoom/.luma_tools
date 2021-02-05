import os
import sys
import logging


logger = logging.getLogger("mayascan")
logger.setLevel(logging.INFO)

os.environ['MAYA_SKIP_USER_SETUP'] = "1"
logger.info("usersetup disabled")

import maya.standalone
maya.standalone.initialize()
logger.info("maya initialized")

import maya.cmds as cmds
cmds.optionVar(iv= ("fileExecuteSN", 0))
logger.info("scriptnodes disabled")

file_list = []
counter = 0

for root, _, files in os.walk(sys.argv[-1]):
    for mayafile in files:
        lower = mayafile.lower()
        if lower.endswith(".ma") or lower.endswith(".mb"):
            counter += 1
            abspath = os.path.join(root, mayafile)
            logger.info("scanning {}".format(abspath))
            cmds.file(abspath, open=True)
            scriptnodes = cmds.ls(type='script')
            # almost all Maya files will contain two nodes named
            # 'sceneConfigurationScriptNode' and 'uiConfigurationScriptNode'
            # a proper job wouldd make sure that they contained only trivial MEL 
            # but youd have to really inspect the contents to make sure
            # a smart attacker hadn't hidden inside those nodes.  For demo purposes
            # I'm just ignoring them but that is a clear vulnerability

            if len(scriptnodes) > 2:
                # here's where you'd want to nuke and resave the file if you were really cleaning house,
                # or you could loop through them applying your own safety test
                logger.warning("file {} contains {} scriptnodes".format(abspath, len(scriptnodes) - 2 ))
                file_list.append(abspath)


logger.info("scanned {} files".format(counter))
if file_list:
    logger.warning ("=" * 72)
    logger.warning ("filenodes found in:")
    for f in file_list:
        logger.warning(f)
