"""
Crystal Aging Project

This script run simulations where the asperity is moved with
constant velocity after relaxation.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.

No grid or erratic -> original even simulation with single asperity
erratic has random erratic configuration of asperities
grid has all asperities

"""
import os
import sys
import json
import time
import random
import numpy as np
from datetime import date
from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU, GPU
sys.path.insert(0,'/home/users/andebraa/master/python')
from runlogger import runlogger

today = date.today()

# paths
#project_dir = "/run/user/1004/andebraa_masterdata/"
project_dir = '../../'
lammps_dir = project_dir + "lammps/"
relax_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/relax/"
init_dir = project_dir + f"initial_system/production"

init_auxiliary = project_dir + 'initial_system/production/erratic/aux/system_or{}_uc{}_seed{}_errgrid{}_{}_auxiliary.json'
def dump_aux(orientation, uc, grid, erratic, output_dir, seed, init_seed = 0):
    """
    Function that reads in auxiliary directory, adds relax_seed and copies file to sim directory,
    note; should not alter init auxiliary
    """
    init_auxiliary = project_dir + 'initial_system/production/erratic/aux/system_or{}_uc{}_seed{}_errgrid{}_{}_auxiliary.json'

    #opening auxiliary file, and copying this to the directory
    with open(init_auxiliary.format(orientation, uc, init_seed, grid[0], grid[1], 'r+')) as auxfile:
        data = json.load(auxfile)
        data.update({'seed': seed})
        auxfile.seek(0) #resets file pointer to beggining of file

    if grid:
        if erratic:
            output_aux = output_dir +'/system_or{}_uc{}_seed{}_errgrid{}_{}_auxiliary.json'.format(orientation, 
                                                                                                   uc, 
                                                                                                   seed,
                                                                                                   grid[0], 
                                                                                                   grid[1])

            with open(output_aux, 'w') as outfile:
                json.dump(data, outfile)
        
        else: 
            output_aux = output_dir + '/system_or{}_uc{}_seed{}_grid{}_{}_auxiliary.json'.format(orientation, 
                                                                                                 uc, 
                                                                                                 seed,
                                                                                                 grid[0], 
                                                                                                 grid[1])
            with open(output_aux, 'w') as outfile:
                
                json.dump(data, outfile)
    return 1

def fetch_initial_system(run_num = 0, random_choice = False):
    '''
    all initial systems without symmetries etc are assumed to be located at 
    ~/master/initial_system/production
    '''
    if random_choice:
        initfile = random.choice(os.listdir('~/master/initial_system/production'))
    else:
        initfile = f'system_or{orientation}_uc{uc}_initnum{initnum}_errgrid{grid[0]}_{grid[1]}.data' 
    
    return initfile



def run_relaxpush(init_num = 0, run_num = 0):
    temp = 2300
    reltime = 200 #picosekunder
    pushtime = 200
    force = 0

    orientation = "100"
    num_restart_points = 3


    unit_cell = 4.3596
    uc = 5 #unit cells height


    height = uc*unit_cell+20+51

    grid = (4,4) 
    slurm = True
    gpu = True
    erratic = True

    
    # paths
    #project_dir = "/run/user/1004/andebraa_masterdata/"
    project_dir = '../../'
    lammps_dir = project_dir + "lammps/"
    output_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/production/"
    init_dir = project_dir + f"initial_system/production"

    init_auxiliary = project_dir + 'initial_system/erratic/aux/system_or{}_uc{}_seed{}_errgrid{}_{}_chess_auxiliary.json'

    # Finding the init datafile
    #finding all files in directory, printing the seeds and having user write in desired seed
    template_dump = init_dir +f"erratic/system_or{orientation}_uc{uc}_initnum{init_num}_errgrid{grid[0]}_{grid[1]}.data"
   
    if not template_dump:
        raise IndexError('no files found')
    
    
    datafile = fetch_initial_system(run_num, random_choice=False
    print(datafile)


    var = {'datafile': datafile.split("/")[-1],
           'paramfile': "SiC.vashishta",
           'temp': temp,
           'init_num': init_num,
           'force': force,
           'freq': int(int(simtime/0.002)/num_restart_points), #timesteps
           'height': height,
           'vel': vel,
           'relaxtime': relax_time,
           'pushtime': push_time}




    # Initializing the run with correct output script
    sim_dir = relax_dir + \
    f"erratic/sim_temp{temp}_force{force}_time{simtime}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}_chess"
    
    sim = Simulator(directory = sim_dir, overwrite=True)


    sim.copy_to_wd(datafile, lammps_dir + "SiC.vashishta")
    sim.set_input_script(lammps_dir + "in.relaxpush", **var)

    #read aux from init and copy to sim folder whilst appending relax_seed
    dump_aux(orientation, uc, grid, erratic, output_dir, run_num) 
        

    # calling lammps simulator dependent on erratic or grid
    sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
            slurm_args={'job-name': f'prod#{run_num}'}, 
            lmp_args={'-pk': 'kokkos newton on neigh full'}))
    runlogger('relaxpush', uc, temp, 0, force, simtime, relax_seed, grid = 'production', push_seed = run_num)


if __name__ == '__main__':
    run_relaxpush()
