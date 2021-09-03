"""
Crystal Aging Project

Plot static friction as a function of contact area and number of
atoms in the contact region.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from regression import poly_reg, nonlin_reg

#plt.rcParams['figure.figsize'] = 7, 5

pgf_with_lualatex = {
'text.usetex': True,
'pgf.rcfonts': False,
'font.family': 'sans-serif',
'font.serif': [],
'font.monospace': [],
'figure.figsize': (7, 3),
"pgf.texsystem": "lualatex",
"pgf.preamble": "\n".join([
r"\usepackage[utf8]{inputenc}",
r"\usepackage[T1]{fontenc}",
r"\usepackage[detect-all,locale=DE]{siunitx}",
])
}
matplotlib.rcParams.update(pgf_with_lualatex)

# user inputs
vel = 5
force = 0.001
height = 300
alpha = 0.6


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
max_static_dir = project_dir + 'txt/max_static/'
area_push_dir = project_dir + 'txt/area_push/'

template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}.txt'
template_contact = area_push_dir + 'areas_{}K_55_time{}_hi{}.txt'


# restructure data
temps = [2150, 2300, 2450]
frictions, slip_times, break_nums, break_areas = [], [], [], []
for temp in temps:
    # load max static friction before system breaks
    friction = np.loadtxt(template_ms.format(temp, vel, force))


    # load contact area and number of particles while pushing the asperity
    contacts = []
    for time in range(25000, 2500001, 25000):
        contact = np.loadtxt(template_contact.format(temp, time, height))
        contacts.append(contact)


    # unpack arrays
    slip_time, friction = friction.T
    contacts = np.asarray(contacts)
    nums, areas = contacts[:, :, 0], contacts[:, :, 1]

    # map break time to contact area and number of contacts
    sliptime2 = np.round(2*slip_time).astype(int)
    break_num, break_area  = [], []
    for i, time in enumerate(sliptime2):
        break_num.append(nums[i, time])
        break_area.append(areas[i, time])

    break_num = np.asarray(break_num)
    break_area = np.asarray(break_area)

    # append arrays to lists
    break_nums.append(break_num)
    break_areas.append(break_area)
    frictions.append(friction)
    slip_times.append(slip_time)


# plot max. static friction as a function of number of contact atoms 
fig = plt.figure()
for i, temp in enumerate(temps):
    a = poly_reg(break_nums[i], frictions[i], 1, bias=False)
    lin_nums = np.asarray([break_nums[i].min(), break_nums[i].max()])

    plt.scatter(break_nums[i], frictions[i], alpha=alpha, label=fr"$T={temp}$ K")
    if i == 0:
        plt.plot(lin_nums, a * lin_nums, '--k', label=r'$f(t)=at$')
    else:
        plt.plot(lin_nums, a * lin_nums, '--k')
plt.legend(loc='best')
plt.xlabel(r"$N$")
plt.ylabel(r"$f_{s,max}$ ($\mu$N)")
plt.tight_layout()
plt.savefig(fig_dir + 'png/max_static_num_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/max_static_num_2150_2300_2450.pgf')


# plot max. static friction as a function of contact area 
#fig, ax = plt.subplots(1, 2)
plt.figure()
for i, temp in enumerate(temps):
    a = poly_reg(break_areas[i], frictions[i], 1, bias=False)
    #lin_areas = np.linspace(break_areas[i].min(), break_areas[i].max(), 2)
    lin_areas = np.asarray([break_areas[i].min(), break_areas[i].max()])

    plt.scatter(break_areas[i], frictions[i], alpha=alpha, label=fr"$T={temp}$ K")
    if i == 0:
        plt.plot(lin_areas, a * lin_areas, '--k', label=r'$f(t)=at$')
    else:
        plt.plot(lin_areas, a * lin_areas, '--k')
plt.legend(loc='best')
plt.xlabel(r"$A$ (nm$^2$)")
plt.ylabel(r"$f_{s,max}$ ($\mu$N)")
#plt.tight_layout()
plt.show()


# plot max. static friction as a function of break time
def F(t, F0, c, tau):
    return F0*(1+c*np.log(1+t/tau))

bounds = [[10, 100], [-10, 10], [0.001, 10]]

fig, ax = plt.subplots(1, 2)
for i, temp in enumerate(temps):
    params = nonlin_reg(slip_times[i], frictions[i], F, bounds)
    lin_slips = np.linspace(slip_times[i].min(), slip_times[i].max(), 1000)

    ax[0].scatter(slip_times[i], frictions[i], alpha=alpha, label=fr"$T={temp}$ K")
    if i == 0:
        ax[0].plot(lin_slips, F(lin_slips, *params), '--k', label=r'$f_{s,max}(t)=N(t)\cdot\bar{F}(t)$')
    else:
        ax[0].plot(lin_slips, F(lin_slips, *params), '--k')
ax[0].legend(loc='best')
ax[0].set_ylabel(r"$f_{s,max}$ ($\mu$N)")
ax[0].set_xlabel(r"$t$ (ns)")
#plt.tight_layout()
#plt.savefig(fig_dir + 'png/max_static_time_2150_2300_2450.png')
#plt.savefig(fig_dir + 'pgf/max_static_time_2150_2300_2450.pgf')


# plot max. static friction divided by number of contact atoms
def F(A, Fs, Fw):
    r = np.sqrt(A/np.pi)
    return (2/r) * (Fs-Fw) + Fw

bounds = [[0.001, 1], [0.001, 1]]

#fig = plt.figure()
for i, temp in enumerate(temps):
    avg_force = friction[i]/break_nums[i] * 1000
    params = nonlin_reg(break_areas[i], avg_force, F, bounds)
    ax[1].scatter(slip_times[i], avg_force, alpha=alpha, label=fr'$T={temp}$ K')
    if i == len(temps)-1:
        ax[1].plot(slip_times[i], F(break_areas[i], *params), '--k', label=r'$\bar{F}(t)=(2/r)(F_s-F_w)+F_w$')
    else:
        ax[1].plot(slip_times[i], F(break_areas[i], *params), '--k')
ax[1].legend(loc='best')
ax[1].set_ylabel(r"$\bar{F}(t)$ (nN)")
ax[1].set_xlabel(r"$t$ (ns)")
plt.tight_layout()
plt.savefig(fig_dir + 'png/force_regression.png')
plt.savefig(fig_dir + 'pgf/force_regression.pgf')
plt.show()
