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
init_dir = project_dir + f"initial_system/"

init_auxiliary = project_dir + 'initial_system/erratic/aux/system_or{}_uc{}_seed{}_errgrid{}_{}_auxiliary.json'
def dump_aux(orientation, uc, grid, erratic, output_dir, seed, init_seed = 0):
    """
    Function that reads in auxiliary directory, adds relax_seed and copies file to sim directory,
    note; should not alter init auxiliary
    """
    init_auxiliary = project_dir + 'initial_system/erratic/aux/system_or{}_uc{}_seed{}_errgrid{}_{}_auxiliary.json'

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

def fetch_initial_system():
    '''
    all initial systems without symmetries etc are assumed to be located at 
    ~/master/initial_system/production
    '''

    random.choice(os.listdir('~/master/initial_system/production'))



# user inputs
temp = 2300
#seed = np.random.randint(10000, 100000)
force = 0.001
vel = 5
#pushtime = 500000 #timestep to start pushing

#height = 109 #90, 95, 110 or 115
orientation = "100"

grid = (4,4)
slurm = True
gpu = True
erratic = True

# paths

project_dir = "../../"
#project_dir = "/home/users/andebraa/master/"
lammps_dir = project_dir + "lammps/"


# push asperity
relax_time = 500 #ps time until we push
relax_steps = 83333
#push_steps = 25000 # how long we push for (ps maybe, or timesteps)
push_time = 700 #piko seconds. breaks around 100 acording to even


seed_dict = {5: [72208]}

run_number = 4 #which run is this

for uc, seeds in seed_dict.items(): #used: 37144, 48329, 94514


    if erratic:
        push_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/production"
    elif grid:
        relax_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/relax/grid/"
        push_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/push/grid/"

    else:
        relax_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/relax/"
        push_dir = project_dir + f"simulations/sys_or{orientation}_uc{uc}/push/"

    for seed in seeds:
        push_seed = np.random.randint(10000, 100000)
        print(uc, push_seed)
        if grid:
            if erratic:

                restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}_errgrid{grid[0]}_{grid[1]}/time.{relax_steps}.restart"
                
            else:
                restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}_grid{grid[0]}_{grid[1]}/time.{relax_steps}.restart"


        else:
            restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}/time.{relax_steps}.restart"

        var = {'restartfile': f"time.{relax_steps}.restart",
               'paramfile': "SiC.vashishta",
               'temp': temp,
               'seed': push_seed,
               'force': force,
               'reltime': rel_time, #time to relax
               'pushtime': push_time, #time for push
               'pushtime': relax_steps, #steps until push
               'vel': vel} #m/s

        if grid: #system might not be erratic, but it could still be grid 
            
            if erratic:
                output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_errgrid{grid[0]}_{grid[1]}"
                
                sim = Simulator(directory=output_dir, overwrite=True)
                
                runlogger('push', uc, temp, 0, force, push_time, relax_seed, grid = 'erratic', push_seed = 'relaxpush')
            else:

                output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_grid{grid[0]}_{grid[1]}"

                sim = Simulator(directory=output_dir, overwrite=True)
        

                runlogger('push', uc, temp, 0, force, pushtime, relax_seed, grid = 'grid', push_seed = 'relaxpush')
                #with open(project_dir + f'runs/push/grid/run_{run_number}.csv', 'a') as file_object:
                #    file_object.write(str(height) + ', ' +str(relax_seed) +'\n')

        else:
            output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_steps}_seed{push_seed}"

            sim = Simulator(directory=output_dir, overwrite=True)
        
            runlogger('push', uc, temp, 0, force, push_time, relax_seed, grid = 'single', push_seed = 'relaxpush')
        #read aux file from relax, write to push directory, append 

        sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta")
        sim.set_input_script(lammps_dir + "in.relaxpush", **var)
        
        dump_aux(orientation, uc, grid, erratic, output_dir, relax_time, relax_seed, push_seed)
        
        sim.run(computer=SlurmGPU(lmp_exec="lmp_test", slurm_args={'job-name': f'p{push_seed}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))

