import os
import sys
import shutil
import glob

def main():
    project_root = os.environ['IJ_LUMA_PROJ_ROOT']
    edit_sources_root = os.path.join(project_root, 'editorial', 'edit_sources_master')

    list_of_shots  = glob.glob( os.path.join(edit_sources_root, 'animation', 'act*_sc*_sh*.mov') )
    list_of_shots  = list(set(list_of_shots))

    for shot in list_of_shots:
        shot_name = os.path.basename(shot)
        type_of_shot = ''
        print '*' * 50
        print 'Updating ' + shot_name
        current_path = ''
        render_path = os.path.join(edit_sources_root, 'render', shot_name)
        comp_path = os.path.join(edit_sources_root, 'comp'  , shot_name)
        if os.path.exists(comp_path):
            current_path = comp_path
            type_of_shot = 'comp'
        elif os.path.exists(render_path):
            current_path = render_path
            type_of_shot = 'render'
        else:
            current_path = shot
            type_of_shot = 'animation'
        if current_path:
            print '\tLatest is %s.' % type_of_shot
            print '\tFound in %s.' % current_path.split(edit_sources_root)[-1][1:]
            try:
                copy_path = os.path.join(edit_sources_root, '_latest_shot_version', shot_name)
                print '\tCopy to  %s' % copy_path.split(edit_sources_root)[-1][1:]
                shutil.copy2(current_path, copy_path)
            except:
                print 'Failed to copy %s' % current_path
        else:
            print '\tNot Found.'
        print ''

if __name__ == '__main__':
    main()
