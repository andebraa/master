"""
Adjust the boolean variables slurm, gpu and erratic. 
If erratic, the script finds all init files with given grid and asks you to input the seed you want.

Init seeds and run seeds are not the same!
"""
import time
import json
import glob
import re
import numpy as np
from lammps_simulator import Simulator
from lammps_simulator.computer import GPU, CPU, SlurmGPU

#dt = 0.002
#number of timesteps is simtime/dt
# User input
temp = 2300
simtime = 1000 #picosekunder
force = 0.001
height = 90
orientation = "100"
num_restart_points = 5

grid = (4,4) 
slurm = True
gpu = True
erratic = True

seed = np.random.randint(10000, 100000)

# paths
#project_dir = "/run/user/1004/andebraa_masterdata/"
project_dir = '../../'
lammps_dir = project_dir + "lammps/"
relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
init_dir = project_dir + f"initial_system/"


if erratic:
    #finding all files in directory, printing the seeds and having user write in desired seed
    template_dump = init_dir +f"erratic/system_or{orientation}_hi{height}_seed*_errgrid{grid[0]}_{grid[1]}.data"
    print(template_dump)
    init_seeds = glob.glob(template_dump)
   
    if not init_seeds:
        raise IndexError('no files found')
    
    for init_seed in init_seeds:
        print(re.findall('\d+', init_seed)[-3])

    init_seed = input('select seed ')
    
    datafile = project_dir + f"initial_system/erratic/system_or{orientation}_hi{height}_seed{init_seed}_errgrid{grid[0]}_{grid[1]}.data"
    #datafile = project_dir + f"initial_system/erratic/system_or{orientation}_hi{height}_rep{grid[0]}{grid[1]}_removed00.data"

    print(datafile)

elif grid:

    datafile = project_dir + f"initial_system/grid/system_or{orientation}_hi{height}_grid{grid[0]}_{grid[1]}.data"
    print(datafile)

else:
    datafile = project_dir + f"initial_system/system_or{orientation}_hi{height}.data"
    print(datafile)    

# run relaxation
var = {'datafile': datafile.split("/")[-1],
       'paramfile': "SiC.vashishta",
       'temp': temp,
       'seed': seed,
       'force': force,
       'simtime': simtime,
       'freq': int(int(simtime/0.002)/num_restart_points), #timesteps
       'height': height}
if erratic:
    sim = Simulator(directory=relax_dir + \
            f"sim_temp{temp}_force{force}_time{simtime}_seed{seed}_errgrid{grid[0]}_{grid[1]}", overwrite=True)

elif grid:
    sim = Simulator(directory=relax_dir + \
            f"sim_temp{temp}_force{force}_time{simtime}_seed{seed}_grid{grid[0]}_{grid[1]}", overwrite=True)

else:
    sim = Simulator(directory=relax_dir + f"sim_temp{temp}_force{force}_time{simtime}_seed{seed}", overwrite=True)

sim.copy_to_wd(datafile, lammps_dir + "SiC.vashishta")
sim.set_input_script(lammps_dir + "in.relax", **var)

if erratic:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                    slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{seed}_errgrid{grid[0]}_{grid[1]}'}, 
                    lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)
    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)

elif grid:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                                      slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{seed}_grid{grid[0]}_{grid[1]}'}, 
                                      lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)
    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)

else:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{seed}'}, 
                lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)

    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)
