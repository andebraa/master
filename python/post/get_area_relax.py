"""
Crystal Aging Project

Get contact area and number of atoms in the contact
region during relaxation. 

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""


import re
from glob import glob
from post_utils import get_contact_area
from post_utils import count_coord

# user input
orientation = "100"
height = 110  # Å
force = 0.001 # eV/Å
time = 500   # ps
#grid = (3,3)

# paths
project_dir = '../../'
relax_dir = project_dir + 'simulations/sys_or{}_hi{}/relax/'
area_relax_dir = project_dir + 'txt/area_relax/'
coordination_dir = project_dir + 'txt/coordination/'

template_dump = relax_dir + 'sim_temp{}_force{}_time{}_seed*/dump.bin'
template_area = area_relax_dir + 'areas_temp{}_force{}_55_hi{}_seed{}.txt'
template_coord = coordination_dir + 'coordination_temp{}_force{}_hi{}_seed{}.txt'


temps = [2300]  # range(2000, 2500, 50)
for temp in temps:
    dumpfiles = glob(template_dump.format(orientation, height, temp, force, time))
    for dumpfile in dumpfiles:
        seed = re.findall('\d+', dumpfile)[-1]
        print(f"Temperature: {temp}, seed: {seed}")
        get_contact_area(dumpfile, template_area.format(temp, force, height, seed), delta=time/1e6)
        count_coord(dumpfile, template_coord.format(temp, force, height, seed))
