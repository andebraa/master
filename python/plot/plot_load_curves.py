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


def load_load_curves(temp, vel, force, orientation, grid, template_lc, template_ms, seeds):
    # load load curves
    load_curve_files = template_lc.format(temp, vel, force, orientation, grid[0], grid[1])
    load_curves_all = []
   

    files = glob(load_curve_files)
    assert files != []
    for file in glob(load_curve_files):
        load_curves = loadtxt(file)
        for seed in seeds:
            if str(seed) in str(file):
                print('found loadcurve ',file)
                load_curves_all.append(load_curves)
                print(len(load_curves))
    print('load curves shape: ', np.shape(load_curves_all))
    load_curves_all[1] = load_curves_all[1][:len(load_curves_all[0])]
    load_curves_all = np.array(load_curves_all)
    shortest = np.argmin(load_curves_all) 

    
    load_curves = mean(load_curves_all, axis=0)
    print(np.shape(load_curves))
    load_curves = load_curves.reshape(-1, np.shape(load_curves)[0], 2)   # assuming that all curves have 1001 points
    
    return load_curves_all, load_curves


"""
# extract push times
push_times = []
with open(load_curve_file, 'r') as f:
    for line in f:
        if 'push time' in line:
            push_times.append(float(line.split()[3]))
"""
def plot_load_curves_as_funciton_of_top_thiccness():
    # user input
    temp = 2300
    vel = 1.25
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    """ #first run vel 5
    seeds_5 =  [88753, 12754, 91693] # thicc 80
    seeds_8 =  [50219, 31693, 19478] # thicc 83
    seeds_9 =  [81094, 81717, 10840] # thicc 85
    seeds_11 = [89936, 25987, 82860] # thicc 85
    seeds_12 = [63620, 46351, 18735] # thicc 90
    seeds_14 = [62648, 89682, 30607] # thicc 90
    seeds_16 = [17767, 58195, 19686] # thicc 95
    seeds_18 = [11084, 50879, 83355] # thicc 93
    seeds_20 = [81955, 86485, 61282] # thicc 95
    seeds_22 = [96804, 43682, 88372] # thicc 100
    seeds_24 = [64771, 82158, 63871] # thicc 100
    seeds_26 = [95317, 18462, 11729]#thicc 100
    seeds_28 = [54648,88413,94253] #thicc 103
    seeds_30 = [92651,19224,85380] #thicc 105
    seeds_33 = [64798,34149] #thicc 109

    """
    """
    # second push run vel 5
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
    """
    """
        #third push run
    seeds_5 = [76532,67473,86988]
    seeds_8 = [22135,54054,39337]
    seeds_9 = [15007,95692,61395]
    seeds_11 = [31234,92172,49033]
    seeds_12 = [27448,57576,83094] 
    seeds_14 = [68672,65867,65400]
    seeds_16 = [57652,77804,75056]
    seeds_18 = [37474,72730,76985] 
    seeds_20 = [16010,24858,24113]
    seeds_22 = [19590,75450,95072] 
    seeds_24 = [63988,78860,45476] 
    seeds_26 = [35593,21768,33674]
    seeds_28 = [81910,33465] #46388 missing
    seeds_30 = [23317,44679,86430]
    seeds_33 = [66411,52069,63812]
    """

    #fourth push, 700 long
    seeds_5 = [97841,88985,79749] #80
    seeds_8 = [81474,90347,79290] #83
    seeds_9 = [40328,90215,62491]
    seeds_11 = [80371,12038,48116] # 85
    seeds_12 = [61347,50189,68738]
    seeds_14 = [19022,23781,73474] #90
    seeds_16 = [27598,75257,74926] # 95
    seeds_20 = [17821,40450,80080] # 95
    seeds_18 = [14130,95349,16972] #93
    seeds_22 = [64180,63781,84634] 
    seeds_24 = [64308,93573,48127] 
    seeds_26 = [78231,43336,42599] # 100
    seeds_28 = [28782,23246,41573] # 103
    seeds_30 = [48834,99626,28475] # 105
    seeds_33 = [89090,40422,52257] #109


    _seeds1 = [seeds_5, seeds_8, seeds_9, seeds_11]
    _seeds2 = [seeds_12, seeds_14, seeds_16, seeds_18]
    _seeds3 = [seeds_20, seeds_22, seeds_24, seeds_26]
    _seeds4 = [seeds_28, seeds_30, seeds_33]

    hup = [5,8,9,11,12,14,16,18,20,22,24,26,28,30,33]

    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}.txt'
    style.use('seaborn') 
    min_hup = np.min(hup)
    max_hup = hup[-1]

    fig, axs = plt.subplots(2,2)
   
    axs = axs.ravel()
    i = 0
    for j, seeds in enumerate([_seeds1, _seeds2, _seeds3, _seeds4]):
        for k,seed in enumerate(seeds):
            load_curves_all, load_curves = load_load_curves(temp, vel, force, orientation, 
                                                            grid, template_lc,template_ms, seed)
            c = plt.cm.viridis((max_hup - hup[i])/(max_hup - min_hup + 0.01))
            axs[j].plot(load_curves[0,:,0], load_curves[0,:,1], c=c, label = f'hup {hup[i]}' )
            for l in range(len(seed)):
                axs[j].plot(load_curves_all[l,:,0], load_curves_all[l,:,1], '--', alpha = 0.5, c=c)
            axs[j].legend()
            i += 1
            
    for ax in axs.flat:
        ax.set(xlabel=r"$t_p$ [ns]", ylabel = r"$f$ [$\mu$N]")
        ax.label_outer()
        
    #plt.xlabel(r"$t_p$ [ns]")
    #plt.ylabel(r"$f$ [$\mu$N]")
    fig.suptitle(f"Mean of three runs, for varying upper plate thicness")
    plt.savefig(fig_dir + 'png/load_curves_thicc_runs3_foursquare.png', dpi = 500)


def plot_all_curves_and_mean(temp, vel, force, orientation, grid, template_lc, template_ms, seeds):
    load_curves_all, load_curves = load_load_curves(temp, vel, force, orientation, grid, template_lc,template_ms, seeds) 

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
    plt.savefig(fig_dir + 'png/load_curves_second_rendition_all_and_mean.png')

def plot_mean_of_multiple(temp, vel, force, orientation, grid, template_lc, template_ms, seeds):
    for i in range(len(seeds)):
        load_curves, load_curves_mean = load_load_curves(temp, vel, 
                                                                force, orientation, 
                                                                grid, template_lc, 
                                                                template_ms, seeds[i])

        plt.plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label=seeds[i])
        plt.xlabel(r"$t_p$ [ns]")
    plt.ylabel(r"$f$ [$\mu$N]")
    plt.title(f"mean of multiple load curves relax seeds, force {force}, vel {vel}")
    plt.legend()
    plt.savefig(fig_dir + 'png/means_of_multiple.png')
    

if __name__ == '__main__':

    # user input
    temp = 2300
    vel = 1.25
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    #seeds1 = [27278,70295,98184,31906,35578,69872] 
    #seeds2 = [42439,51019,79411,14943]
    #seeds3 = [17744,77072,77201,88708]
    #seeds4 = [58958,67466,85867]
    #seeds5 = [12589, 50887] #thiccest
   

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

    #plot_all_curves_and_mean(temp, vel, force, orientation, grid, template_lc, template_ms, seeds)    
    #plot_mean_of_multiple(temp, vel, force, orientation, grid, template_lc, template_ms, [seeds1, seeds2, seeds3])
    plot_load_curves_as_funciton_of_top_thiccness()
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
