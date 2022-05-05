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


def load_displacement(temp, vel, force, orientation, grid, disp_files, initnum):
    # load load curves
    disp_all = []
   
    files = glob(disp_files)
    assert files != []
    for _file in glob(disp_files):
        disp = loadtxt(_file)
        disp_all.append(disp)
    #load_curves_all[1] = load_curves_all[1][:len(load_curves_all[0])]
    disp_all = np.array(disp_all)
    #shortest = np.argmin(load_curves_all) 
    disp_mean = mean(disp_all, axis=0)
    disp_mean = disp_mean.reshape(-1, np.shape(disp_mean)[0], 2)   # assuming that all curves have 1001 points
    
    return disp_all, disp_mean


def load_load_curves(temp, vel, force, orientation, grid, load_curve_files, template_ms, initnum):
    # load load curves
    load_curves_all = []
   
    print(load_curve_files)
    files = glob(load_curve_files)
    assert files != []
    for _file in glob(load_curve_files):
        load_curves = loadtxt(_file)
        #print('found loadcurve ',_file)
        #print('load curves shape: ', np.shape(load_curves))
        load_curves_all.append(load_curves)
    #load_curves_all[1] = load_curves_all[1][:len(load_curves_all[0])]
    load_curves_all = np.array(load_curves_all)
    #shortest = np.argmin(load_curves_all) 
    load_curves = mean(load_curves_all, axis=0)
    load_curves = load_curves.reshape(-1, np.shape(load_curves)[0], 2)   # assuming that all curves have 1001 points
    
    return load_curves_all, load_curves


def load_max_static(temp, vel, force, orientation, grid, template_lc, ms_files, seeds):
    ms_all = []
    
    files = glob(ms_files)
    # ms files: time [nS] max friction [mN] 
    assert files != []
    for file in glob(ms_files):
        for seed in seeds:
            print('seed ', seed)
            if str(seed) in str(file):
                print(' found seed ', seed)
                time, ms = loadtxt(file)
                ms_all.append((time,ms))

    #print(ms_all)
    #mean_static = mean(ms_all, axis = 0)
    return ms_all#, mean_static


#def plot_max_static_for_speeds():


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
    vel = 5
    force = 0.001
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    #seed_dict = {1: [40525,37063,90058],
    #             2: [30643,69590,85108],
    #             3: [33852,81835,65387],
    #             4: [23383,57218,24832],
    #             5: [22125,97481,26403],
    #             6: [84340,13006,94745],
    #             7: [94340,52540,92005],
    #             8: [11394, 11394]}


#    seed_dict = {1: [36015,37461,77220], 2: [49156,64486,73803],
#                 3: [30642,74822,90272], 4: [20939,86781,87609],
#                 5: [25642,46012,71581], 6: [86406,91501]}


    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    style.use('seaborn') 
    min_hup = 1
    max_hup = 8

    fig, axs = plt.subplots(4,2)
    fig2 = plt.figure()
    axs2 = fig2.add_subplot(111)

    axs = axs.ravel()
    i = 0
    for j, (uc, seeds) in enumerate(seed_dict.items()):
        print(seeds)
        print('i :',i)
        print('j :',j)
        load_curves_all, load_curves = load_load_curves(temp, vel, force, orientation, 
                                                        grid, template_lc,template_ms, seeds)

        ms_all, ms_mean = load_max_static(temp, vel, force, orientation, grid,
                                 template_lc, template_ms, seeds)
        c = plt.cm.viridis((max_hup - uc)/(max_hup - min_hup + 0.01))
        if len(seeds) > 2:
            axs[j].plot(load_curves[0,:,0], load_curves[0,:,1], c=c, label = f'uc {uc}' )
            axs2.plot(ms_mean[0], ms_mean[1],'*', label = f'uc {uc}', c=c)
        print(np.shape(ms_all))
        for l in range(len(seeds)):
            print('l :',l)
            # ms_all contains tuples (time, ms)
            print(ms_all[l][0], ms_all[l][1])
            #axs2.plot(ms_all[l][0]*vel, ms_all[l][1], 'o')
            axs[j].plot(ms_all[l][0], ms_all[l][1], 'o',c=c)
            axs[j].plot(load_curves_all[l,:,0], load_curves_all[l,:,1], '--', alpha = 0.5, c=c)
        axs[j].legend()
        axs2.legend()
        i += 1
            
    for ax in axs.flat:
        ax.set(xlabel=r"$t_p$ [ns]", ylabel = r"$f$ [$\mu$N]")
        ax.label_outer()
        
    #plt.xlabel(r"$t_p$ [ns]")
    #plt.ylabel(r"$f$ [$\mu$N]")
    axs2.set_xlabel('displacement [nm]')
    axs2.set_ylabel(r"$f$ [$\mu$N]")
    fig2.suptitle(f'max static vs displacement for various thicnessess of upper plate')
    fig2.savefig(fig_dir + 'png/displacement_vs_maxstatic_chess.png')
    fig.suptitle(f"Mean of three runs, for varying upper plate thicness temp {temp}")
    fig.savefig(fig_dir + 'png/load_curves_varying_uc_ms_chess_2300.png', dpi = 500)

    
    plt.close()

    

