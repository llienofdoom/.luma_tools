import os
import sys
import logging
import maya.cmds as cmds
from datetime import datetime


# Specify where the report file will be saved
arg_folder = os.path.join( sys.argv[-1] )
log_folder = arg_folder
# Start folder name
start_folder = os.path.basename(arg_folder)

# Specify the name of the report file
infection_report_file = os.path.join(log_folder, 'Infection_Report_' + start_folder + '.txt')


if os.path.exists(log_folder):
    pass
else:
    os.mkdir(log_folder)

# Get the current date and time
now = datetime.now()
dt_string = now.strftime("%d %B %Y at %H:%M:%S")

logger = logging.getLogger('mayascan')
logger.setLevel(logging.INFO)

os.environ['MAYA_SKIP_USER_SETUP'] = '1'
logger.info('Usersetup disabled')

import maya.standalone
maya.standalone.initialize()
logger.info('Maya initialized')

import maya.cmds as cmds
cmds.optionVar(iv=('fileExecuteSN', 0))
logger.info('Scriptnodes disabled')

file_list = []
infected_file_list = []
counter = 0

# Open and prep the Infection report file to write the results to
infection_report = open(infection_report_file, 'a+')
infection_report.write('Scan started at ' + dt_string + '\n')
infection_report.write('Scan started in folder ' + sys.argv[-1] + '\n')
infection_report.write('Scanned using Maya ' + str(cmds.about(version=True)) + '\n')
infection_report.write('====================================================================\n')
infection_report.close()

for root, _, files in os.walk(sys.argv[-1]):
    for mayafile in files:
        lower = mayafile.lower()
        if lower.endswith('.ma') or lower.endswith('.mb'):
            try:
                counter += 1
                abspath = os.path.join(root, mayafile)
                infection_report = open(infection_report_file, 'a+')
                infection_report.write('Scanning ' + str(abspath) + '\n')
                infection_report.close()
                logger.info('Scanning {}'.format(abspath))
                cmds.file(abspath, open=True, executeScriptNodes=False, ignoreVersion=True, loadReferenceDepth='none')
                scriptnodes = cmds.ls(type='script')

                infection_report = open(infection_report_file, 'a+')
                infection_report.write('\tStarting iteration over scriptnodes...\n')
                infection_report.close()
                for node in scriptnodes:
                    if 'breed_gene' in node.lower():
                        infected_file_list.append(str(abspath))
                        cmds.delete(node)
                    if 'vaccine_gene' in node.lower():
                        infected_file_list.append(str(abspath))
                        cmds.delete(node)
                infection_report = open(infection_report_file, 'a+')
                infection_report.write('\tDone iteration over scriptnodes. Saving File...\n')
                infection_report.close()
                cmds.file(save=True, force=True)
                infection_report = open(infection_report_file, 'a+')
                infection_report.write('\tSaved. Next one.\n')
                infection_report.close()
            except Exception as e:
                infection_report = open(infection_report_file, 'a+')
                infection_report.write('Failed to parse the maya file. %s\n' % e)
                infection_report.close()

# Remove duplicate entries
infected_file_list = list(dict.fromkeys(infected_file_list))

# Write the list of any infected files into the report file
infection_report = open(infection_report_file, 'a+')
infection_report.write('\n====================================================================\n')
infection_report.write('Infections cleaned in the following files:\n')
infection_report.write('====================================================================\n')
if len(infected_file_list) > 0:
    for infected_entry in infected_file_list:
        infection_report.write(infected_entry + '\n')
else:
    infection_report.write('None\n')
infection_report.write('====================================================================\n')
infection_report.write('\n')
logger.info('Scanned {} files'.format(counter))
infection_report.write('Scanned {} files'.format(counter) + '\n')

# Close the Infection Report file
infection_report.write('\n\n')
infection_report.write('*'*80)
infection_report.write('\n\n\n')
infection_report.close()
