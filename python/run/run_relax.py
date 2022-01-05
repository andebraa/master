"""
Adjust the boolean variables slurm, gpu and erratic. 
If erratic, the script finds all init files with given grid and asks you to input the seed you want.

Init seeds and run seeds are not the same!
"""
import time
import json
import glob
import re
import os
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
erratic = False

relax_seed = np.random.randint(10000, 100000)


# paths
#project_dir = "/run/user/1004/andebraa_masterdata/"
project_dir = '../../'
lammps_dir = project_dir + "lammps/"
relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
init_dir = project_dir + f"initial_system/"

init_auxiliary = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_seed{}_errgrid{}_{}_auxiliary.json'

def dump_aux(orientation, height, grid, erratic, output_dir, relax_seed, init_seed = 0):
    """
    Function that reads in auxiliary directory, adds relax_seed and copies file to sim directory,
    note; should not alter init auxiliary
    """

    #opening auxiliary file, and copying this to the directory
    with open(init_auxiliary.format(orientation, height, init_seed, grid[0], grid[1], 'r+')) as auxfile:
        data = json.load(auxfile)
        data.update({'relax_seed': relax_seed})
        auxfile.seek(0) #resets file pointer to beggining of file

    if grid:
        if erratic:
            output_aux = output_dir +'/system_or{}_hi{}_seed{}_errgrid{}_{}_auxiliary.json'.format(orientation, 
                                                                                                   height, 
                                                                                                   relax_seed,
                                                                                                   grid[0], 
                                                                                                   grid[1])

            with open(output_aux, 'w') as outfile:
                json.dump(data, outfile)
        
        else: 
            output_aux = output_dir + '/system_or{}_hi{}_seed{}_grid{}_{}_auxiliary.json'.format(orientation, 
                                                                                                 height, 
                                                                                                 relax_seed,
                                                                                                 grid[0], 
                                                                                                 grid[1])
            with open(output_aux, 'w') as outfile:
                
                json.dump(data, outfile)
    return 1


# Finding the init datafile
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


var = {'datafile': datafile.split("/")[-1],
       'paramfile': "SiC.vashishta",
       'temp': temp,
       'seed': relax_seed,
       'force': force,
       'simtime': simtime,
       'freq': int(int(simtime/0.002)/num_restart_points), #timesteps
       'height': height}



# Initializing the run with correct output script
if erratic:
    output_dir = directory=relax_dir + \
    f"erratic/sim_temp{temp}_force{force}_time{simtime}_seed{relax_seed}_errgrid{grid[0]}_{grid[1]}"
    
    sim = Simulator(directory = output_dir, overwrite=True)

elif grid:
    output_dir = relax_dir + \
            f"grid/sim_temp{temp}_force{force}_time{simtime}_seed{relax_seed}_grid{grid[0]}_{grid[1]}"
    sim = Simulator(directory=output_dir, overwrite=True)

else:
    output_dir = relax_dir + f"sim_temp{temp}_force{force}_time{simtime}_seed{relax_seed}"
    sim = Simulator(directory= output_dir, overwrite=True)

sim.copy_to_wd(datafile, lammps_dir + "SiC.vashishta")
sim.set_input_script(lammps_dir + "in.relax", **var)

#make the output directory, so we can write aux before run
#os.mkdir(output_dir)

#read aux from init and copy to sim folder whilst appending relax_seed
if grid and erratic:
    dump_aux(orientation, height, grid, erratic, output_dir, relax_seed, init_seed) 
elif erratic:
    dump_aux(orientation, height, grid, erratic, output_dir, relax_seed) 
    

# calling lammps simulator dependent on erratic or grid
if erratic:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                    slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{relax_seed}_errgrid{grid[0]}_{grid[1]}'}, 
                    lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)
    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)

elif grid:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                                      slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{relax_seed}_grid{grid[0]}_{grid[1]}'}, 
                                      lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)
    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)

else:
    if gpu:
        if slurm:
            sim.run(computer=SlurmGPU(lmp_exec="lmp_python", 
                slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{relax_seed}'}, 
                lmp_args={'-pk': 'kokkos newton on neigh full'}))
        else:
            sim.run(computer=GPU(lmp_exec = 'lmp_python'), stdout = None)

    else:
        sim.run(computer=CPU(num_procs=2, lmp_exec="lmp"), stdout=None)
