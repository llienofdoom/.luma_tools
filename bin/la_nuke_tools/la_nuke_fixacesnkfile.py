import os
import sys
import json
import glob
import nuke

COMP_ROOT = '/mnt/luma_i/shots'

def main():
    print('Finding all Nuke Comps...')
    list_of_nuke_files = glob.glob(os.path.join(COMP_ROOT, 'act01', 'sc049', 'sh*', 'act*_sc*_sh*_v00.nk'))
    if list_of_nuke_files:
        list_of_nuke_files.sort()
        for nk in list_of_nuke_files:
            print('Processing ' + os.path.basename(nk))
            print('Processing ' + nk)
            # nuke.scriptOpen(nk)

            exr_render_node = nuke.toNode('AUTO_Write_EXR')
            if exr_render_node:
                print('\tTurning off ACES Compliant EXR knob.')
                print('Processing ' + nk)
                # exr_render_node['write_ACES_compliant_EXR'].setValue(0)

            print('\tSaving updated script.')
            print('Processing ' + nk)
            # nuke.scriptSave(nk)
            print('\tDone.\n')

if __name__ == '__main__':
    main()
