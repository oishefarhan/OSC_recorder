#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert an osc file to multiple csv files.

Accepts file.osc with contents:
____________________________________________________________________________________________________
osc_time          |path      |types  |packets                                                    
e17775e1.21044f19 |/muse/eeg |ffffff |825.201477 825.201477 825.201477 825.201477 nan 825.201477
e17775e1.21173fb7 |/muse/acc |fff    |0.000000 0.000000 0.000000
----------------------------------------------------------------------------------------------------

Parses and saves to multiple `path`.csv files.
The first column is the corresponding timestamp.

osc_time is in a weird format:
    x.y where x and y are hex numbers.
    x = seconds since 1 Jan 1900
    y = 2**-32 fraction of a second
    Subtract 2,208,988,800 seconds to get unix timestamp
"""
import os
from argparse import ArgumentParser
import numpy as np
from collections import defaultdict

eaxmple_usage = 'Usage: python osc_to_csv.py file.osc -f folder_path'

parser = ArgumentParser(
    description='Convert an osc file to multiple csv files.',
    epilog=eaxmple_usage)
parser.add_argument(
    'file_name', type=str,
    help='osc file captured via: ```oscdump [port] > file.osc```')
parser.add_argument(
    '-f', '--folder', type=str, dest='folder_path',
    help='A folder to place files in.')

args = parser.parse_args()
file_name = args.file_name
folder_path = args.folder_path

path_dict = defaultdict(lambda: [], {})

debug = False
num = 0

with open(file_name, 'r') as osc_file:
    for line in osc_file.readlines():
        line = line.strip('\n')
        osc_time, path, types, packets = line.split(' ', 3)
        x, y = osc_time.split('.')
        float_time = int(x, 16) + int(y,16)/2**32

        path_dict[path] += [[float_time] + [float(pack) for pack in packets.split(' ')]]

        # debug with smaller file size
        if debug:
            if num < 50:
                num = num + 1
            else:
                break

for path, path_list in path_dict.items():
    path = path[1::] if path[0] == '/' else path
    file_name = path.replace('/', '_')+'.csv'
    if folder_path:
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        file_name = os.path.join(folder_path, file_name)
    np.savetxt(file_name, np.array(path_list), delimiter=',')
    print(f'Saved: {file_name}')
print('Done!')
