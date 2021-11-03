"""
Crystal Aging Project

This script runs LAMMPS simulations where the system
is relaxed. 

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
from lammps_simulator import Simulator
from lammps_simulator.computer import GPU, CPU, SlurmGPU


# User input
temp = 2300
simtime = 20000
force = 0.001
height = 100
orientation = "100"

seed = np.random.randint(10000, 100000)


# paths
project_dir = "../../"
lammps_dir = project_dir + "lammps/"
relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"

datafile = project_dir + f"initial_system/system_or{orientation}_hi{height}.data"



# run relaxation
var = {'datafile': datafile.split("/")[-1],
       'paramfile': "SiC.vashishta",
       'temp': temp,
       'seed': seed,
       'force': force,
       'simtime': simtime,
       'freq': 5000,
       'height': height}

sim = Simulator(directory=relax_dir + f"sim_temp{temp}_force{force}_time{simtime}_seed{seed}", overwrite=True)
sim.copy_to_wd(datafile, lammps_dir + "SiC.vashishta")
sim.set_input_script(lammps_dir + "in.relax", **var)
#sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'N{int(temp/100)}_{int(force*1000)}_{seed}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
sim.run(computer=CPU(num_procs=3, lmp_exec="lmp_python"), stdout=None)
#sim.run(computer=GPU(lmp_exec="lmp_python"), stdout=None)
