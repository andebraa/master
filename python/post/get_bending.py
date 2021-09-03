"""
Crystal Aging Project

Get the bending of the asperity as a
function of time. This is in particular
interesting in the stick-slip regime of
friction.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""
from numpy import savetxt, asarray
from lammps_logfile import File, running_mean

from post_utils import extract_displacement

# user input
temp = 2300
vel = 5
force = 0.001
orientation = "100"
height = 200


# paths
project_dir = '../../'
push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
bend_dir = project_dir + 'txt/bending/'

template_log = push_dir + 'sim_temp{}_vel{}_force{}_seed*/log.lammps'
template_bend = bend_dir + 'bending_temp{}_force{}.txt'


# extract displacement from log file
extract_displacement(template_log.format(orientation, height, temp, vel, force),
                     template_bend.format(temp, force))
