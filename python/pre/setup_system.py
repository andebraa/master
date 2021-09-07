"""
Crystal Aging Project

Script for generating intial system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from pre_utils import gen_system

# user-input
lx = 299.9    # system length x-dir
ly = 300      # system length y-dir
ax = 150      # initial x-coordinate of asperity
ay = 150      # initial y-coordinate of asperity
hl = 50       # height of lower surface/plate
hu = 150      # height of upper surface
hup = 2       # height of upper plate
lz = hl + hu  #total height of system

octa_d = 3 * 39.0
dode_d = 3 * 37.3

lower_orient = "100"
remove_atoms = True

path = '../../initial_system/'

system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
           remove_atoms, path)

system_file = path + f"system_or{lower_orient}_hi{lz}.data"
system.write(system_file, format="lammps-data")
print("System written to: ", system_file)

