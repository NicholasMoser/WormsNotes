import os
import subprocess
import sys
from tqdm import tqdm

xom2xml = 'Xom2Xml.exe'
xomschm = 'XOMSCHM.dat'

# Script setup and input validation
if not os.path.isfile(xom2xml):
    print(f'Missing {xom2xml}, download from https://github.com/AlexBond2/Xom2Xml/releases')
    sys.exit(1)
if not os.path.isfile(xomschm):
    print(f'Missing {xomschm}, download from https://github.com/AlexBond2/Xom2Xml/releases')
    sys.exit(1)
if len(sys.argv) < 2:
    print(f'Please provide a directory to extract from, for example:')
    print(f'python extract_all_xom.py C:/Worms3D')
    sys.exit(1)
directory = sys.argv[1]
if not os.path.isdir(directory):
    print(f'{directory} is not a directory')
    sys.exit(1)

# Get all xom files
xoms = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.xom'):
            file_path = os.path.join(root, file)
            xoms.append(file_path)

# Run script
for xom in tqdm(xoms):
    head, tail = os.path.split(xom)
    output_dir = tail.replace('.xom', '')
    try:
        # TODO: Most files fail and none extract the image
        subprocess.check_output([xom2xml, xom, '-ximg-file', 'tg', '-ximg-dir', output_dir])
    except:
        print('error')

# Error checking
for xom in xoms:
    if not os.path.isfile(xom.replace('.xom', '.xml')):
        print(f'Failed to convert {xom}')
