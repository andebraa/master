"""
Crystal Aging Project

Script for generating intial system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from pre_utils import gen_grid_system

# user-input
lx = 99.9       # system length x-dir
ly = 100        # system length y-dir
ax = 50         # initial x-coordinate of asperity
ay = 50         # initial y-coordinate of asperity
hl = 50         # height of lower surface/plate
hu = 60         # height of upper surface
hup = 2         # height of upper plate
lz = hl + hu    #total system height
octa_d = 1 * 39.0 #The multiplyer has to be an integer
dode_d = 1 * 37.3
grid = (3,3)

lower_orient = "100"
remove_atoms = True

#beefboy path
#path = '/run/user/1004/initial_system/andebraa_masterdata/'
#regular path
path = '../../initial_system/'
system = gen_grid_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                         remove_atoms, path, grid=(3,3))



system_file = path + f"system_or{lower_orient}_hi{lz}_grid{grid[0]}_{grid[1]}.data"
system.write(system_file, format="lammps-data")
print("System written to: ", system_file)

