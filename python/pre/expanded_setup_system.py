"""
Crystal Aging Project

Script for generating intial system

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from pre_utils import gen_system

# user-input
lx = 99.9    # system length x-dir
ly = 100      # system length y-dir
ax = 50      # initial x-coordinate of asperity
ay = 50      # initial y-coordinate of asperity
hl = 50       # height of lower surface/plate
hu = 60      # height of upper surface
hup = 2       # height of upper plate

octa_d = 1 * 39.0 #The multiplyer has to be an integer
dode_d = 1 * 37.3

lower_orient = "100"
remove_atoms = True

path = '../../initial_system/'

gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
           remove_atoms, path)



#lx = 99.9    # system length x-dir
#ly = 100      # system length y-dir
#ax = 50      # initial x-coordinate of asperity
#ay = 50      # initial y-coordinate of asperity
#hl = 50       # height of lower surface/plate
#hu = 60      # height of upper surface
#hup = 2       # height of upper plate

#octa_d = 1 * 39.0 #The multiplyer has to be an integer
#dode_d = 1 * 37.3