def plot_all_curves_and_mean(temp, vel, force, asperities, grid, template_lc, template_ms, initnum):
    load_curves_all, load_curves = load_load_curves(temp, vel, force, orientation, grid, template_lc,template_ms, seeds) 

    # load max static curves
    max_point_files = template_ms.format(temp, vel, force, asperities, initnum, grid[0], grid[1])

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
    

def plot_single_loadcurve():
    # user input
    temp = 2300
    vel = 5
    force = 0
    orientation = 100
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/png/'


    load_curve_dir = project_dir + 'txt/load_curves/erratic/'
    max_static_dir = project_dir + 'txt/max_static/erratic/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed*_errgrid{}_{}_chess.txt'
    style.use('seaborn')
    min_hup = 1
    max_hup = 8
    seeds = [44066, 44066]


    load_curve, load_curves_mean = load_load_curves(temp, vel,
                                                                force, orientation,
                                                                grid, template_lc,
                                                                template_ms, seeds)
    
    print(load_curve.shape)
    plt.plot(load_curve[0,:,0], load_curve[0,:,1])
    #plt.plot(load_curves_mean[:,:,0],load_curves_mean[:,:,1])
    plt.xlabel(r"$t_p$ [ns]")
    plt.ylabel(r"$f$ [$\mu$N]")

    plt.title(f'temp {temp}, vel {vel}, force{force}, 4x4 chess')
    plt.savefig(fig_dir + 'no_force.png')

