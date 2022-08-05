"""
Crystal Aging Project

Script for generating intial system, standard is tiny system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""
import sys 
from molecular_builder import write
from pre_utils import gen_system, gen_grid_system, gen_erratic_system
import argparse
import numpy as np
import json

sys.path.insert(0,'/home/users/andebraa/master/python')
from runlogger import runlogger

def setup_system(production = False, init_num = 0, asperities = 2): 

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

    lower_orient = "110"
    remove_atoms = False
    erratic = True

    seed = np.random.randint(10000, 100000)


    path = '../../initial_system/'

    args = {'lx': lx, 'ly':ly, 'ax':ax, 'ay':ay, 'hl':hl, 'hu': hu, 'hup': hup, 'grid': grid, 'asperities':asperities,
            'lower_orient': lower_orient, 'erratic': erratic}

    if production or isinstance(production, np.ndarray):
        print('------------------------production run--------------------')
        system_file = path + f"production/erratic/system_asp{asperities}_or{lower_orient}_uc{num_unit_cells}_initnum{init_num}_errgrid{grid[0]}_{grid[1]}"
        aux_path = path + f"production/erratic/aux/system_asp{asperities}_or{lower_orient}_uc{num_unit_cells}_initnum{init_num}_errgrid{grid[0]}_{grid[1]}_auxiliary.json"

        system = gen_erratic_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                    remove_atoms, aux_path=aux_path, grid=grid, 
                                    asperities = asperities, seed = seed, production = production)


        system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic') #alternate write method that fixes error?

        print("System written to: ", system_file+'.data')
        runlogger('init', num_unit_cells, 0, 0, 0, 0,relax_seed = seed, grid= 'production', push_seed = 0)

    else:
        if erratic and grid:
            
            system_file = path + f"erratic/system_asp{asperities}_or{lower_orient}_uc{num_unit_cells}_seed{seed}_errgrid{grid[0]}_{grid[1]}"
            aux_path = path + f"erratic/aux/system_asp{asperities}_or{lower_orient}_uc{num_unit_cells}_seed{seed}_errgrid{grid[0]}_{grid[1]}_auxiliary.json"

            system = gen_erratic_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                        remove_atoms, aux_path=aux_path, grid=grid, 
                                        asperities = asperities, seed = seed, production = production)


            system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic') #alternate write method that fixes error?

            print("System written to: ", system_file+'.data')
            runlogger('init', num_unit_cells, 0, 0, 0, 0,relax_seed = seed, grid= 'erratic', push_seed = 0)

        elif grid:
            system_file = path + f"grid/system_asp{asperities}_uc{num_unit_cells}_grid{grid[0]}_{grid[1]}"
            aux_path = path + f"grid/aux/system_asp{asperities}_uc{num_unit_cells}_grid{grid[0]}_{grid[1]}_auxiliary.json"

            system = gen_grid_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                     remove_atoms, aux_path=aux_path, grid=grid)

            system.write(system_file +'.data', format="lammps-data", atom_style = 'atomic')

            print("System written to: ", system_file+'.data')


            runlogger('init', num_unit_cells, 0, 0, 0, 0, relax_seed = seed, grid = 'grid', push_seed = 0)

        else:
            
            system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                remove_atoms, path)

            system_file = path + f"system_asp{asperities}_uc{num_unit_cells}.data"
            system.write(system_file, format="lammps-data", atom_style = 'atomic')

            print("System written to: ", system_file)

            runlogger('init', num_unit_cells, 0, 0, 0, seed, 'single', 0, asperities)
if __name__ == '__main__':
    setup_system(asperities=8)
