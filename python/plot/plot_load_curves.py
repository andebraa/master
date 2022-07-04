"""
Crystal Aging Project

Plot load curves as curves and heatmaps

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import re
import json
from glob import glob
from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from multiline import multiline
from matplotlib import style
plt.style.use('seaborn')

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

def plot_sigmoid(load_curve):
    pass

def load_displacement(temp, vel, force, orientation, grid, disp_template, initnum, seeds):
    disp_all = []
    for seed in seeds:
        lc_files = disp_template.format(temp, vel, force, asperities, initnum, seed, grid[0], grid[1])
        files = glob(disp_files)
        assert files != []
        for _file in glob(disp_files):
            disp = loadtxt(_file)
            disp_all.append(disp)
    disp_all = np.array(disp_all)
    disp_mean = mean(disp_all, axis=0)
    disp_mean = disp_mean.reshape(-1, np.shape(disp_mean)[0], 2)   # assuming that all curves have 1001 points
    
    return disp_all, disp_mean

def load_rise(temp, vel, force, asperities, orientation, grid, template_r, initnum, seeds, production):
    rise_all = []
    if isinstance(seeds, tuple) and len(seeds) > 1:
        for seed in seeds:
            if production:
                rise_files = template_r.format(temp, vel, force, asperities, orientation, initnum, seed, grid[0], grid[1])
            else:
                rise_files = template_r.format(temp, vel, force, asperities, orientation, seed, grid[0], grid[1])
            files = glob(rise_files)
            assert files != []
            for _file in glob(rise_files):
                rise = loadtxt(_file)
                rise_all.append(rise)
    else:
        if production:
            rise_files = template_r.format(temp, vel, force, asperities, orientation, initnum, seeds, grid[0], grid[1])
        else:
            rise_files = template_r.format(temp, vel, force, asperities, orientation, seeds, grid[0], grid[1])
        files = glob(rise_files)
        assert files != []
        for _file in glob(rise_files):
            rise = loadtxt(_file)
            rise_all.append(rise)

    rise_all = np.array(rise_all)
    if isinstance(seeds, tuple) and len(seeds) > 1:
        rise = mean(rise_all, axis=0)
        #rise = rise.reshape(-1, np.shape(rise)[0], 2)   # assuming that all curves have 1001 points
    else:
        rise = None

    return rise_all, rise

def load_load_curves(temp, vel, force, asperities, orientation, grid, template_lc, template_ms, initnum, seeds, production):
    # load load curves
    load_curves_all = []
    if isinstance(seeds, tuple) and len(seeds) > 1: 
        for seed in seeds: 
            if production:
                load_curve_files = template_lc.format(temp, vel, force, asperities, orientation, initnum, seed, grid[0], grid[1])
            else:
                load_curve_files = template_lc.format(temp, vel, force, asperities, orientation, seed, grid[0], grid[1])

            files = glob(load_curve_files)
            assert files != []
            for _file in glob(load_curve_files):
                load_curves = loadtxt(_file)
                load_curves_all.append(load_curves)
    else:
        if production:
            load_curve_files = template_lc.format(temp, vel, force, asperities, orientation, initnum, seeds, grid[0], grid[1])
        else: 
            load_curve_files = template_lc.format(temp, vel, force, asperities, orientation, seeds, grid[0], grid[1])
        files = glob(load_curve_files)
        assert files != []
        for _file in glob(load_curve_files):
            load_curves = loadtxt(_file)
            load_curves_all.append(load_curves)
        
    load_curves_all = np.array(load_curves_all)
    if isinstance(seeds, list):
        load_curves = mean(load_curves_all, axis=0)
        load_curves = load_curves.reshape(-1, np.shape(load_curves)[0], 2)   # assuming that all curves have 1001 points
    else:
        load_curves = None
    return load_curves_all, load_curves


def load_max_static(temp, vel, force, asperities, orientation, grid, template_lc, template_ms, initnum, seeds, production):
    ms_all = []
   
    if isinstance(seeds, tuple):
        for seed in seeds:
            if production:
                ms_files = template_ms.format(temp, vel, force, asperities, orientation, initnum, seed, grid[0], grid[1])
            else:
                ms_files = template_ms.format(temp, vel, force, asperities, orientation, seed, grid[0], grid[1])
                
            files = glob(ms_files)
            # ms files: time [nS] max friction [mN] 
            assert files != []
            
            for file in glob(ms_files):
                time, ms = loadtxt(file)
                ms_all.append((time,ms))
        mean_static = mean(ms_all, axis = 0)
    else:
        if production:
            ms_files = template_ms.format(temp, vel, force, asperities, orientation, initnum, seeds, grid[0], grid[1])
        else:
            ms_files = template_ms.format(temp, vel, force, asperities, orientation, seeds, grid[0], grid[1])

        files = glob(ms_files)
        # ms files: time [nS] max friction [mN] 
        assert files != []
        
        for file in glob(ms_files):
            time, ms = loadtxt(file)
            ms_all.append((time,ms))
        mean_static = None

    return ms_all , mean_static


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
            axs[j].plot(ms_all[l][0], ms_all[l][1], 'o',c=c)
            axs[j].plot(load_curves_all[l,:,0], load_curves_all[l,:,1], '--', alpha = 0.5, c=c)
        axs[j].legend()
        axs2.legend()
        i += 1
            
    for ax in axs.flat:
        ax.set(xlabel=r"$t_p$ [ns]", ylabel = r"$f$ [$\mu$N]")
        ax.label_outer()
        
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

def plot_mean_of_multiple():
        # user input
    temp = 2300
    vel = 5
    orientation = 110
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
    rise_dir = project_dir + 'txt/rise/production/'


    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed*_errgrid{}_{}.txt'
    template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed*_errgrid4_4.txt'
    template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/sim_temp{}_force{}_asp{}_or{}_time{}_initnum{}_seed*_errgrid4_4/system_asp{}_or{}_uc{}_initnum*_errgrid4_4_auxiliary.json'
    
    fig, axs = plt.subplots(5,2, figsize = (20,20))
    axs = axs.ravel()

    fig2, axs2 = plt.subplots()
    for i in range(10):
        lc_files = glob(template_lc.format(temp, vel, force, asperities,orientation, i, grid[0], grid[1]))
        print(lc_files)
        rise_files = glob(template_r.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        ms_files = glob(template_ms.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        load_curves = []
        rise = []
        ms = []
        #finding the shortest in case one is longer and it needs to be truncated
        shortest = (10000000, 0) #length, index
        for j, lc_file in enumerate(lc_files):
            infile = loadtxt(lc_file)
            if np.shape(infile)[0] < shortest[0]:
                shortest = (np.shape(infile)[0], j)
            load_curves.append(np.array(infile))
        for j, load_curve in enumerate(load_curves):
            if j != shortest[1]:
                load_curves[j] = load_curves[j][:shortest[0]]

        for rise_file in rise_files:
            rise.append(loadtxt(rise_file))
        #for ms_file in ms_files:
        #    print(ms_file)
        #    ms.append(ms_file)
        axs[i].plot(load_curves[0][:,0], load_curves[0][:,1], label = f'rise {rise[0]}')
        axs[i].plot(load_curves[1][:,0], load_curves[1][:,1], label = f'rise {rise[1]}')
        axs[i].set_xlabel(r"$t_p$ [ns]")
        axs[i].set_ylabel(r"$f$ [$\mu$N]")
        axs[i].legend()
        axs2.plot(i, rise[0], 'o', color = 'blue')
        axs2.plot(i, rise[1], 'o', color = 'red')
        
        avg_lc = mean(load_curves)
        
        

    fig.suptitle(f"Two runs of the first 10 random configurations \n temp {temp}, force {force}, vel {vel}, asperities {asperities}, orientation {orientation}")
    fig.legend()
    fig.savefig(fig_dir + 'png/first_10_double.png')

    axs2.set_xlabel('random configuration number')
    axs2.set_ylabel('rise of simoid fit')
    fig2.suptitle(f"the rise of a fitted sigmoid curve, for the 10 first random 8 asperity configurations, \n temp {temp}, force {force}, vel {vel}, asperities {asperities}, orientation {orientation}")
    fig2.savefig(fig_dir + 'png/10_first_rise.png')

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

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}_seed{}_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}_seed{}_errgrid{}_{}.txt'
    
    foursquare = False

    if foursquare:
        fig, axs = plt.subplots(2,3, figsize = (10,10))
    else:
        fig, axs = plt.subplots(2, figsize = (10,10))
    axs = axs.ravel()
    axs2 = []
    for ax in axs:
        axs2.append(ax.twinx())
    axs2 = np.array((axs2))

    varyforce = {0.0001: 14738, 0.001:29336, 0.01:34053, 0:49495}

    for i, (force, seed) in enumerate(varyforce.items()):
        
        lc_files = template_lc.format(temp, vel, force, asperities, initnum, seed, grid[0], grid[1])
        heights_file =  highz_dir + f"maxz_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}.txt"
        print(lc_files)
        load_curves_all, load_curves_mean = load_load_curves(temp, vel, force, asperities,
                                                    grid, lc_files,template_ms, initnum)

        print('mean load curves shape: ',load_curves_mean.shape)
        print('all load curves shape: ',load_curves_all.shape)
        disp_files = f'../../txt/displacement/production/displacement_temp{temp}_vel{vel}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}_errgrid4_4.txt'
        disp, disp_mean = load_displacement(temp, vel, force, orientation, grid, disp_files, initnum)
        

        maxz_file = glob(heights_file)[0]
        print('glob heights file ',len(glob(heights_file)))
        assert len(glob(heights_file)) == 1
        
        for curve in load_curves_all:
            axs[i].plot(curve[:,0], curve[:,1])
        #height plot 
        data = np.loadtxt(maxz_file)
        timeframes = []
        height = []
        for row in data:
            timeframes.append(row[0]*timestep*0.001)
            height.append(row[1])
        
        timeframes = np.array(timeframes)
        height = np.array(height)

        foursquare = False
        if foursquare: 
            axs[i].plot(disp_mean[0,:,0], disp_mean[0,:,1], label = 'displacement')
            axs2[i].plot(timeframes, height, label = f'highest particle')
            axs2[i].grid(False)
            axs2[i].set_ylabel('Height [Å]')

            #load plot
            print(len(load_curves_mean[0,:,0]))
            axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = 'average')
            axs[i].set_xlabel(r"$t_p$ [ns]")
            axs[i].set_ylabel(r"$f$ [$\mu$N]")
            axs[i].set_title(f'normal force {force}')
        
        else:
            axs[0].plot(disp_mean[0,:,0], disp_mean[0,:,1], label = f'force {force}')
            axs[1].plot(disp_mean[0,:,0], disp_mean[0,:,1], label = f'force {force}')
            axs[0].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label=f'{force}')
            axs[1].plot(timeframes, height)
    
    plt.suptitle(f"temp {temp}, force {force}, vel {vel}")
    plt.legend()
    fig.tight_layout(pad=0.2)
    plt.savefig(fig_dir + 'production_varying_normalforce_height.png')


def plot_production(temp, vel, force, uc, asperities, time, orientation, grid, erratic, production = True):
    
    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    if production:
        load_curve_dir = project_dir + 'txt/load_curves/production/'
        max_static_dir = project_dir + 'txt/max_static/production/'
        rise_dir = project_dir + 'txt/rise/production/'

        template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid{}_{}.txt'
        template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid{}_{}.txt'
        template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
        template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/sim_temp{}_force{}_asp{}_or{}_time{}_initnum{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'
    else:
        load_curve_dir = project_dir + 'txt/load_curves/erratic/'
        max_static_dir = project_dir + 'txt/max_static/erratic/'
        rise_dir = project_dir + 'txt/rise/erratic/'

        template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
        template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
        template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid4_4.txt'
        template_aux = project_dir + 'simulations/sys_asp{}_uc{}/erratic/sim_temp{}_force{}_asp{}_or{}_time{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'


    fig, axs = plt.subplots(2,2, figsize = (15,15))
    axs = axs.ravel()
    #initseed = {0:(77222, 66232, 79443), 1:(29672, 40129), 2:(64364, 32077), 3:(33829, 84296),
    #            4:(29082, 59000), 5:(16388, 65451), 6:(69759, 69759), 7:(65472, 62780)}
    #initseed = {0: (47011, 82042), 1: (22453, 94902), 2: (21337, 87980), 3:(11962, 13930),
    #            4: (21979, 89876), 5: (43427, 48032)}
    #initseed = {0: (88094, 43563), 1: (98414, 72415), 2: (86494, 67638), 3: (94091, 77768)}
    initseed = {0: (44380, 20344), 1: (74493, 20107), 2: (82915, 64226), 3: (39869, 61527)}

    man_init_2asp = {0:'[[0,0,0,0][0,0,0,0][1,0,0,1][0,0,0,0]]', 1:'[[0,0,0,1][0,0,0,0][1,0,0,0][0,0,0,0]]',
                     2:'[[0,0,0,0][0,0,0,1][0,0,1,0][0,0,0,0]]', 3:'[[0,0,1,0][0,0,0,0][0,0,0,0][0,0,1,0]]',
                     4:'[[0,0,1,0][0,0,0,0][0,0,0,0][1,0,0,0]]', 5:'[[0,1,0,0][0,0,1,0][0,0,0,0][0,0,0,0]]',
                     6:'[[0,0,1,0][0,0,0,0][1,0,0,0][0,0,0,0]]', 7:'[[0,0,0,0][1,0,0,0][0,0,0,0][1,0,0,0]]'}

    man_init_strange = {0: '[[0,1,1,0][0,1,1,0][0,1,1,0][0,1,1,0]]', 1: '[[0,0,0,0][1,1,1,1][1,1,1,1][0,0,0,0]]',
                        2: '[[0,1,0,0][1,1,1,0][1,1,1,0][0,1,0,0]]', 3: '[[1,0,1,0][0,1,0,1][1,0,1,0][0,1,0,1]]'}
    strange = True
    temp_initseed = {0: 60352, 1: 90667, 2: 84066, 3: 22580}
    for i, (initnum, seeds) in enumerate(initseed.items()):
        if production:
            load_curves_all, load_curves_mean= load_load_curves(temp, vel, force, asperities, orientation,
                                                        grid, template_lc,template_ms, initnum, seeds, production)
            ms_all, ms_mean = load_max_static(temp, vel, force, asperities, orientation, grid,
                                     template_lc, template_ms, initnum, seeds, production)

            rise_all, rise_mean= load_rise(temp, vel, force, asperities, orientation,
                                                    grid, template_r, initnum, seeds, production)
        else:
            load_curves_all, load_curves_mean= load_load_curves(temp, vel, force, asperities, orientation,
                                                        grid, template_lc,template_ms,0, seeds, production)
            ms_all, ms_mean = load_max_static(temp, vel, force, asperities, orientation, grid,
                                     template_lc, template_ms,0, seeds, production)

            rise_all, rise_mean= load_rise(temp, vel, force, asperities, orientation,
                                                    grid, template_r,0, seeds, production)

        
        
        #extract system setup from auxiliary folder
        if asperities == 8:
            if isinstance(seeds, tuple) and len(seeds) > 1:
                seed = seeds[0]
            else:
                seed = seeds
            if production:
                with open (template_aux.format(asperities, uc, temp, force, asperities, orientation, 
                                     time, initnum, seed, asperities, orientation, uc, seed)) as fp:
                    #note that seeds contain runs of the same system, so all are similar to seeds[0]
                    aux_dict = json.loads(fp.read())
            else:
                with open (template_aux.format(asperities, uc, temp, force, asperities, orientation, 
                                     time, seed, asperities, orientation, uc, seed)) as fp:
                    #note that seeds contain runs of the same system, so all are similar to seeds[0]
                    aux_dict = json.loads(fp.read())

            aux_dict['erratic'] = np.asarray(aux_dict['erratic'])

        #print('ms all, ms mean ', ms_all, ms_mean) 
        #print('load curves', np.shape(load_curves_all), np.shape(load_curves_mean))
        for j, load_curve in enumerate(load_curves_all):
            axs[i].plot(load_curve[:,0], load_curve[:,1], label = f'rise: {rise_all[j]:.4e}')
            axs[i].legend()



        #for ms in ms_all:
        #   axs[i].plot(ms[0], ms[1], 'o') #this is just proprietary

        axs[i].set_xlabel(r"$t_p$ [ns]")
        axs[i].set_ylabel(r"$f$ [$\mu$N]")
        if asperities == 2:
            axs[i].set_title(man_init_2asp[i])
        elif asperities ==8 and not strange:
            axs[i].set_title(f'rise: {rise_all}, mean: {rise_mean}')
            
            #axs[i].set_title(aux_dict['erratic'])
        elif strange:
            axs[i].set_title(man_init_strange[i])
        
        push_start_indx = (np.abs(load_curves_all[0][:,0] - 1.0)).argmin()
        push_stop_indx = (np.abs(load_curves_all[0][:,0] - 1.03)).argmin()

        #axs[i].set_ylim(bottom = -0.02, top = 0.07)
        #axs[i].set_xlim(left = 0.5, right = 1.7)
        #axs[i].legend(f'mean rise: {rise_mean}') 
        
        #axs[i].axvline(load_curves_all[0][push_start_indx,0], alpha = 0.5)
        #axs[i].axvline(load_curves_all[0][push_stop_indx,0], alpha = 0.5)
    
    plt.subplots_adjust(hspace=0.3)
    plt.suptitle(f"temp {temp}, force {force}, vel {vel}, asperities {asperities}, orientation {orientation}")
    plt.legend()
    plt.savefig(fig_dir + f'production_varying_initnum_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_time{time}_strange.png')

        


if __name__ == '__main__':

    # user input
    temp = 2300
    time = 2000
    vel = 5
    force = 0
    orientation = 110
    uc = 5
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
    plot_mean_of_multiple()
    #plot_load_curves_as_funciton_of_top_thiccness()
    #load_vs_normal_force()
    #plot_single_loadcurve()
    plot_production(temp, vel, force, uc, 8, time,orientation, grid, erratic, production = False)
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


