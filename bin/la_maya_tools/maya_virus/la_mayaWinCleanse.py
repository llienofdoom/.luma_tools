import os
import sys
# import glob

try :
    root = os.environ['HOMEPATH']
except:
    print('Failed to get Environment')
    sys.exit()

doc_path = os.path.join('C:', root, 'Documents', 'maya')
search_path = doc_path + '\\**\\*.py*'

list_of_offending_files = []
for dirpath, dirs, files in os.walk(doc_path):
    for filename in files:
        if '.py' in filename:
            path = os.path.join(dirpath, filename)
            list_of_offending_files.append(path)

if len(list_of_offending_files) > 0:
    for f in list_of_offending_files:
        if 'usersetup.' in f.lower():
            print('Found userSetup.py, %s' % f)
            new_name = os.path.basename(f).split('.')[0] + '_ORIGINAL.' + os.path.basename(f).split('.')[-1]
            print('Rename old userSetup.py to ORIG.')
            os.system('ren %s %s' % (f, new_name))
            print('Make ORIG read only..')
            os.system('attrib +R %s' % os.path.join(os.path.dirname(f), new_name))
            print('make new empty userSetup.py.')
            os.system('type nul > %s' % f)

            print('Rename new userSetup.py to read only.')
            os.system('attrib +R %s' % f)
        if 'vaccine' in f.lower():
            print('Found vaccine.py, %s. Removing.' % f)
            os.remove(f)
else:
    print('No Files in list.')