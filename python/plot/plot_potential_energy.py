"""
Crystal Aging Project

Plot the contact area and number of particles in the
contact area as a function of time

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from numpy import loadtxt, asarray, mean
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from lammps_logfile import File, running_mean
from glob import glob

from multiline import multiline

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 7, 3


# user input
temps = range(2000, 2500, 50)
temps = [2000, 2150, 2300, 2450]
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
poteng_dir = project_dir + 'txt/poteng/'

template = poteng_dir + 'poteng_temp{}_force{}_seed{}.txt'


# get potential energy files
times_elastic = []
times_crystal = []
elastic_list = []
crystal_list = []
for temp in temps:
    files = template.format(temp, force, "*")
    times_elastic_avg = []
    times_crystal_avg = []
    poteng_elastic_avg = []
    poteng_crystal_avg = []
    print(temp)
    for file in glob(files):
        data = loadtxt(file)
        time, poteng = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 40  #np.argmax(poteng)

        time_elastic = time[:max_ind]
        time_crystal = time[max_ind:]
        elastic = poteng[:max_ind]
        crystal = poteng[max_ind:]

        times_elastic_avg.append(time_elastic)
        times_crystal_avg.append(time_crystal)
        poteng_elastic_avg.append(elastic)
        poteng_crystal_avg.append(crystal)

    times_elastic_avg = mean(times_elastic_avg, axis=0)
    times_crystal_avg = mean(times_crystal_avg, axis=0)
    poteng_elastic_avg = mean(poteng_elastic_avg, axis=0)
    poteng_crystal_avg = mean(poteng_crystal_avg, axis=0)

    times_elastic.append(times_elastic_avg)
    times_crystal.append(times_crystal_avg)
    elastic_list.append(poteng_elastic_avg)
    crystal_list.append(poteng_crystal_avg)


#############################
### plot with common colorbar
#############################
fig, ax = plt.subplots(1, 3)

# plot potential energy elasticity
#fig, ax = plt.subplots()
lc = multiline(times_elastic, elastic_list, temps, ax=ax[0], lw=2, cmap='cividis')
#axcb = fig.colorbar(lc, ax=ax)
#axcb.set_label(r"$T$ [K]")
ax[0].set_xlabel(r'$t$ [ns]')
ax[0].set_ylabel(r'$U(t)$ [MeV]')
#plt.tight_layout()
#plt.show()


# plot potential energy crystallization
#fig, ax = plt.subplots()
lc = multiline(times_crystal, crystal_list, temps, ax=ax[1], lw=2, cmap='cividis')
#axcb = fig.colorbar(lc, ax=ax)
#axcb.set_label(r"$T$ [K]")
ax[1].set_xlabel(r'$t$ [ns]')
ax[1].set_ylabel(r'$U(t)$ [MeV]')
#plt.tight_layout()
#plt.show()


# plot change of potential energy
#fig, ax = plt.subplots()
potengs = asarray(crystal_list) * 1000
potengs = potengs - potengs[:, 0].reshape(-1,1)
lc = multiline(times_crystal, potengs, temps, ax=ax[2], lw=2, cmap='cividis')
axcb = fig.colorbar(lc, ax=ax, orientation='horizontal', aspect=40)
axcb.set_label(r"$T$ [K]")
ax[2].set_xlabel(r'$t$ [ns]')
ax[2].set_ylabel(r'$U(t)-U(0)$ [KeV]')
#plt.tight_layout()
plt.savefig(fig_dir + 'png/poteng_subplots.png')
plt.savefig(fig_dir + 'pgf/poteng_subplots.pgf')
plt.show()


################################
### Plot coordinate system with different axis
################################
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False, gridspec_kw = {'wspace':0})

# plot elastic part
ax1.set_title("elastic")
for i, temp in enumerate(temps):
    ax1.plot(times_elastic[i], elastic_list[i], label=fr"$T={temp}$ K")
ax1.set_ylabel(r'$U(t)$ (MeV)')
ax1.legend(loc='best')

# plot crystalization part
ax2.set_title("crystalization")
for i, temp in enumerate(temps):
    ax2.plot(times_crystal[i], crystal_list[i])
ax2.set_ylabel(r'$U(t)$ (MeV)')

# adjust axes
ax1.yaxis.set_label_position("left")
ax2.yaxis.set_label_position("right")
ax1.yaxis.tick_left()
ax2.yaxis.tick_right()
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

# add diagonal lines
d = .015 # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1-d,1+d), (-d,+d), **kwargs)
ax1.plot((1-d,1+d),(1-d,1+d), **kwargs)

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d,+d), (1-d,1+d), **kwargs)
ax2.plot((-d,+d), (-d,+d), **kwargs)

# adjust ranges and ticks
ax1.set_xlim(-0.0125, times_elastic[0][-1])
ax2.set_xlim(times_crystal[0][0], 5.25)
ax1.set_xticks([0.0, 0.050, 0.10, 0.150])
ax1.set_xticklabels(['0', '1/20', '1/10', '3/20'])
ax2.set_xticks(range(1, 6))

# background hatch
ax1.add_patch(Rectangle((-0.0125, -6), 0.25, 1, fill=False, color='0.8', hatch=".."))
ax2.add_patch(Rectangle((0.15, -6), 6, 1, fill=False, color='0.8', hatch="o"))

# common label on x-axis
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("$t$ (ns)")

plt.tight_layout()
plt.savefig(fig_dir + 'pgf/potential_energy_split.pgf')
plt.show()
