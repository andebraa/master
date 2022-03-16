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


def load_max_static(temp, vel, force, orientation, grid, template_lc, template_ms, seeds):
    
    ms_files = template_ms.format(temp, vel, force, orientation, grid[0], grid[1])
    ms_all = []
    
    files = glob(ms_files)
    # ms files: time [nS] max friction [mN] 
    assert files != []
    for file in glob(ms_files):
        for seed in seeds:
            if str(seed) in str(file):
                print(seed)
                time, ms = loadtxt(file)
                ms_all.append(ms)

    mean_static = mean(ms_all, axis = 0)
    return ms_all, mean_static


def plot_max_static_vs_thiccness():
    # user input
    temp = 1800
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'


    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    style.use('seaborn') 
    #fig, ax = plt.subplots(2,15)
    #axs = axs.ravel()

    seed_dict_5 = {1: [36015,37461,77220], 2: [49156,64486,73803],
                 3: [30642,74822,90272], 4: [20939,86781,87609],
                 5: [25642,46012,71581], 6: [86406,91501]}
    colours = {1.25: 'go', 5:'ro'}
    
    vel_seed_uc = {5: seed_dict_5} #, 1.25: seed_dict_125}
    
    all_mean_static = np.zeros(len(seed_dict_5)) #num keys
    
    for vel, seed_dict in vel_seed_uc.items():
        for i, (uc, seed) in enumerate(seed_dict.items()):
            ms_all, mean_static = load_max_static(temp, vel, force, orientation, grid, 
                                                  template_lc, template_ms, seed) 
            all_mean_static[i] = mean_static
            plt.plot(uc, mean_static, colours[vel])
            #for ms in ms_all:
            #    plt.plot(hup[i], ms, 'ob')
    

    plt.xlabel(r"$hup$ [pm]")
    plt.ylabel(r"$f$ [$\mu$N]")
    plt.title('mean max static vs upper plate thicness, green: 1.25, red: 5')
    plt.savefig(fig_dir + 'png/max_static_chess.png')

    

if __name__ == '__main__':

    # user input
    temp = 1800
    vel = 5
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'
    
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

    plot_max_static_vs_thiccness()
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


    """ #theese are relax seeds
    seeds_5 =  [24296,84160,79210]
    seeds_8 =  [35701,84452,85253]
    seeds_9 =  [34105,10800,42330]
    seeds_11 = [89027,21504,40454]
    seeds_12 = [80577,25262,14194]
    seeds_14 = [82798,96793,76957]
    seeds_16 = [81147,61987,51593]
    seeds_18 = [51735,44709,45053]
    seeds_20 = [70164,14798,28863]
    seeds_22 = [43346,72761,24220]
    seeds_24 = [41110,27848,58248]
    seeds_26 = [29628,48780,22090]
    seeds_28 = [47223,86471,56804]
    seeds_30 = [55262,76203,84098]
    seeds_33 = [39463,84117,53537]
    """
