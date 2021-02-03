import os
import sys
import shutil
import glob
import json

###############################################################################
def find_shot_data():
    print('Collecting shot_info files...')
    root = os.environ['JOB']
    shot_folder = os.path.join(root, 'shots')
    list_of_json_files = glob.glob(
        os.path.join(shot_folder, 'act*', 'sc001', 'sh*', 'shot_info.json')
    )
    return list_of_json_files
###############################################################################
def find_env_asset_paths():
    print('Collecting environment assets...')
    root = os.environ['JOB']
    asset_folder = os.path.join(root, 'assets', 'env')
    list_of_env_assets = glob.glob(
        os.path.join(asset_folder, 'env_ij_mst_*')
    )
    return list_of_env_assets

###############################################################################
def main():
    list_of_env_assets = find_env_asset_paths()
    list_of_json_files = find_shot_data()

    print('Looping over shots...')
    for shot in list_of_json_files:
        scene_name = shot.split('/')[-3]
        shot_name  = shot.split('/')[-2]
        print('\n\tShot {}'.format(shot_name))
        json_file = open(shot, 'r')
        json_data = json.load(json_file)[0]
        json_file.close()
        try:
            env = json_data['assets']['env']
            if not 'ij_env' in env:
                # print('\t\tFailed to find environment. Skipping.')
                continue
        except:
            # print('\t\tFailed to find environment. Skipping.')
            continue
        env = env.split('ij_env_')[-1]
        env_path = ''
        for asset in list_of_env_assets:
            if env in asset:
                env_path = list_of_env_assets[list_of_env_assets.index(asset)]
                print('\t\tEnvironment Found : {}'.format(env))
                print('\t\tat {}'.format(env_path))
                print('\t\tChecking for camera...')
                cam_search = os.path.join(os.path.dirname(shot), 'shot_data', 'camera_data', 'camera*.abc')
                cam_abc = glob.glob(cam_search)
                if len(cam_abc) > 0:
                    cam_abc.sort()
                    shot_cam_path = cam_abc[-1]
                    print('\t\tFound, at {}'.format(shot_cam_path))
                    print('\t\tMaking a copy in the Asset Folder...')
                    asset_cam_dir = os.path.join(env_path, 'asset_data', 'camera_data')
                    if not os.path.exists(asset_cam_dir):
                        print('\t\t\tPath not created yet. Creating')
                        try:
                            os.mkdir(asset_cam_dir)
                        except:
                            print('ERROR : Failed to create camera_data folder in {}. Exiting.'.format(env_path))
                            sys.exit()
                    else:
                        print('\t\t\tPath exists.')
                    try:
                        asset_cam_path = os.path.join(asset_cam_dir, scene_name + '_' + shot_name + '_camera.abc')
                        shutil.copy2(shot_cam_path, asset_cam_path)
                    except:
                        print('ERROR : Falied to make a copy of the Camera in the Asset folder. Exiting.')
                        sys.exit()

if __name__ == '__main__':
    main()
