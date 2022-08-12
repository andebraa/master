"""
Crystal Aging Project

Plot the diffusion coefficient as a function of time for
relaxation simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from regression import nonlin_reg, multiple_reg

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 7, 9

#######################################
### SPREAD IN DIFFUSION
#######################################

# user input
temp = 2300
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diffusion_dir = project_dir + 'txt/diffusion/'

template = diffusion_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
diff_list = []
temp_list = []

files = glob(template.format(temp, force, "*"))
for file in files:
    print(file)
    data = loadtxt(file)
    time, diff = data[:, 0], data[:, 1]

    # split between elasticity and crystallization 
    max_ind = 35  #np.argmax(poteng)

    time = time[max_ind:]
    diff = diff[max_ind:]

    diff_list.append(diff)


fig, ax = plt.subplots(3, 2)
for i, diff in enumerate(diff_list):
    ax[0, 0].plot(time, diff, label=f"seed {i}")
ax[0, 0].legend(loc='best')
ax[0, 0].set_xlabel("Time (ns)")
ax[0, 0].set_ylabel(r"Mass diffusivity (cm$^2$/s)")



#######################################
### DIFFUSION FOR VARIOUS TEMPERATURES
#######################################

# user input
temps = [2000, 2150, 2300]  # range(2000, 2500, 50)
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diffusion_dir = project_dir + 'txt/diffusion/'

template = diffusion_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
time_list = []
diff_list = []
temp_list = []
for temp in temps:
    files = glob(template.format(temp, force, "*"))
    time_temp, diff_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, diff = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        diff = diff[max_ind:]

        time_temp.append(time)
        diff_temp.append(diff)

    time_list.append(mean(time_temp, axis=0))
    diff_list.append(mean(diff_temp, axis=0))
    temp_list.append(temp)

#plt.figure()
for i, temp in enumerate(temp_list):
    ax[1, 0].plot(time_list[i], diff_list[i], label=fr"$T={temp}$ K")
ax[1, 0].legend(loc='best')
ax[1, 0].set_xlabel("Time (ns)")
ax[1, 0].set_ylabel(r"Mass diffusivity (cm$^2$/s)")


#######################################
### DIFFUSION FOR VARIOUS TEMPERATURES WITH INDIVIDUAL REGRESSION
#######################################

print("D0 d tau")

def D(t, D0):
    T = temps[i]
    # E = 2100
    # d = 20
    Dss = D0 # * np.exp(-E/T)
    d = 3.45e-5
    tau = 0.02
    return Dss + d/(1+t/tau)
bounds = [[1, 2]]

# user input
temps = [2000, 2150, 2300]  # range(2000, 2500, 50)
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diffusion_dir = project_dir + 'txt/diffusion/'

template = diffusion_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
time_list = []
diff_list = []
temp_list = []
for temp in temps:
    files = glob(template.format(temp, force, "*"))
    time_temp, diff_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, diff = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        diff = diff[max_ind:]

        time_temp.append(time)
        diff_temp.append(diff)

    time_list.append(mean(time_temp, axis=0))
    diff_list.append(mean(diff_temp, axis=0))
    temp_list.append(temp)

#plt.figure()
params_list = []
for i, temp in enumerate(temp_list):
    params = nonlin_reg(time_list[i], diff_list[i], D, bounds, maxfev=100000)
    params_list.append(params[0])
    ax[1, 1].plot(time_list[i], diff_list[i], label=fr"$T={temp}$ K")
    if i == len(temps) - 1:
        ax[1, 1].plot(time_list[i], D(time_list[i], *params), '--k', label=r"$D(t)=D_{ss}+d/(1+t/\tau))$")
    else:
        ax[1, 1].plot(time_list[i], D(time_list[i], *params), '--k')
ax[1, 1].legend(loc='best')
ax[1, 1].set_xlabel("Time (ns)")
ax[1, 1].set_ylabel(r"Mass diffusivity (cm$^2$/s)")


#######################################
### PLOT PARAMETER
#######################################

def Dss(T, D0, E):
    return D0 * np.exp(-E/T)

bounds = [[1, 2], [1, 2]]

params = nonlin_reg(temps, params_list, Dss, bounds)
temps_long = np.linspace(temps[0], temps[-1], 1000)

#plt.figure()
for i in range(len(temps)):
    ax[2, 1].scatter(temps[i], params_list[i], label=fr"$T={temps[i]}$ K")
ax[2, 1].plot(temps_long, Dss(temps_long, *params), '--k', label=r"$D_{ss}(T)=D_0\exp(-E/kT)$")
ax[2, 1].legend(loc='best')
ax[2, 1].set_xlabel(r"$T$ (K)")
ax[2, 1].set_ylabel(r"$D_{ss}(T)$ (cm$^2$/s)")
ax[2, 1].set_xticks(temps)


########################################
### DIFFUSION FOR VARIOUS NORMAL FORCES
########################################

# user input
temp = 2300
forces = [0.001, 0.002]

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diff_dir = project_dir + 'txt/diffusion/'

template = diff_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
time_list = []
diff_list = []
for force in forces:
    files = glob(template.format(temp, force, "*"))
    time_temp, diff_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, diff = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        diff = diff[max_ind:]

        time_temp.append(time)
        diff_temp.append(diff)

    time_list.append(mean(time_temp, axis=0))
    diff_list.append(mean(diff_temp, axis=0))


#plt.figure()
for i, force in enumerate(forces):
    ax[0, 1].plot(time_list[i], diff_list[i], label=fr"$F={force}$ eV/Å")
ax[0, 1].legend(loc='best')
ax[0, 1].set_xlabel("Time (ns)")
ax[0, 1].set_ylabel(r"Mass diffusivity (cm$^2$/s)")



#######################################
### DISPLACED DIFFUSION FOR VARIOUS TEMPERATURES
#######################################

# user input
temps = [2000, 2150, 2300]  # range(2000, 2500, 50)
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diffusion_dir = project_dir + 'txt/diffusion/'

template = diffusion_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
time_list = []
diff_list = []
temp_list = []
for temp in temps:
    files = glob(template.format(temp, force, "*"))
    time_temp, diff_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, diff = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        diff = diff[max_ind:]

        time_temp.append(time)
        diff_temp.append(diff)

    time_list.append(mean(time_temp, axis=0))
    diff_list.append(mean(diff_temp, axis=0))
    temp_list.append(temp)

#plt.figure()
for i, temp in enumerate(temp_list):
    ax[2, 0].plot(time_list[i], diff_list[i]-diff_list[i][-1], label=fr"$T={temp}$ K")
ax[2, 0].legend(loc='best')
ax[2, 0].set_xlabel("Time (ns)")
ax[2, 0].set_ylabel(r"Mass diffusivity (cm$^2$/s)")
plt.tight_layout()
plt.savefig(fig_dir + 'png/diffusion.png')
plt.savefig(fig_dir + 'pgf/diffusion.pgf')
plt.show()

stop

#######################################
### DISPLACED DIFFUSION FOR VARIOUS TEMPERATURES WITH COMMON REGRESSION
#######################################

def D(t, temp, D0, d, tau):
    # T = temp
    # E = 2100
    # d = 20
    Dss = D0  # * np.exp(-E/T)
    return Dss + d/(1+t/tau)


# user input
temps = [2000, 2150, 2300]  # range(2000, 2500, 50)
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
diffusion_dir = project_dir + 'txt/diffusion/'

template = diffusion_dir + 'diffusion_temp{}_force{}_seed{}.txt'


# get diffusion files
time_list = []
diff_list = []
temp_list = []
for temp in temps:
    files = glob(template.format(temp, force, "*"))
    time_temp, diff_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, diff = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        diff = diff[max_ind:]

        time_temp.append(time)
        diff_temp.append(diff)

    time_temp_mean = mean(time_temp, axis=0)
    diff_temp_mean = mean(diff_temp, axis=0)

    time_list.append(time_temp_mean)
    diff_list.append(diff_temp_mean - diff_temp_mean[-1])
    temp_list.append(temp)

params, _ = multiple_reg(time_list, diff_list, D, temps, [10, 100, 0.1], maxfev=10000)
print(params)

plt.figure()
for i, temp in enumerate(temp_list):
    plt.plot(time_list[i], diff_list[i], label=f"T={temp} K")
plt.plot(time_list[0], D(time_list[0], 0, *params), '--k')
plt.legend(loc='best')
plt.xlabel("Time (ns)")
plt.ylabel(r"Mass diffusivity (cm$^2$/s)")
plt.show()
