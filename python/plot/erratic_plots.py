"""
Rewrite of even chrystal aging project.
Assumes erratic system, with corresponding auxiliary file.

"""
import json
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
height = 115
save = True
grid = (3,3)
seed = 10730

project_dir = '../../'
fig_dir = project_dir + 'fig/png/erratic/'
relax_dir = project_dir + 'simulations/sys_or{}_hi{}/relax/'
area_relax_dir = project_dir + 'txt/area_relax/erratic/'
coordination_dir = project_dir + 'txt/coordination/'


template_dump = relax_dir + 'sim_temp{}_force{}_time{}_seed*_errgrid{}_{}/dump.bin'
auxiliary_dir = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_errgrid{}_{}_auxiliary.json'
template_area = area_relax_dir + 'areas_temp{}_force{}_55_hi{}_seed{}_erratic{}_{}_asperity{}.txt'
template_coord = coordination_dir + 'coordination_temp{}_force{}_hi{}_seed{}_erratic{}_{}'


with open(auxiliary_dir.format(orientation, height, grid[0], grid[1])) as auxfile:
    data = auxfile.read()
args = json.loads(data)


##################################
### READ FILES
##################################


# plot number of contact atoms, colorbar plot
#if asperities % 2 == 0:
#    nrows = asperities/2
#    ncols = asperities/2
#else:
#    nrows = asperities
#    ncols = 1

asperities = args['asperities']

fig, ax = plt.subplots(nrows = 1, ncols = 1)


# read area files
times, nums, areas = [], [], []
for temp in temps:
    
    for asperity in range(args['asperities']):
        files = glob(template_area.format(temp, force, height, seed, grid[0], grid[1], asperity))
        
        if files == []:
            raise AssertionError("no files found")
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
            
            ax.plot(time, area, label='asperity {}'.format(asperity))
            #ax[asperity].plot(time, area, label='asperity {}'.format(asperity))
            #ax[asperity].plot(time, num, label = 'num') 
            print(asperity)            
            

            nums_temp.append(num)
            areas_temp.append(area)
            

        nums.append(np.asarray(nums_temp).mean(axis=0))
        areas.append(np.asarray(areas_temp).mean(axis=0))
        times.append(time)
        
        #if save:
        #    plt.savefig(fig_dir + 'png/area_temp{}_force{}_hi{}_seed{}_erratic{}_{}.png'.format(temp,
        #                                               force, height, seed, grid[0], grid[1]))


nums = np.asarray(nums)
areas = np.asarray(areas)

#################################
### LINE PLOTS WITH COLORBAR
#################################

#lc = multiline(times, nums, temps, ax=ax, lw=2, cmap='cividis')
#axcb = fig.colorbar(lc, ax=ax)
#axcb.set_label(r"$T$ [K]")

plt.title('area of erratic asperities {}'.format(args['erratic']))
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.legend()
plt.tight_layout()
if save:
    plt.savefig(fig_dir + 'area_temp{}_force{}_hi{}_seed{}_erratic{}_{}.png'.format(temp, 
                                                       force, height, seed, grid[0], grid[1]))
#plt.show()
#stop

"""
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

"""
