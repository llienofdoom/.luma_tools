import os
import sys
import json

print 'Setting Comp Template.'

# Read JSON file for comp info and frame ranges, etc.
shot_path = os.environ['IJ_SHOT_PATH']
print '\tReading JSON file...',
json_file  = open( os.path.join(shot_path, 'shot_info.json'), 'r' )
json_data  = json.load( json_file )
json_file.close()
print 'Done.'

print '\tGetting Comp Template...',
comp_template = ''
try:
    comp_template = str(json_data[0]['comp_template'])
    print 'Found.'
except:
    print 'NOT Found. Creating.'
    json_data[0]['comp_template'] = ''

print '\tCurrently set to : %s' % comp_template

print '\tOptions to choose from:'
template_master_path = os.path.join(os.environ['IJ_LUMA_PROJ_ROOT'], 'assets', 'comp', 'templates', 'MASTER')
list_of_templates = os.listdir(template_master_path)
list_of_templates.sort()
templates = []
i = 1
if list_of_templates:
    for template in list_of_templates:
        if template.endswith('~'):
            pass
        else:
            # template = template[17:]
            template = template.split('.')[0]
            print '\t\t%02d - %s' % (i, template)
            templates.append(template)
            i += 1

choice = int(raw_input('\tChoose your DESTINY : '))

if (choice > 0) and (choice < len(templates) + 1):
    template = templates[choice - 1]
    print '\tSetting Comp Template to : %s' % template
    json_data[0]['comp_template'] = template
    json_file = open( os.path.join(shot_path, 'shot_info.json'), 'w' )
    json.dump(json_data, json_file, sort_keys=True, indent=4)
    json_file.close()
else:
    print '\tERROR: Input makes no sense. Be better. Quiting.'
