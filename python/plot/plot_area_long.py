"""
Crystal Aging Project

Plot the contact area and number of particles in the
contact area as a function of time

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.constants import physical_constants
from scipy.signal import savgol_filter

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 6.5, 2


# user input
temps = [2300]
force = 0.001
orientation = "100"
height = 200
time = 20000


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
area_relax_dir = project_dir + 'txt/area_relax/'

template = area_relax_dir + 'areas_temp{}_force{}_time{}_55_hi{}_seed*.txt'

##################################
### READ FILES
##################################

# read area files
times, nums, areas = [], [], []
for temp in temps:
    files = glob(template.format(temp, force, time, height))
    
    # average simulations with same parameters but different seeds
    nums_temp, areas_temp = [], []
    for file in files:
        print(file)
        data = np.loadtxt(file)
        time, num, area = data[:, 0], data[:, 1], data[:, 2]

        # ignore elastic part
        max_ind = 20

        num = num[max_ind:]
        area = area[max_ind:]
        time = time[max_ind:]

        num = savgol_filter(num, 29, 2)
        area = savgol_filter(area, 29, 2)

        nums_temp.append(num)
        areas_temp.append(area)

    nums.append(np.asarray(nums_temp).mean(axis=0))
    areas.append(np.asarray(areas_temp).mean(axis=0))
    times.append(time)

area_indirect = nums[0] * 21 / 300 - 20
np.savetxt(area_relax_dir + 'area_long_indirect.txt', np.asarray([times[0], area_indirect]).T)
stop

##################################
### LINE PLOTS
##################################

alpha = 0.7
xticks = [0, 5, 10, 15, 20]
yticks = [30, 50, 70, 90]

"""
# plot number of contact atoms, legend plot
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.plot(times[i], nums[i], alpha=alpha, linewidth=2, color='k')
plt.xticks(xticks)
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()


# plot contact area, legend plot
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.plot(times[i], areas[i], alpha=alpha, linewidth=2, color='k')
plt.xticks(xticks)
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
"""

# plot contact area indirectly via number of contact atoms, legend plot
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    ax.plot(times[i], nums[i] * 21 / 300 - 20, alpha=alpha, linewidth=2, color='k')
ax.set_xticks(xticks)
ax.set_yticks(yticks)
ax.set_xlabel(r'$t$ [ns]')
ax.set_ylabel(r'$A(t)$ [nm$^2$]')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()
#plt.savefig(fig_dir + 'png/area_time_2300_long.png')
#plt.savefig(fig_dir + 'pgf/area_time_2300_long.pgf')
#plt.show()


"""
# plot contact area vs. number of contact points
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.plot(nums[i], areas[i], alpha=alpha, linewidth=2, color='k')
plt.xlabel(r'$N(t)$')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.show()
"""
