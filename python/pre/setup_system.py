"""
Crystal Aging Project

Script for generating intial system, standard is tiny system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from molecular_builder import write
from pre_utils import gen_system, gen_grid_system, gen_erratic_system
import argparse
import numpy as np
import json

parser = argparse.ArgumentParser()
# user-input
lx = 99.9       # system length x-dir
ly = 100        # system length y-dir
ax = 50         # initial x-coordinate of asperity
ay = 50         # initial y-coordinate of asperity
hl = 50         # height of lower surface/plate
hu = 65         # height of upper surface
hup = 2         # height of upper plate
lz = hl + hu    #total system height
octa_d = 1 * 39.0 #The multiplyer has to be an integer
dode_d = 1 * 37.3

grid = (2,2) 
asperities = 2

lower_orient = "100"
remove_atoms = True
erratic = False

path = '../../initial_system/'

args = {'lx': lx, 'ly':ly, 'ax':ax, 'ay':ay, 'hl':hl, 'hu': hu, 'hup': hup, 'grid': grid, 'asperities':asperities,
        'lower_orient': lower_orient, 'erratic': erratic}

if erratic and grid:
    system = gen_erratic_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                remove_atoms, path, grid=grid, asperities = asperities)

    system_file = path + f"erratic/system_or{lower_orient}_hi{lz}_errgrid{grid[0]}_{grid[1]}"

    system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic') #alternate write method that fixes error?
    print("System written to: ", system_file+'.data')
    with open (system_file +'_auxiliary.json', 'w') as outfile:
        json.dump(args, outfile)
    print('auxiliary datafile written to: ' ,system_file+'_auxiliary.json')  

elif grid:
    system = gen_grid_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                             remove_atoms, path, grid=grid)

    system_file = path + f"grid/system_or{lower_orient}_hi{lz}_grid{grid[0]}_{grid[1]}"
    system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic')

    print("System written to: ", system_file+'.data')
    with open (system_file +'_auxiliary.json', 'w') as outfile:
        json.dump(args, outfile)
    print('auxiliary datafile written to: ' ,system_file+'_auxiliary.json')



else:
    
    system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                        remove_atoms, path)

    system_file = path + f"system_or{lower_orient}_hi{lz}.data"
    system.write(system_file, format="lammps-data", atom_style = 'atomic')

    print("System written to: ", system_file)

