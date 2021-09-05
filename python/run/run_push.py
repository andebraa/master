"""
Crystal Aging Project

This script run simulations where the asperity is moved with
constant velocity after relaxation.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU, GPU


# user inputs
temp = 2200
#seed = np.random.randint(10000, 100000)
force = 0.001
vel = 5
simtime = 5
#seed_prev = 10989

height = 110
orientation = "100"


# paths
project_dir = "../../"
lammps_dir = project_dir + "lammps/"
relax_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/relax/"
push_dir = project_dir + f"simulations/sys_or{orientation}_hi{height}/push/"


# push asperity
time = 250
for seed in [19472, 22162, 38661, 64074, 77815]:
    restartfile = relax_dir + f"sim_temp{temp}_force{force}_time5000_seed{seed}/time.{time}.restart"

    var = {'restartfile': f"time.{time}.restart",
           'paramfile': "SiC.vashishta",
           'temp': temp,
           'seed': seed,
           'force': force,
           'vel': vel,
           'simtime': simtime,
           'pushtime': time}

    sim = Simulator(directory=push_dir + f"sim_temp{temp}_vel{vel}_force{force}_time{time}_seed{seed}", overwrite=True)
    sim.copy_to_wd(restartfile, lammps_dir + "SiC.vashishta", "sigmoid.py")
    sim.set_input_script(lammps_dir + "in.push", **var)
    sim.run(computer=SlurmGPU(lmp_exec="lmp_python", slurm_args={'job-name': f'{int(temp/100)}_{int(time)}_{seed}'}, lmp_args={'-pk': 'kokkos newton on neigh full'}))
