"""
Crystal Aging Project

Get load curves from push simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from glob import glob
from post_utils import extract_load_curves


# user input
temp = 2300
orientation = "100"
height = 200
vel = 5
force = 0.001


# paths
project_dir = '../../'
push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
lc_dir = project_dir + 'txt/load_curves/'
ms_dir = project_dir + 'txt/max_static/'

template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}/log.lammps'
template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}.txt'
template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}.txt'


# collect log files
times = [50000, 100000, 500000, 1000000, 5000000, 10000000]
times = range(125000, 2500001, 125000) 
seeds = [35183, 69877, 83182, 92410]
seeds = [17361, 29464, 55979, 57200, 90536]

for seed in seeds:
    logfiles = []
    for time in times:
        print(f"seed: {seed}   time: {time}")
        logfile = template_logfiles.format(orientation, height, temp, vel, force, time, seed)
        logfiles.append(logfile)


    # extract load curves
    extract_load_curves(logfiles, None, 0, 5000, template_lc.format(temp, vel, force, orientation, seed),
                        template_ms.format(temp, vel, force, orientation, seed))

