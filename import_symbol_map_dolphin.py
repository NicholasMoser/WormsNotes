'''
Takes the symbol map from Ghidra and stores it to the list of symbol maps in Dolphin.
This assumes that the Dolphin folder is in your user's Documents which may not be true if using a newer
version of Dolphin.

It also removes some spacing and adds .text to the beginning to work with Dolphin.
'''
import os
from pathlib import Path
import shutil

home = Path.home()
maps = os.path.join(home, 'Documents/Dolphin Emulator/Maps')
new_map = 'GWME51.map'
temp_map = 'temp.map'

with open(new_map, 'r') as new:
    with open (temp_map, 'w') as temp:
        temp.write('.text\n')
        for line in new.readlines():
            temp.write(line.lstrip())

vanilla_map = os.path.join(maps, 'GWME51.map')
kerfuffle_map = os.path.join(maps, 'GWME52.map')
shutil.copyfile(temp_map, vanilla_map)
shutil.copyfile(temp_map, kerfuffle_map)