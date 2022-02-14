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
import json
import time
import numpy as np
from datetime import date
from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU, GPU

today = date.today()

def dump_aux(orientation, height, grid, erratic, output_dir, relax_time, relax_seed, push_seed):
    """
    Function that reads in auxiliary directory, adds relax_seed and copies file to sim directory

    In push, it reads auxiliary from relax run, and adds push seed. 
    """
    #find aux file from relax
    if erratic:
        relax_dir = f'../../simulations/sys_or{orientation}_hi{height}/relax/erratic/sim_temp{temp}_force{force}_time{relax_time}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}'
    
        auxiliary_relax_dir = relax_dir + \
        f"/system_or{orientation}_hi{height}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}_auxiliary.json"
    
    elif not erratic:
        relax_dir = f'../../simulations/sys_or{orientation}_hi{height}/relax/grid/sim_temp{temp}_force{force}_time{relax_time}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}'

        auxiliary_relax_dir = relax_dir + \
        f"/system_or{orientation}_hi{height}_seed{relax_seed}_grid{grid[0]}_{grid[1]}_auxiliary.json"



    
    #opening auxiliary file, and copying this to the directory
    with open(auxiliary_relax_dir , 'r+') as auxfile:
        data = json.load(auxfile)
        data.update({'push_seed': push_seed})
        auxfile.seek(0) #resets file pointer to beggining of file

    if grid:
        if erratic:
            with open(output_dir +'/system_or{}_hi{}_seed{}_errgrid{}_{}_auxiliary.json'.format(orientation, height, push_seed, grid[0], grid[1]), 'w') as outfile:
                json.dump(data, outfile)
        else:
            with open(output_dir + '/system_or{}_hi{}_seed{}_grid{}_{}_auxiliary.json'.format(orientation, height, push_seed, grid[0], grid[1]), 'w') as outfile:
                json.dump(data, outfile)
    return 1



# user inputs
temp = 2300
#seed = np.random.randint(10000, 100000)
force = 0.001
vel = 5/4
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
prev_push_time = 700 #push time before restart
relax_steps = 500000
#push_steps = 25000 # how long we push for (ps maybe, or timesteps)
push_time = 300 #piko seconds. breaks around 100 acording to even

#fourth push, 700 long
seeds_80 = [97841,88985,79749] #80
seeds_83 = [81474,90347,79290] #83
seeds_85 = [40328,90215,62491,80371,12038,48116] # 85
seeds_90 = [61347,50189,68738, 19022,23781,73474] #90
seeds_95 = [27598,75257,74926, 17821,40450,80080] # 95
seeds_93 = [14130,95349,16972] #93
seeds_100 = [64180,63781,84634, 64308,93573,48127, 78231,43336,42599] # 100
seeds_103 = [28782,23246,41573] # 103
seeds_105 = [48834,99626,28475] # 105
seeds_109 = [89090,40422,52257] #109

seed_dict = {80: seeds_80, 83: seeds_83, 85: seeds_85, 90: seeds_90,
             93: seeds_93, 95: seeds_95, 100: seeds_100, 103: seeds_103,
             105: seeds_105, 109: seeds_109}

for height, seeds in seed_dict.items(): #used: 37144, 48329, 94514


    if erratic:
        push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/erratic/"    
    elif grid:
        push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/grid/"

    else:
        push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"

    for old_push_seed in seeds:
        if grid:
            if erratic:

                restartfile = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{old_push_seed}_errgrid{grid[0]}_{grid[1]}/push_restart.bin"
                
            else:
                restartfile = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{old_push_seed}_grid{grid[0]}_{grid[1]}/push_restart.bin"


        else:
            restartfile = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{old_push_seed}/push_restart.bin"

        var = {'restartfile': f"push_restart.bin",
               'paramfile': "SiC.vashishta",
               'temp': temp,
               'seed': old_push_seed,
               'force': 0.001,
               'simtime': push_time, #even called it simetime, no idea what it is
               'pushtime': relax_steps, #steps until push
               'vel': vel} #m/s

        if grid: #system might not be erratic, but it could still be grid 
            
            if erratic:
                output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}_errgrid{grid[0]}_{grid[1]}/restart_time{push_time}"
                
                sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}_errgrid{grid[0]}_{grid[1]}/restart_time{push_time}", overwrite=True)
                
            else:

                output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}_grid{grid[0]}_{grid[1]}/restart_time{push_time}"

                sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}_grid{grid[0]}_{grid[1]}/restart_time{push_time}", overwrite=True)
        

        else:
            output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}/restart_time{push_time}"

            sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{prev_push_time}_seed{old_push_seed}/restart_time{push_time}", overwrite=True)
        
        #read aux file from relax, write to push directory, append 

        sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta", "sigmoid.py")
        sim.set_input_script(lammps_dir + "in.push", **var)
        
        
        sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'p{old_push_seed}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
