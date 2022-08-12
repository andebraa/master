"""
Crystal Aging Project

Plot the bending of the asperity as a
function of time. This is in particular
interesting in the stick-slip regime of
friction.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from numpy import loadtxt
import matplotlib.pyplot as plt
from multiline import multiline


# user input
temp = 2300
vel = 5
force = 0.001
orientation = "100"
height = 200


# paths
project_dir = '../../'
bend_dir = project_dir + 'txt/bending/'

template = bend_dir + 'bending_temp{}_force{}.txt'


# read data
data = loadtxt(template.format(temp, force))


# plot curves with colorbar indicating the height
fig, ax = plt.subplots()
height = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5]
lc = multiline(data[:, 0], data[:, 1:], height, ax=ax, **kwargs)
axcb = plt.colorbar(lc, ax=ax)
axcb.set_label(f'Asperity z [Å]')
plt.ylabel("x-position cm [Å]")


# plot heatmap
times, fx, cms = read_logfile(logfile, window)

cms = cms - cms[-1]

fig, ax = plt.subplots(2)

force = ax[0].imshow(-fx.reshape(1, -1), extent=[times[0][0], times[0][-1], 0, 1], aspect='auto')

cbar = plt.colorbar(force, ax=ax[0])
cbar.set_label('force [eV/Å]')

dis = ax[1].imshow(cms[::-1][:-1], extent=[times[0][0], times[0][-1], 15, 150], aspect='auto', cmap='viridis_r')

cbar = plt.colorbar(dis, ax=ax[1])
cbar.set_label('displacement x [Å]')
ax[1].set_xlabel("time [ps]")
ax[1].set_ylabel("z-position cm [Å]")
plt.show()


if __name__ == "__main__":
    for i in range(500, 5010, 500):
        plot_heatmap(f"/home/users/evenmn/sic-friction/simulations/static_large_torque/sim_temp2200_vel5_force0.001_time{i}_seed72221/log.lammps", window=1000)

