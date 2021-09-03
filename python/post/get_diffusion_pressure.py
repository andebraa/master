"""
Crystal Aging Project

Get diffusion coefficient and normal pressure as a function of time
for relaxation simulations. The potential energy is saved in compressed
files.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import re
from glob import glob
from lammps_logfile import File

from post_utils import extract_diffusion_coefficient, extract_normal_pressure


# user input
temps = [2000]  # range(2000, 2500, 50)
force = 0.001
sim_time = 5000
orientation = "100"
height = 200


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
relax_dir = project_dir + f'simulations/sys_or{orientation}_hi{height}/relax/'
diff_dir = project_dir + 'txt/diffusion/'
press_dir = project_dir + 'txt/pressure/'

template_log = relax_dir + 'sim_temp{}_force{}_time{}_seed{}/log.lammps'
template_diff = diff_dir + 'diffusion_temp{}_force{}_seed{}.txt'
template_press = press_dir + 'pressure_temp{}_force{}_seed{}.txt'


# read LAMMPS log files
for temp in temps:
    logfiles = template_log.format(temp, force, sim_time, "*")
    for logfile in glob(logfiles):
        print(logfile)
        seed = re.findall('\d+', logfile)[-1]
        difffile = template_diff.format(temp, force, seed)
        pressfile = template_press.format(temp, force, seed)
        try:
            extract_diffusion_coefficient(logfile, difffile)
        except:
            pass
        try:
            extract_normal_pressure(logfile, pressfile)
        except:
            pass
