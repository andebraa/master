"""
Crystal Aging Project

Script for generating intial system, standard is tiny system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""
#TODO can this script replace or merge with grid setup0?
from molecular_builder import write
from pre_utils import gen_grid_system, erratic_setup
import numpy as np

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

grid = (4,4) 

lower_orient = "100"
remove_atoms = True
erratic = True

path = '../../initial_system/'


if erratic:
    system = erratic_setup(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                           remove_atoms, path, grid=grid)

    print(system)
    system.set_cell(np.diag(np.max(system.positions, axis=0)))
    system.wrap()

    system_file = path + f"erratic/system_or{lower_orient}_hi{lz}_errgrid{grid[0]}_{grid[1]}.data"


    write(system, system_file)
    #system.write(system_file, format="lammps-data") #alternate write method that fixes error?
    print("System written to: ", system_file)

elif grid:
    system = gen_grid_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                             remove_atoms, path, grid=grid)

    system_file = path + f"grid/system_or{lower_orient}_hi{lz}_grid{grid[0]}_{grid[1]}.data"
    system.write(system_file, format="lammps-data")
    print("System written to: ", system_file)

else:
    
    system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                        remove_atoms, path)

    system_file = path + f"system_or{lower_orient}_hi{lz}.data"
    system.write(system_file, format="lammps-data")
    #write(system, system_file)
    print("System written to: ", system_file)


#print(system)
#system.set_cell(np.diag(np.max(system.positions, axis=0)))
#system.wrap()
##system_file = path + f"system_or{lower_orient}_hi{lz}_grid{grid[0]}_{grid[1]}.data"
#write(system, system_file)
##system.write(system_file, format="lammps-data")
##print("System written to: ", system_file)


