"""
Crystal Aging Project

Plot the normal pressure as a function of time for
relaxation simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from numpy import loadtxt, asarray, mean
import matplotlib.pyplot as plt
from glob import glob

#plt.style.use('seaborn-deep')
#plt.rcParams['figure.figsize'] = 12, 4

#######################################
### PRESSURE FOR VARIOUS TEMPERATURES
#######################################

# user input
temps = [2150, 2300, 2450]  # range(2000, 2500, 50)
force = 0.001

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
press_dir = project_dir + 'txt/pressure/'

template = press_dir + 'pressure_temp{}_force{}_seed{}.txt'


# get pressure files
time_list = []
press_list = []
temp_list = []
for temp in temps:
    files = glob(template.format(temp, force, "*"))
    time_temp, press_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, press = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        press = -press[max_ind:]/1000  # convert from MPa to GPa

        time_temp.append(time)
        press_temp.append(press)

    time_list.append(mean(time_temp, axis=0))
    press_list.append(mean(press_temp, axis=0))
    temp_list.append(temp)

plt.figure()
for i, temp in enumerate(temp_list):
    plt.scatter(time_list[i], press_list[i], alpha=0.6, label=f"T={temp} K")
    avg = mean(press_list[i])
    plt.axhline(avg, color='k', linestyle='--')
plt.legend(loc='best')
plt.title(r"Applied contant normal force 1.6$\mu N$")
plt.xlabel("Time [ns]")
plt.ylabel("Pressure [GPa]")
#plt.show()


########################################
### PRESSURE FOR VARIOUS NORMAL FORCES
########################################

# user input
temp = 2300
forces = [0.001, 0.002, 0.003, 0.01]

# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'
press_dir = project_dir + 'txt/pressure/'

template = press_dir + 'pressure_temp{}_force{}_seed{}.txt'


# get pressure files
time_list = []
press_list = []
for force in forces:
    files = glob(template.format(temp, force, "*"))
    time_temp, press_temp = [], []
    for file in files:
        print(file)
        data = loadtxt(file)
        time, press = data[:, 0], data[:, 1]

        # split between elasticity and crystallization 
        max_ind = 35  #np.argmax(poteng)

        time = time[max_ind:]
        press = -press[max_ind:]/1000  # convert from MPa to GPa

        time_temp.append(time)
        press_temp.append(press)

    time_list.append(mean(time_temp, axis=0))
    press_list.append(mean(press_temp, axis=0))


plt.figure()
for i, force in enumerate(forces):
    plt.scatter(time_list[i], press_list[i], alpha=0.6, label=f"F={force} eV/Å")
    avg = mean(press_list[i])
    plt.axhline(avg, color='k', linestyle='--')
plt.legend(loc='best')
plt.title(r"Temperature 2300 K")
plt.xlabel("Time [ns]")
plt.ylabel("Pressure [GPa]")
plt.show()
