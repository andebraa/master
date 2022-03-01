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
                time, ms = loadtxt(file)
                ms_all.append(ms)

    mean_static = mean(ms_all, axis = 0)
    return ms_all, mean_static


def plot_max_static_vs_thiccness():
    # user input
    temp = 2300
    vel = [5,1.25]
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    # first run vel 5 time 500
    _seeds_5 =  [88753, 12754, 91693] # thicc 80
    _seeds_8 =  [50219, 31693, 19478] # thicc 83
    _seeds_9 =  [81094, 81717, 10840] # thicc 85
    _seeds_11 = [89936, 25987, 82860] # thicc 85
    _seeds_12 = [63620, 46351, 18735] # thicc 90
    _seeds_14 = [62648, 89682, 30607] # thicc 90
    _seeds_16 = [17767, 58195, 19686] # thicc 95
    _seeds_18 = [11084, 50879, 83355] # thicc 93
    _seeds_20 = [81955, 86485, 61282] # thicc 95
    _seeds_22 = [96804, 43682, 88372] # thicc 100
    _seeds_24 = [64771, 82158, 63871] # thicc 100
    _seeds_26 = [95317, 18462, 11729]#thicc 100
    _seeds_28 = [54648,88413,94253] #thicc 103
    _seeds_30 = [92651,19224,85380] #thicc 105
    _seeds_33 = [64798,34149] #thicc 109
    


    # second push run vel 1.25
    seeds_5 = [71361,91111,63445] # 80
    seeds_8 = [12890,62608,29899] # 83
    seeds_9 = [70529,45585,64900]
    seeds_11 = [66909,27035,43111] # 85 
    seeds_12 = [81809,93141,56900]
    seeds_14 = [33447,88504,79793] # 90
    seeds_18 = [75942,21663,49508] # 93
    seeds_16 = [67321,29830,36667]
    seeds_20 = [77113,99307,62931] # 95
    seeds_22 = [47606,72506,44762]
    seeds_24 = [47009,37801,56714]
    seeds_26 = [54238,10257,73002] # 100
    seeds_28 = [71970,74062,60542] # 103
    seeds_30 = [81636,35286,69718] # 105
    seeds_33 = [90953,90762,47980] # 109

    seeds = {1.25: [seeds_5, seeds_8, seeds_9, seeds_11, seeds_12, seeds_14, 
            seeds_16, seeds_18, seeds_20, seeds_22, seeds_24, seeds_26, 
            seeds_28, seeds_30, seeds_33], 5: [_seeds_5, _seeds_8, _seeds_9, _seeds_11, _seeds_12, _seeds_14, 
            _seeds_16, _seeds_18, _seeds_20, _seeds_22, _seeds_24, _seeds_26, 
            _seeds_28, _seeds_30, _seeds_33]}


    hup = [5,8,9,11,12,14,16,18,20,22,24,26,28,30,33]

    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'
    style.use('seaborn') 
    #fig, ax = plt.subplots(2,15)
    #axs = axs.ravel()
    all_mean_static = np.zeros(len(seeds[1.25])*2)

    fig_num = 0
    
    for vel, _seeds in seeds.items():
        for i, seed in enumerate(_seeds):
            ms_all, mean_static = load_max_static(temp, vel, force, orientation, grid, 
                                                  template_lc, template_ms, seed) 
            all_mean_static[i] = mean_static
            plt.plot(hup[i], mean_static, 'o', label=vel)
            #for ms in ms_all:
            #    plt.plot(hup[i], ms, 'ob')
        plt.legend()
    plt.xlabel(r"$hup$ [pm]")
    plt.ylabel(r"$f$ [$\mu$N]")
    plt.title('mean max static vs upper plate thicness')
    plt.savefig(fig_dir + 'png/max_static_vs_hup2.png')

    

if __name__ == '__main__':

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
