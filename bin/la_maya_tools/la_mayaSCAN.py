import os
import sys
import datetime

log_file = open('/mnt/luma_i/vaccine_check_log.txt', 'w')
date     = datetime.datetime.now()
log_file.write('DATE : {}\n'.format(date))

os.environ['MAYA_SKIP_USER_SETUP'] = "1"
log_file.write('userSetup disabled.\n')

import maya.standalone
maya.standalone.initialize()
log_file.write('maya initialized.\n')

import maya.cmds as cmds
cmds.optionVar(iv= ("fileExecuteSN", 0))
log_file.write('scriptnodes disabled\n')

for root, _, files in os.walk(sys.argv[-1]):
    for mayafile in files:
        lower = mayafile.lower()
        if lower.endswith(".ma") or lower.endswith(".mb"):
            abspath = os.path.join(root, mayafile)
            log_file.write('scanning {}\n'.format(abspath))
            cmds.file(abspath, open=True)
            scriptnodes = cmds.ls(type='script')

            for node in scriptnodes:
                if 'sceneconfigurationscriptnode' in node.lower():
                    pass
                elif 'uiconfigurationscriptnode' in node.lower():
                    pass
                elif 'igpucs' in node.lower():
                    pass
                else:
                    log_file.write('file {} contains {} scriptnode.\n'.format(abspath, node ))

log_file.close()
