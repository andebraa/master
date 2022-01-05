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
import numpy as np
from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU, GPU

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
vel = 5
#pushtime = 500000 #timestep to start pushing

height = 90 #90 or 115
orientation = "100"

grid = (4,4)
slurm = True
gpu = True
erratic = True

# paths

project_dir = "../../"
#project_dir = "/home/users/andebraa/master/"
lammps_dir = project_dir + "lammps/"

if erratic:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/erratic/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/erratic/"    
elif grid:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/grid/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/grid/"

else:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"
#print(os.listdir(relax_dir))


# push asperity
relax_time = 1000 #ps time until we push
relax_steps = 500000
#push_steps = 25000 # how long we push for (ps maybe, or timesteps)
push_time = 500 #piko seconds. breaks around 100 acording to even

push_seed = np.random.randint(10000, 100000)

for relax_seed in []: #used: 37144
    
    if grid:
        if erratic:

            restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}/time.{relax_steps}.restart"
        else:
            restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{relax_seed}_grid{grid[0]}_{grid[1]}/time.{relax_steps}.restart"


    else:
        restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{relax_seed}/time.{relax_steps}.restart"

    var = {'restartfile': f"time.{relax_steps}.restart",
           'paramfile': "SiC.vashishta",
           'temp': temp,
           'seed': push_seed,
           'force': 0.001,
           'simtime': push_time, #even called it simetime, no idea what it is
           'pushtime': relax_steps, #steps until push
           'vel': 5} #m/s

    if grid: #system might not be erratic, but it could still be grid 
        
        if erratic:
            output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_errgrid{grid[0]}_{grid[1]}"
            
            sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_errgrid{grid[0]}_{grid[1]}", overwrite=True)

        else:
            output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_grid{grid[0]}_{grid[1]}"

            sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_grid{grid[0]}_{grid[1]}", overwrite=True)
    

    else:
        output_dir = push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_steps}_seed{push_seed}"

        sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_steps}_seed{push_seed}", overwrite=True)
    
    #read aux file from relax, write to push directory, append 

    sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta", "sigmoid.py")
    sim.set_input_script(lammps_dir + "in.push", **var)
    
    dump_aux(orientation, height, grid, erratic, output_dir, relax_time, relax_seed, push_seed)
    
    sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'{int(temp/100)}_{relax_steps}_{push_seed}_erratic{erratic}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
