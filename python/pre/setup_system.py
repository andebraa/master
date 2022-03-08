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

unit_cell = 4.3956

parser = argparse.ArgumentParser()
# user-input
lx = 99.9       # system length x-dir
ly = 100        # system length y-dir
ax = 50         # initial x-coordinate of asperity
ay = 50         # initial y-coordinate of asperity
az = 53         # height of asperity
hl = 20         # height of lower surface/plate
#hup = 9         # thickness of upper plate #thin: 2, thicc: 20, thiccer: 35
#hup = np.arange(5)*unit_cell
num_unit_cells = 5
hup = unit_cell*num_unit_cells 
hu = az+hup         # height of upper surface #thin: 65, thicc: 75, thiccer: 90

lz = hl + hu    #total system height
octa_d = 1 * 39.0 #The multiplyer has to be an integer
dode_d = 1 * 37.3

grid = (4,4) 
porosity = 0.5

asperities = int(grid[0]*grid[1]*porosity)

lower_orient = "100"
remove_atoms = True
erratic = True

seed = np.random.randint(10000, 100000)


path = '../../initial_system/'

args = {'lx': lx, 'ly':ly, 'ax':ax, 'ay':ay, 'hl':hl, 'hu': hu, 'hup': hup, 'grid': grid, 'asperities':asperities,
        'lower_orient': lower_orient, 'erratic': erratic}

if erratic and grid:
    
    system_file = path + f"erratic/gapfix/system_or{lower_orient}_uc{num_unit_cells}_seed{seed}_errgrid{grid[0]}_{grid[1]}_chess"
    aux_path = path + f"erratic/gapfix/aux/system_or{lower_orient}_uc{num_unit_cells}_seed{seed}_errgrid{grid[0]}_{grid[1]}_chess_auxiliary.json"

    system = gen_erratic_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                remove_atoms, aux_path=aux_path, grid=grid, 
                                asperities = asperities, seed = seed)


    system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic') #alternate write method that fixes error?
    print("System written to: ", system_file+'.data')

elif grid:
    system_file = path + f"grid/system_or{lower_orient}_uc{num_unit_cells}_grid{grid[0]}_{grid[1]}"
    aux_path = path + f"grid/aux/system_or{lower_orient}_uc{num_unit_cells}_grid{grid[0]}_{grid[1]}_auxiliary.json"

    system = gen_grid_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                             remove_atoms, aux_path=aux_path, grid=grid)

    system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic')

    print("System written to: ", system_file+'.data')



else:
    
    system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                        remove_atoms, path)

    system_file = path + f"system_or{lower_orient}_uc{num_unit_cells}.data"
    system.write(system_file, format="lammps-data", atom_style = 'atomic')

    print("System written to: ", system_file)