def load_vs_normal_force():

    # user input
    temp = 2300
    vel = 5
    orientation = 100
    grid = (4,4)
    erratic = True
    asperities = 8
    initnum = 0
    timestep = 0.002
    time = 1800
    reltime = 800
    pushtime = 1000
    relframe = int(reltime/timestep)
    frames = int(time/timestep)
    reldist = np.zeros((reltime))
    pushdist = np.linspace(0,time, 1000)
    pushdist = np.concatenate((reldist, pushdist)) 

    lc_len = 361
    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'
    highz_dir = '../../txt/high_z/'

    load_curve_dir = project_dir + 'txt/load_curves/production/'
    max_static_dir = project_dir + 'txt/max_static/production/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}_seed*_errgrid{}_{}.txt'

    fig, axs = plt.subplots(2,2, figsize = (10,10))
    axs = axs.ravel()
    axs2 = []
    for ax in axs:
        axs2.append(ax.twinx())
    axs2 = np.array((axs2))

    for i, force in enumerate([0, 0.0001, 0.001, 0.01]):
        
        lc_files = template_lc.format(temp, vel, force, asperities, initnum, grid[0], grid[1])
        heights_file =  highz_dir + f"maxz_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*.txt"
        print(lc_files)
        load_curves_all, load_curves_mean = load_load_curves(temp, vel, force, asperities,
                                                    grid, lc_files,template_ms, initnum)

        disp, disp_mean = load_displacement(temp, vel, force, orientation, grid, disp_files, initnum)
        
        maxz_file = glob(heights_file)[0]
        print('glob heights file ',len(glob(heights_file)))
        assert len(glob(heights_file)) == 1
        
        for curve in load_curves_all:
            axs[i].plot(curve[:,0], curve[:,1])
        #height plot 
        seed = re.findall(r'\d+', maxz_file)[-1]
        data = np.loadtxt(maxz_file)
        timeframes = []
        height = []
        for row in data:
            timeframes.append(row[0]*timestep*0.001)
            height.append(row[1])
        
        timeframes = np.array(timeframes)
        
        height = np.array(height)
        axs[i].plot(disp_mean[0,:,0], disp_mean[0,:,1], label = 'displacement')
        axs2[i].plot(timeframes, height, label = f'highest particle')
        axs2[i].grid(False)
        axs2[i].set_ylabel('Height [Å]')

        #load plot
        #print('mean load curves shape: ',load_curves_mean.shape)
        #print('all load curves shape: ',load_curves_all.shape)
        print(len(load_curves_mean[0,:,0]))
        axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = 'average')
        axs[i].plot(np.linspace(0, time*0.001, len(pushdist)), pushdist*0.001, label = 'push distance')
        axs[i].set_xlabel(r"$t_p$ [ns]")
        axs[i].set_ylabel(r"$f$ [$\mu$N]")
        axs[i].set_title(f'normal force {force}')
    plt.suptitle(f"temp {temp}, force {force}, vel {vel}")
    plt.legend()
    fig.tight_layout(pad=0.2)
    plt.savefig(fig_dir + 'production_varying_normalforce_height.png')


def plot_production(temp, vel, force, asperities, orientation, grid, erratic):
    
    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'


    load_curve_dir = project_dir + 'txt/load_curves/production/'
    max_static_dir = project_dir + 'txt/max_static/production/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}_seed{}_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}_seed{}_errgrid{}_{}.txt'

    fig, axs = plt.subplots(4,3, figsize = (10,10))
    axs = axs.ravel()
    initseed = {0: 77800, 1:36173, 2:47530, 3:33479, 4:92732, 5:31470, 6:81050, 7:49079, 8:20661, 9:45424, 10:52221, 11:27048} 
    print(template_lc)
    for i, (initnum, seed) in enumerate(initseed.items()):
        
        lc_files = template_lc.format(temp, vel, force, asperities, initnum, seed, grid[0], grid[1])
        print(lc_files)
        load_curves_all, load_curves_mean= load_load_curves(temp, vel, force, asperities,
                                                    grid, lc_files,template_ms, initnum)
        
        ms_files = template_ms.format(temp, vel, force, asperities, initnum, seed, grid[0], grid[1])
        #ms_all, ms_mean = load_max_static(temp, vel, force, asperities, grid,
        #                     lc_files, ms_files, initnum)
        for curve in load_curves_all:
            axs[i].plot(curve[:,0], curve[:,1])
    
        print('mean load curves shape: ',load_curves_mean.shape)
        print('all load curves shape: ',load_curves_all.shape)
        axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = 'average')
        axs[i].set_xlabel(r"$t_p$ [ns]")
        axs[i].set_ylabel(r"$f$ [$\mu$N]")
    plt.title(f"temp {temp}, force {force}, vel {vel}")
    plt.legend()
    plt.savefig(fig_dir + 'production_varying_initnum_first10.png')

        


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

    #plot_all_curves_and_mean(temp, vel, force, orientation, grid, template_lc, template_ms, seeds)    
    #plot_mean_of_multiple(temp, vel, force, orientation, grid, template_lc, template_ms, [seeds1, seeds2, seeds3])
    #plot_load_curves_as_funciton_of_top_thiccness()
    #load_vs_normal_force()
    #plot_single_loadcurve()
    plot_production(temp, vel, force, 8,orientation, grid, erratic)
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


