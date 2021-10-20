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
pushtime = 10000 #how long to push for
seed = 19970

height = 115
orientation = "100"

grid = (3,3)
slurm = True
gpu = True
erratic = True

# paths

project_dir = "../../"
#project_dir = "/home/users/andebraa/master/"
lammps_dir = project_dir + "lammps/"

if erratic:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"    
elif grid:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"

else:
    relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
    push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"
print(os.listdir(relax_dir))


# push asperity
relax_time = 100000
relax_time_restart = 955000
for seed in [41162]:
    
    if grid:
        restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}_grid{grid[0]}_{grid[1]}/time.{relax_time_restart}.restart"

    elif erratic:
        restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}_errgrid{grid[0}_{grid[1]}/time.{relax_time_restart}.restart"

    else:
        restartfile = relax_dir + f"sim_temp{temp}_force{force}_time{relax_time}_seed{seed}/time.{relax_time_restart}.restart"

    var = {'restartfile': f"time.{relax_time_restart}.restart",
           'paramfile': "SiC.vashishta",
           'temp': temp,
           'seed': seed,
           'force': 0.001,
           'simtime': pushtime,
           'pushtime': relax_time}

    if erratic:
        sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{seed}_errgrid{grid[0]}_{grid[1]}", overwrite=True)
    
    elif grid: #system might not be erratic, but it could still be grid 
        sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{seed}_grid{grid[0]}_{grid[1]}", overwrite=True)

    else:
        sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{relax_time}_seed{seed}", overwrite=True)
    
    sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta", "sigmoid.py")
    sim.set_input_script(lammps_dir + "in.push", **var)
    sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'{int(temp/100)}_{int(relax_time)}_{seed}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
