"""
Crystal Aging Project

Plot load curves as curves and heatmaps

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import re
from glob import glob
from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from multiline import multiline
from matplotlib import style
plt.style.use('seaborn')

# user input
temp = 2300
vel = 5
force = 0.001
orientation = 100
grid = (4,4)
erratic = True


# paths
project_dir = '../../'
fig_dir = project_dir + 'fig/'

#seeds = [27278,70295,98184,31906,35578,69872] 
seeds = [42439,51019,79411,14943]

if erratic:
    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'
    
    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'

elif grid:
    load_curve_dir = project_dir + 'txt/load_curves/grid/'
    max_static_dir = project_dir + 'txt/max_static/grid/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_grid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_grid{}_{}.txt'


# load load curves
load_curve_files = template_lc.format(temp, vel, force, orientation, grid[0], grid[1])
load_curves_all = []

for file in glob(load_curve_files):
    load_curves = loadtxt(file)
    print(file)
    for seed in seeds:
        if str(seed) in str(file):
            print(file)
            load_curves_all.append(load_curves)

load_curves_all[1] = load_curves_all[1][:len(load_curves_all[0])]
load_curves_all = np.array(load_curves_all)
shortest = np.argmin(load_curves_all) 

load_curves = mean(load_curves_all, axis=0)

load_curves = load_curves.reshape(-1, 1001, 2)   # assuming that all curves have 1001 points

"""
# extract push times
push_times = []
with open(load_curve_file, 'r') as f:
    for line in f:
        if 'push time' in line:
            push_times.append(float(line.split()[3]))
"""

# load max static curves
max_point_files = template_ms.format(temp, vel, force, orientation, grid[0], grid[1])
max_static_all = []
for file in glob(max_point_files):
    for seed in seeds:
        if str(seed) in str(file):
            max_static = loadtxt(file)
            max_static_all.append(max_static)
            print(file)
max_static = mean(max_static_all, axis=0)

push_times = [0.2, 2, 20]
print(np.shape(load_curves[0,:,0]))
for i in range(len(seeds)):

    plt.plot(load_curves_all[i,:, 0], load_curves_all[i,:, 1], 'b--',label=seeds[i])
plt.plot(load_curves[0,:,0], load_curves[0,:,1], '-g', label = 'mean' )
plt.xlabel(r"$t_p$ [ns]")
plt.ylabel(r"$f$ [$\mu$N]")
plt.title(f"load curves for {len(seeds)} runs, force {force}, vel {vel}")
plt.legend()
plt.savefig(fig_dir + 'png/load_curves_runs6_rseed48329.png')
#plt.savefig(fig_dir + 'pgf/load_curves_2450_all.pgf')
#plt.show()
"""
stop

# select a few curves
select = [20, 40, 60, 80, 99]
push_times = asarray(push_times)[select]
times = [1, 2, 3, 4, 5]
load_curves = load_curves[select]
max_static = max_static[select]


# cut the curves
load_curves = load_curves[:, :600]


# plot selected curves with legends and max static force marked with a X
fig, ax = plt.subplots()
for i, time in enumerate(times):
    plt.plot(load_curves[i, :, 0], load_curves[i, :, 1], label=fr'$t={time}$ ns')
for i, time in enumerate(push_times):
    plt.plot(max_static[i, 0]-time, max_static[i, 1], 'kX', markersize=10)
plt.legend(loc='best')
plt.xlabel(r"$t_p$ [ns]")
plt.ylabel(r"$f$ [$\mu$N]")
plt.savefig(fig_dir + 'png/load_curves_2450_selected.png')
plt.savefig(fig_dir + 'pgf/load_curves_2450_selected.pgf')
#plt.show()
"""
