"""
Crystal Aging Project

Get potential energy as a function of time for relaxation simulations.
The potential energy is saved in compressed files.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import re
from glob import glob
from lammps_logfile import File

from post_utils import extract_potential_energy


# user input
temps = range(2000, 2500, 50)
force = 0.001
sim_time = 5000
orientation = "100"
height = 200


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
relax_dir = project_dir + f'simulations/sys_or{orientation}_hi{height}/relax/'
poteng_dir = project_dir + 'txt/poteng/'

template_log = relax_dir + 'sim_temp{}_force{}_time{}_seed{}/log.lammps'
template_poteng = poteng_dir + 'poteng_temp{}_force{}_seed{}.txt'


# read LAMMPS log files
counter = 0
for temp in temps:
    logfiles = template_log.format(temp, force, sim_time, "*")
    for logfile in glob(logfiles):
        print(logfile)
        seed = re.findall('\d+', logfile)[-1]
        outfile = template_poteng.format(temp, force, seed)
        extract_potential_energy(logfile, outfile)
        counter += 1

print(f"Found {counter} logfiles, which corresponds to {counter * 40} simulation hours")
