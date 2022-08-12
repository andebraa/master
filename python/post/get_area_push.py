"""
Crystal Aging Project

Get contact area and number of atoms in the contact
region while asperity moves. 

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import re
from glob import glob
from post_utils import get_contact_area

# user input
orientation = "110"
height = 200  # Å
force = 0.001 # eV/Å
vel = 5


# paths
project_dir = '../../'
push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
area_push_dir = project_dir + 'txt/area_push/'
coordination_dir = project_dir + 'txt/coordination/'

template = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}/dump.bin'


temps = [2300]
for temp in temps:
    dumpfiles = template.format(orientation, height, temp, vel, force, "*", "*")
    print(dumpfiles)
    for dumpfile in glob(dumpfiles):
        print(dumpfile)
        matches = re.findall('\d+', dumpfile)
        seed = matches[-1]
        time = matches[-2]
        get_contact_area(dumpfile, area_push_dir + f"areas_{temp}K_55_hi{height}_or{orientation}_time{time}_seed{seed}.txt",
                     delta=5/1000)
