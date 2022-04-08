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
temps = [2300]  # range(2000, 2500, 50)
grid = (4,4)
force = 0.001
sim_time = 5000
orientation = "100"
uc = 5
asperities = 2

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
relax_dir = project_dir + f'simulations/sys_asp{asperities}_uc{uc}/production/'
diff_dir = project_dir + 'txt/diffusion/'
press_dir = project_dir + 'txt/pressure/'

template_log = relax_dir + 'sim_temp{}_force{}_asp{asperities}_time{}_initnum{}_errgrid{}_{}/log.lammps'
template_diff = diff_dir + 'diffusion_temp{}_force{}_initnum{}.txt'
template_press = press_dir + 'pressure_temp{}_force{}_initnum{}.txt'


# read LAMMPS log files
for initnum in range(0,4):
    logfiles = template_log.format(temp, force, asperities, sim_time, initnum, grid[0], grid[1])
    for logfile in glob(logfiles):
        print(logfile)
        seed = re.findall('\d+', logfile)[-1]
        difffile = template_diff.format(temp, force, seed)
        pressfile = template_press.format(temp, force, seed)
        try:
            extract_diffusion_coefficient(logfile, difffile)
        except:
            print('pass')
            pass
        try:
            extract_normal_pressure(logfile, pressfile)
        except:
            print('pass')
            pass
