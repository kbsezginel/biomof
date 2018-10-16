"""
python change_coordinates.py IRMOF-1-222.cif 37 new.cif
"""
import os
import sys


filename = sys.argv[1]
coor_start = int(sys.argv[2])
new_file = sys.argv[3]


def change_coor(coor):
    """ Change coordinate using any operation here """
    return float(coor) / 2


with open(filename, 'r') as f:
    cif_lines = f.readlines()

coor_end = cif_lines.index('#END\n')

new_lines = cif_lines[:coor_start]
for line in cif_lines[coor_start:coor_end - 1]:
    atom_id, element, x, y, z = line.split()
    nx, ny, nz = [change_coor(i) for i in [x, y, z]]
    new_lines.append('%-6s %-2s  %-7.4f  %-7.4f  %-7.4f\n' % (atom_id, element, nx, ny, nz))

new_lines += ['\n', '#END\n']

with open(new_file, 'w') as nf:
    for line in new_lines:
        nf.write(line)
print('Done!')
