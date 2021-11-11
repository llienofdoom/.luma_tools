#!/usr/bin/env python2

import os
import sys
import shutil
import glob

def main():
    project_root = os.environ['IJ_LUMA_PROJ_ROOT']
    project_root = '/mnt/luma_i'
    edit_sources_root = os.path.join(project_root, 'editorial', 'edit_sources_master')

    list_of_anim_shots   = glob.glob( os.path.join(edit_sources_root, 'animation', 'act*_sc*_sh*.mov') )
    list_of_oldcur_shots = glob.glob( os.path.join(edit_sources_root, 'animation', 'act*_sc*_sh*.mov') )

    list_of_shots = list(set(list_of_shots))

    for shot in list_of_shots:
        print shot

if __name__ == '__main__':
    main()
