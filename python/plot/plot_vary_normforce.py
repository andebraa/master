import re
import json
from glob import glob
from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from multiline import multiline
from matplotlib import style
from plot_utils import sigmoid, rip_norm, test_rip_norm, fit_sigmoid
plt.style.use('seaborn')

from plot_load_curves import load_displacement, load_rise, load_load_curves, load_max_static






def load_vs_normal_force():

    # user input
    temp = 2300
    vel = 5
    orientation = 110
    grid = (4,4)
    erratic = True
    asperities = 8

    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'
    highz_dir = '../../txt/high_z/'

    load_curve_dir = project_dir + 'txt/load_curves/erratic/vary_normforce/'
    max_static_dir = project_dir + 'txt/max_static/erratic/vary_normforce/'
    rise_dir = project_dir + 'txt/rise/erratic/vary_normforce/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
    template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid4_4.txt'

    #axs1 is load curves over time
    fig, axs = plt.subplots(2,2, figsize = (12,12))
    #axs2 is max static and rise
    fig2, axs2 = plt.subplots(2)
    axs2 = axs2.ravel()
    axs = axs.ravel()
    #axs2 = []
    #for ax in axs:
    #    axs2.append(ax.twinx())
    #axs2 = np.array((axs2))
    vary_norm = {0:(43898,74145,26926), 0.0001: (89567,11678,27618), 0.001:(43698,76180,77635), 0.01:(83673,80288,70338)}

    man_init_strange = {1: '[[0,1,1,0][0,1,1,0][0,1,1,0][0,1,1,0]]', 2: '[[0,0,0,0][1,1,1,1][1,1,1,1][0,0,0,0]]',
                        3: '[[0,1,0,0][1,1,1,0][1,1,1,0][0,1,0,0]]', 0: '[[1,0,1,0][0,1,0,1][1,0,1,0][0,1,0,1]]'}

    #c = plt.cm.viridis(np.array(tuple(varyforce))/(0.01))
    c = plt.cm.viridis((3 - np.arange(len(vary_norm)))/(3 - 0 + 0.01))
    for i, (normforce, seed) in enumerate(vary_norm.items()):

        load_curves_all, load_curves_mean = load_load_curves(temp, vel, normforce, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)


        max_static_all, max_static_mean = load_max_static(temp, vel, normforce, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)

        rise_all, rise_mean = load_rise(temp, vel, normforce, asperities, orientation,
                                                        grid, template_r, 0, seed, False)

        #disp_files = f'../../txt/displacement/production/displacement_temp{temp}_vel{vel}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}_errgrid4_4.txt'
        #disp, disp_mean = load_displacement(temp, vel, force, orientation, grid, disp_files, initnum)


        #maxz_file = glob(heights_file)[0]
        #print('glob heights file ',len(glob(heights_file)))
        #assert len(glob(heights_file)) == 1

        
        for j,curve in enumerate(load_curves_all):
            axs[i].plot(curve[:,0], curve[:,1], alpha = 0.4, c=c[j])
        for j, max_static in enumerate(max_static_all):
            axs[i].plot(max_static[0], max_static[1], 'bo')
            axs2[0].plot(normforce, max_static[1], 'o', c=c[j])
        #axs2[0].plot(normforce, max_static_mean[1], '*', label='mean')
        for j,rise in enumerate(rise_all):
            axs2[1].plot(normforce, rise, 'o', c = c[j])
        #axs2[1].plot(normforce, rise_mean, '*', label='mean')
        axs2[0].legend()

    
        axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = f'average')
        axs[i].legend()
        axs[i].set_xlabel(r"$t_p$ [ns]")
        axs[i].set_ylabel(r"$f$ [$\mu$N]")
        axs[i].set_title(f'Normal force {normforce} [$\mu$N]')
        axs[i].set_ylim([-0.03, 0.5])

    fig.suptitle(f"Load curves for the chess system with increasing normal force")
    fig.tight_layout(pad=1.8)
    
    outname = 'vary_normforce.png'

    print(f'saved fig to {fig_dir + outname}')
    fig.savefig(fig_dir + outname, dpi = 200)

    axs2[0].set_title('maximum static')
    axs2[1].set_title('slope of sigmoid fit')
    axs2[0].set_xlabel('normal force [$\mu$N]')
    axs2[1].set_xlabel('normal force [$\mu$N]')
    axs2[0].set_ylabel(r"$f$ [$\mu$N]")
    axs2[1].set_ylabel(r"$f$ [$\mu$N]")


    fig2.suptitle(f'slope and maximum static friction for varying normal force, chess layout')
    fig2.tight_layout()
    fig2.savefig(fig_dir + 'varying_normforce_rise_maxstatic.png', dpi = 200)

if __name__ == '__main__':

    load_vs_normal_force()
