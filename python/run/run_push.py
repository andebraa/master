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
import numpy as np
from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU, GPU


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

for relax_seed in [53538]:
    
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
            print(push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_errgrid{grid[0]}_{grid[1]}")
            
            sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_errgrid{grid[0]}_{grid[1]}", overwrite=True)

        else:
            sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{push_time}_seed{push_seed}_grid{grid[0]}_{grid[1]}", overwrite=True)
    

    else:
        sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_steps}_seed{push_seed}", overwrite=True)
    
    sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta", "sigmoid.py")
    sim.set_input_script(lammps_dir + "in.push", **var)
    sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'{int(temp/100)}_{relax_steps}_{push_seed}_erratic{erratic}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
