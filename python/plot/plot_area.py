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
from lammps_logfile import running_mean
from scipy.constants import physical_constants

from regression import nonlin_reg, multiple_reg
from multiline import multiline

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 7, 5


# user input
#temps = range(2000, 2500, 50)
temps = [2300]
force = 0.001
orientation = "100"
height = 200
save = True


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
relax_dir = project_dir + 'simulations/aging/sys_or{}_hi{}/relax/'
area_relax_dir = project_dir + 'txt/area_relax/'

template_log = relax_dir + 'sim_temp{}_force{}_time5000_seed*/log.lammps'
template_area = area_relax_dir + 'areas_temp{}_force{}_55_hi{}_seed*.txt'

##################################
### READ FILES
##################################

# read area files
times, nums, areas = [], [], []
for temp in temps:
    files = glob(template_area.format(temp, force, height))

    # average simulations with same parameters but different seeds
    nums_temp, areas_temp = [], []
    for file in files:
        print(file)
        data = np.loadtxt(file)
        time, num, area = data[:, 0], data[:, 1], data[:, 2]

        # ignore elastic part
        max_ind = 35

        num = num[max_ind:]
        area = area[max_ind:]
        time = time[max_ind:]

        nums_temp.append(num)
        areas_temp.append(area)

    nums.append(np.asarray(nums_temp).mean(axis=0))
    areas.append(np.asarray(areas_temp).mean(axis=0))
    times.append(time)

nums = np.asarray(nums)
areas = np.asarray(areas)

#################################
### LINE PLOTS WITH COLORBAR
#################################

# plot number of contact atoms, colorbar plot
fig, ax = plt.subplots()
lc = multiline(times, nums, temps, ax=ax, lw=2, cmap='cividis')
axcb = fig.colorbar(lc, ax=ax)
axcb.set_label(r"$T$ [K]")
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'png/num_time_cb_2000_2150_2300_2450.png')
    plt.savefig(fig_dir + 'pgf/num_time_cb_2000_2150_2300_2450.pgf')
#plt.show()
#stop

# plot contact area, colorbar plot
fig, ax = plt.subplots()
lc = multiline(times, areas, temps, ax=ax, lw=2, cmap='cividis')
axcb = fig.colorbar(lc, ax=ax)
axcb.set_label(r"$T$ [K]")
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'png/area_time_cb_2000_2150_2300_2450.png')
    plt.savefig(fig_dir + 'pgf/area_time_cb_2000_2150_2300_2450.pgf')


##################################
### SCATTER PLOTS WITH LEGENDS
##################################

alpha = 0.7
marker_size = 2
lgnd_marker_size = 30

# plot number of contact atoms, legend plot
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], nums[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'png/num_time_2000_2150_2300_2450.png')
    plt.savefig(fig_dir + 'pgf/num_time_2000_2150_2300_2450.pgf')


# plot contact area, legend plot
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], areas[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'png/area_time_2000_2150_2300_2450.png')
    plt.savefig(fig_dir + 'pgf/area_time_2000_2150_2300_2450.pgf')



