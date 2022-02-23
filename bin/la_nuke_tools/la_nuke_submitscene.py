import os
import sys
import glob
import json

proj_root  = os.environ['IJ_LUMA_PROJ_ROOT']
shots_root = os.path.join(proj_root, 'shots')

try:
    print '#' * 80
    print ''
    process_choice = int(raw_input('Do you want to process similar template comps (1), or scenes (2), or both (3) ? : [1/2/3] : '))
    comp_rebuild_choice = raw_input('Do you also want to rebuild the shots from template? [y/n] : ')

    ######################################################################################################################
    if   process_choice is 1:
        print '\nProcessing all templates.'

    print '\tOptions to choose from:'
    template_master_path = os.path.join(proj_root, 'assets', 'comp', 'templates', 'MASTER')
    list_of_templates = os.listdir(template_master_path)
    list_of_templates.sort()
    templates = []
    template = ''
    i = 1
    if list_of_templates:
        for template in list_of_templates:
            if template.endswith('~'):
                pass
            else:
                template = template.split('.')[0]
                print '\t\t%02d - %s' % (i, template)
                templates.append(template)
                i += 1
    choice_of_template = int(raw_input('\t\tChoose your DESTINY : '))
    if (choice_of_template > 0) and (choice_of_template < len(templates) + 1):
        template = templates[choice_of_template - 1]
        print '\t\tSetting Comp Template to : %s' % template

        print '\tFinding all JSON files...'
        list_of_json_files = glob.glob( os.path.join(shots_root, 'act*', 'sc*', 'sh*', 'shot_info.json') )
        list_of_shots = []
        if list_of_json_files:
            print '\t\tFound %04d entries.' % len(list_of_json_files)
            list_of_json_files.sort()
            print '\tChecking all JSON files for template...',
            for current_json_file in list_of_json_files:
                current_template = ''
                try:
                    json_file  = open( current_json_file, 'r' )
                    json_data  = json.load( json_file )
                    json_file.close()
                    current_template = json_data[0]['comp_template']
                except:
                    current_template = ''
                if current_template != '':
                    if current_template in template:
                        list_of_shots.append( current_json_file.split('/shot_info.json')[0] )
                        print '.',
        print 'Done.\n'
        for current_shot in list_of_shots:
            print '\tProcessing %s' % current_shot

            print '\t\tSetting Shot.'
            shot_bits = current_shot.split('/')
            act = shot_bits[4][3:]
            scn = shot_bits[5][2:]
            sht = shot_bits[6][2:]
            os.environ['IJ_SHOT'] = '%s-%s-%s' % (act, scn, sht)
            os.environ['IJ_SHOT_PATH'] = current_shot
            os.environ['IJ_SHOT_NAME'] = 'act%s_sc%s_sh%s' % (act, scn, sht)

            if 'y' in comp_rebuild_choice.lower():
                print '\t\tRebuilding Comp...'
                cmd = 'echo python $IJ_LOCAL_REPO/bin/la_nuke_tools/la_nuke_autocomp.py;'
                os.system( cmd )
                cmd = 'echo $IJ_LOCAL_REPO/bin/la_tools/la_nukepy $IJ_LOCAL_REPO/bin/la_nuke_tools/la_nuke_autocomp_setup.py $IJ_SHOT_PATH/$IJ_SHOT_NAME\_comp_v00.nk'
                os.system( cmd )
            else:
                print '\t\tNot Rebuilding Comp.'
            print '\t\tSubmitting.'
            cmd = 'echo $IJ_LOCAL_REPO/bin/la_tools/la_nukepy $IJ_LOCAL_REPO/bin/la_nuke_tools/la_nuke_submit2opencue.py $IJ_SHOT_PATH/$IJ_SHOT_NAME\_comp_v00.nk'
            os.system( cmd )

            print '\t\tDone.'




















    ######################################################################################################################
    elif process_choice is 2:
        print '\nProcessing individual scenes.'





    ######################################################################################################################
    elif process_choice is 3:
        print '\nProcessing using both template and scene.'



    ######################################################################################################################
    else:
        print '\nI\'m not sure what you typed, but that was not in ANY way correct. Giving up, like you should ;-)'
except Exception as e:
    print e
    print '#' * 80
    print ''
    print 'I\'m not sure what you typed, but that was not in ANY way correct. Giving up, like you should ;-)'

