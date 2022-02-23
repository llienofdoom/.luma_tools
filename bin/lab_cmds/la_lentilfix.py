from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
from posixpath import join, split
import site
import sys
import json
import shutil
import glob

img_path = sys.argv[1]
print('imgpath = ' + img_path)
cp_path = sys.argv[2]
print('cp path = ' + cp_path)
shot_path = sys.argv[3]
print('shot path = ' + shot_path)
hipname = sys.argv[4]
print('hipname = ' + hipname)

origdir = img_path.rsplit('/', 1)[0]
cpdir = cp_path.rsplit('/', 1)[0]
#print('directory' + dir)

path = origdir + '/*main*.exr'
print('path=' + path)
list_of_frames = glob.glob(path)
num = len(list_of_frames)
c = 1
list_of_frames = sorted(list_of_frames)
#print(list_of_frames)

#COPY
for cur in list_of_frames:
    # for file in cur:
    #print('origdir: ' + origdir)
    filename = cur.split('/')[-1]
    currentframe=filename.split('.')[-2] 
    print('Doing frame: ' + filename)
    cp_path = origdir + '/lentil/' + filename
    crypto_path = origdir + '/cryptomatte/' + filename.replace("main","cryptomatte")
    N_path = origdir + '/lentil/' + 'N_noice.' + currentframe + '.exr' 
    Z_path = origdir + '/lentil/' + 'Z_noice.' + currentframe + '.exr'   
    #print('cp path:' + cp_path)
    #print('current"' + cur)
    #shutil.move(cur, cp_path)
    #NORMAL
    os.system('oiiotool %s --ch R,G,B,A,variance.R,variance.G,variance.B,denoise_albedo_noice.R,denoise_albedo_noice.G,denoise_albedo_noice.B %s --ch N_noice.R=N.R,N_noice.G=N.G,N_noice.B=N.B,Z.R,Z.G,Z.B --chappend --chnames R,G,B,A,variance.R,variance.G,variance.B,denoise_albedo_noice.R,denoise_albedo_noice.G,denoise_albedo_noice.B,N_noice.R,N_noice.G,N_noice.B,Z.R,Z.G,Z.B, --attrib "arnold/aovs/RGBA/filter" "RGBA" --attrib "arnold/aovs/variance/filter" "variance_filter" -o %s' % (cur,crypto_path,cp_path))

#FIX
print('done with lentil filter fix')