# plot contact area vs. number of contact points
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(nums[i], areas[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
plt.plot([0.0, max(nums[-1])], [0.0, max(areas[-1])], '--k')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$N(t)$')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'png/area_num_2000_2150_2300_2450.png')
    plt.savefig(fig_dir + 'pgf/area_num_2000_2150_2300_2450.pgf')
plt.show()


"""

#################################
### INDEPENDENT REGRESSION
#################################


def F(t, F0, c, tau):
    #c = 0.9
    #d = 2100
    #c *= np.exp(-d/temps[i])
    tau = 0.2
    return F0*(1+c*np.log(1+t/tau))


N0s, Ntaus, Ncs, Nds = [], [], [], []
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    bounds = [[100, 1000], [0.1, 1.0], [0.001, 10]]
    params = nonlin_reg(times[i], nums[i], F, bounds, seed=10)
    plt.scatter(times[i], nums[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
    plt.plot(times[i], F(times[i], *params), '--k')
    N0s.append(params[0])
    Ncs.append(params[1])
    #Nds.append(params[2])
    Ntaus.append(params[2])
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()


A0s, Ataus, Acs, Ads = [], [], [], []
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    bounds = [[10, 100], [0.1, 1.0], [0.001, 10]]
    params = nonlin_reg(times[i], areas[i], F, bounds)
    plt.scatter(times[i], areas[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
    plt.plot(times[i], F(times[i], *params), '--k')
    A0s.append(params[0])
    Acs.append(params[1])
    #Ads.append(params[2])
    Ataus.append(params[2])
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.show()


# plot parameters
def tau(T, a, T0):
    return a*(1-T/T0)

bounds = [[1, 2], [1500, 2500]]
params_tau = nonlin_reg(temps, Ataus, tau, bounds)

temps_dense = np.linspace(temps[0], temps[-1], 1000)

fig = plt.figure()
plt.plot(temps, Ataus, label='observation')
plt.plot(temps_dense, tau(temps_dense, *params_tau), '--k', label=r'$a\exp(-b/T)$')
#plt.plot(temps, Ntaus, label='Num')
plt.legend(loc='best')
plt.xlabel("Temperature [K]")
plt.ylabel(r"$\tau$ [ns]")
plt.tight_layout()

def c(T, a, b):
    return a*np.exp(-b/T)

bounds = [[1, 2], [1500, 2500]]
params_c = nonlin_reg(temps, Acs, c, bounds)
temps_long = np.linspace(temps[0], temps[-1], 1000)

fig = plt.figure()
plt.plot(temps, Acs, label='observation')
#plt.plot(temps, Ncs, label='Num')
plt.plot(temps_long, c(temps_long, *params_c), '--k', label=r'$a(1-T/T^*)$')
plt.legend(loc='best')
plt.xlabel("Temperature [K]")
plt.ylabel(r"$c$")
plt.tight_layout()
plt.show()


# displace graphs
def F(t, F0, c, tau):
    #c = 0.9
    #id = 2100

    #c *= np.exp(-d/temps[i])
    tau = 0.2
    return F0*(1+c*np.log(1+t/tau))

print("")
for i in range(len(nums)):
    nums[i] -= N0s[i]
    nums[i] += 300

fig, ax = plt.subplots()
Ncs, Ntaus = [], []
for i, temp in enumerate(temps):
    bounds = [[200, 400], [0.1, 1.0], [0.001, 10]]
    params = nonlin_reg(times[i], nums[i], F, bounds)
    plt.scatter(times[i], nums[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
    plt.plot(times[i], F(times[i], *params), '--k')
    Ncs.append(params[1])
    Ntaus.append(params[2])
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()

for i in range(len(areas)):
    areas[i] -= A0s[i]
    areas[i] += 21

fig, ax = plt.subplots()
Acs, Ataus = [], []
for i, temp in enumerate(temps):
    bounds = [[10, 100], [0.1, 1.0], [0.001, 10]]
    params = nonlin_reg(times[i], areas[i], F, bounds)
    plt.scatter(times[i], areas[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
    plt.plot(times[i], F(times[i], *params), '--k')
    plt.plot(times[i], F(times[i], 21, c(temp, *params_c), 0.2), '--r')
    Acs.append(params[1])
    Ataus.append(params[2])
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.show()

#############################
### SUBPLOTS
#############################

fig, ax = plt.subplots(2, 2)

# (1, 1)
bounds = [[3000, 4000], [20000, 30000]]
temps_long = np.linspace(temps[0], temps[-1], 100)
params_c = nonlin_reg(temps, Acs, c, bounds)
ax[1, 1].plot(temps_long, c(temps_long, *params_c), linestyle='--', color='0.5', label=r"$c(T)=c_0\exp(-E/kT)$")
for temp, Ac in zip(temps, Acs):
    ax[1, 1].scatter(temp, Ac, alpha=alpha, label=fr'$T={temp}$ siK')
ax[1, 1].set_xlabel(r"$T$ (siK)")
ax[1, 1].set_ylabel(r"$c(T)$")
ax[1, 1].set_xticks([2000, 2150, 2300, 2450])

# (0, 1)
ax[0, 1].axis('off')

# (0, 0)
for i, temp in enumerate(temps):
    bounds = [[10, 100], [0.1, 1.0], [0.001, 10]]
    params = nonlin_reg(times[i], areas[i], F, bounds)
    ax[0, 0].scatter(times[i], areas[i], s=marker_size, alpha=alpha)
    if i == 0:
        ax[0, 0].plot(times[i], F(times[i], 21, c(temp, *params_c), 0.2), '--k', label=r"$A(t)=A_0[1+c\log(1+t/\tau)]$")
    else:
        ax[0, 0].plot(times[i], F(times[i], 21, c(temp, *params_c), 0.2), '--k')
ax[0, 0].set_xlabel(r'$t$ (sins)')
ax[0, 0].set_ylabel(r'$A(t)$ (sinm $^2$)')

#################################
### CURVE COLLAPSE
#################################

# (1, 0)
for i, temp in enumerate(temps):
    ax[1, 0].scatter(times[i], (areas[i]/21-1)/c(temp, *params_c), s=marker_size, alpha=alpha)
ax[1, 0].set_xlabel(r"$t$ (sins)")
ax[1, 0].set_ylabel(r"$\frac{A(t)/A_0-1}{c}$")

# common legends
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
handles, labels = [sum(lol, []) for lol in zip(*lines_labels)]
for handle in handles:
    try:
        handle.set_sizes([lgnd_marker_size])
    except AttributeError:
        pass
fig.legend(handles, labels, loc=(0.61, 0.65))
plt.tight_layout()
plt.savefig(fig_dir + 'pgf/subplots.pgf')
plt.show()
stop


#################################
### DEPENDENT REGRESSION
#################################

k = physical_constants['Boltzmann constant in eV/K'][0]

# do regression on multiple curves with the same parameters
def F(t, T, F0, a, b, c):
    """
    The function

        F(t; T) = F0 * [1 + c * log(1+t/tau)]

    with

        tau = a * T ^ n * exp(-b/T)
    """
    kT = k * T
    tau = (a / kT ** 4.) * np.exp(b/kT)
    t_ = t / tau
    return F0 * (1 + c*np.log(1 + t_))

def F1(t, T, F0, a, b, c):
    """
    The function

        F(t; T) = F0 * [1 + c * log(1+t/tau)]

    with

        tau = a * T ^ n * exp(-b/T)
    """
    kT = k * T
    tau = (a / (kT - b)) * np.exp(b/kT)
    t_ = t / tau
    return F0 * (1 + c*np.log(1 + t_))

# contact area
areas = np.asarray(areas)
for i in range(len(areas)):
    print(A0s[i])
    areas[i] -= A0s[i]
    areas[i] += 21
opt_params_area, _ = multiple_reg(times, areas, F, temps, [21, 1e-10, -1e-5, 1], maxfev=100000)
print("Optimal parameters for area: ", opt_params_area)

fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], areas[i], s=marker_size, alpha=alpha, label=fr"$T={temp}$ K")
    plt.plot(times[i], F(times[i], temp, *opt_params_area), '--k')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.savefig(fig_dir + 'png/area_time_reg_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/area_time_reg_2000_2150_2300_2450.pgf')


# number of contact atoms
nums = np.asarray(nums)
for i in range(len(nums)):
    nums[i] -= N0s[i]
    nums[i] += 400
opt_params_num, _ = multiple_reg(times, nums, F, temps, [300, 1e-10, 1e-5, 1], maxfev=100000)
print("Optimal parameters for num: ", opt_params_num)

fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], nums[i], s=marker_size, alpha=alpha, label=fr"$T={temp}$ K")
    plt.plot(times[i], F(times[i], temp, *opt_params_num), '--k')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()
plt.savefig(fig_dir + 'png/num_time_reg_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/num_time_reg_2000_2150_2300_2450.pgf')


##################################
### SMOOTH GRAPHS
##################################

nums_smooth, areas_smooth = [], []
for num, area in zip(nums, areas):
    nums_smooth.append(running_mean(num, 10))
    areas_smooth.append(running_mean(area, 10))


##################################
### PLOT SMOOTHED GRAPHS
##################################

# contact area
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], areas_smooth[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.savefig(fig_dir + 'png/area_time_smooth_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/area_time_smooth_2000_2150_2300_2450.pgf')


# number of atoms
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    plt.scatter(times[i], nums_smooth[i], s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()
plt.savefig(fig_dir + 'png/num_time_smooth_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/num_time_smooth_2000_2150_2300_2450.pgf')


##################################
### CURVE COLLAPSE
##################################

# contact area
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    A0, a, b, c = opt_params_area
    kT = k * temp
    tau = (a / kT ** 4.) * np.exp(b/kT)
    rhs = tau * (np.exp((areas_smooth[i] - A0) / (c * A0)) - 1)
    plt.scatter(times[i], rhs, s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
plt.plot([0, 5], [0, 5], '--k')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$\tau[\exp((A(t)-A_0)/cA_0)-1]$ [ns]')
plt.xlim(-0.5, 5.5)
plt.ylim(-0.5, 7)
plt.tight_layout()
plt.savefig(fig_dir + 'png/area_time_collapse_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/area_time_collapse_2000_2150_2300_2450.pgf')


# number of contact atoms
fig, ax = plt.subplots()
for i, temp in enumerate(temps):
    N0, a, b, c = opt_params_num
    kT = k * temp
    tau = (a / kT ** 4.) * np.exp(b/kT)
    rhs = tau * (np.exp((nums_smooth[i] - N0) / (c * N0)) - 1)
    plt.scatter(times[i], rhs, s=marker_size, alpha=alpha, label=fr'$T={temp}$ K')
plt.plot([0, 5], [0, 5], '--k')
lgnd = plt.legend(loc='best')
for handle in lgnd.legendHandles:
    handle.set_sizes([lgnd_marker_size])
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$\tau[\exp((N(t)-N_0)/cN_0)-1]$ [ns]')
plt.xlim(-0.5, 5.5)
plt.ylim(-0.5, 7)
plt.tight_layout()
plt.savefig(fig_dir + 'png/num_time_collapse_2000_2150_2300_2450.png')
plt.savefig(fig_dir + 'pgf/num_time_collapse_2000_2150_2300_2450.pgf')

plt.show()

"""
