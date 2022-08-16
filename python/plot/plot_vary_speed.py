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
from sklearn.metrics import r2_score


plt.style.use('seaborn')

from plot_load_curves import load_displacement, load_rise, load_load_curves, load_max_static






def load_vs_normal_force():

    # user input
    temp = 2300
    _vel = 5
    orientation = 110
    grid = (4,4)
    erratic = True
    asperities = 8
    force = 0

    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'
    highz_dir = '../../txt/high_z/'

    load_curve_dir = project_dir + 'txt/load_curves/erratic/vary_speed/'
    max_static_dir = project_dir + 'txt/max_static/erratic/vary_speed/'
    rise_dir = project_dir + 'txt/rise/erratic/vary_speed/'

    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
    template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid4_4.txt'

    #axs1 is load curves over time
    fig, axs = plt.subplots(2,2, figsize = (12,12))
    #axs2 is max static and rise
    fig2, axs2 = plt.subplots(3, figsize = (12, 8))
    fig3, axs3 = plt.subplots() #fake fig for sigmax
    axs2 = axs2.ravel()
    axs = axs.ravel()
    #varyspeed = {2:(55910,60930,14424),5:(72005,76229,37333), 7:(21702,77727,96687), 10:(56649,11605,41397)}
    varyspeed_alt = {1: (66526), 2:(55910,60930,14424), 3:(90254), 5:(72005,76229,37333), 7:(21702,77727,96687), 
                     8:(48242), 10:(56649,11605,41397), 13: (63868)}


    c = plt.cm.viridis((3 - np.arange(len(varyspeed_alt)))/(3 - 0 + 0.01))
    
    ms_vels = []
    sigmax_vels = []
    vels = []
    for i, (vel, seed) in enumerate(varyspeed_alt.items()):

        load_curves_all, load_curves_mean = load_load_curves(temp, _vel, force, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)


        max_static_all, max_static_mean = load_max_static(temp, _vel, force, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)

        rise_all, rise_mean = load_rise(temp, _vel, force, asperities, orientation,
                                                        grid, template_r, 0, seed, False)


        _sigmax_vels = []
        for j,curve in enumerate(load_curves_all):
        #    axs[i].plot(curve[:,0], curve[:,1], alpha = 0.4, c=c[j])
            axs2[2].plot(vel, fit_sigmoid(curve, fig3, axs3), 'o', c=c[j])
            sigmax_vels.append(fit_sigmoid(curve, fig3, axs3))
            vels.append(vel)
        for j, max_static in enumerate(max_static_all):
        #    axs[i].plot(max_static[0], max_static[1], 'bo')
            axs2[0].plot(vel, max_static[1], 'o', c=c[j])
            ms_vels.append(max_static[1])
        #axs2[0].plot(normforce, max_static_mean[1], '*', label='mean')
        for j,rise in enumerate(rise_all):
            axs2[1].plot(vel, rise, 'o', c = c[j])
        #axs2[1].plot(normforce, rise_mean, '*', label='mean')
        axs2[0].legend()

    
        #axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = f'average')
        #axs[i].legend()
        #axs[i].set_xlabel(r"$t_p$ [ns]")
        #axs[i].set_ylabel(r"$f$ [$\mu$N]")
        #axs[i].set_title(f'velocity {vel} [m/s]')
        #axs[i].set_ylim([-0.02, 0.14])

    sigmax_logfit = np.polyfit(np.log(vels), sigmax_vels, 1)
    sigmax_linfit = np.polyfit(vels, sigmax_vels, 1)
    polfit_plot_vels = np.linspace(vels[0], vels[-1], 100)
    sigmax_logfit_arr = sigmax_logfit[0] * np.log(vels) + sigmax_logfit[1]
    sigmax_linfit_arr = sigmax_linfit[0] * np.array(vels) + sigmax_linfit[1]
    axs2[2].plot(vels, sigmax_logfit_arr, label=f'logfit r2 {r2_score(sigmax_vels, sigmax_logfit_arr):.2f}', alpha = 0.6)
    axs2[2].plot(vels, sigmax_linfit_arr, label=f'linfit r2 {r2_score(sigmax_vels, sigmax_linfit_arr):.2f}', alpha = 0.6)
    axs2[2].legend()

    ms_logfit = np.polyfit(np.log(vels), ms_vels, 1)
    ms_linfit = np.polyfit(vels, ms_vels, 1)

    ms_logfit_arr = ms_logfit[0] * np.log(vels) + ms_logfit[1]
    ms_linfit_arr = ms_linfit[0] * np.array(vels) + ms_linfit[1] #apply linear fit to ms vels
    axs2[0].plot(vels, ms_logfit_arr, label=f'logfit r2 {r2_score(ms_vels, ms_logfit_arr):.2f}', alpha = 0.6)
    axs2[0].plot(vels, ms_linfit_arr, label = f'linfit r2 {r2_score(ms_vels, ms_linfit_arr):.2f}', alpha = 0.6)
    axs2[0].legend()
    fig.suptitle(f"Load curves for the chess system with increasing top plate velocity")
    fig.tight_layout(pad=1.8)
    
    outname = 'vary_vel.png'

    print(f'saved fig to {fig_dir + outname}')
    #fig.savefig(fig_dir + outname, dpi = 200)

    axs2[0].set_title('maximum static friction')
    axs2[1].set_title('slope of sigmoid fit')
    axs2[0].set_xlabel('top plate velocity [m/s]')
    axs2[1].set_xlabel('top plate velocity [m/s]')
    axs2[1].set_ylabel(r"$f$ [$\mu$Ns/m]")
    axs2[0].set_ylabel(r"$f$ [$\mu$N]")
    axs2[2].set_xlabel('top plate velocity [m/s]')
    axs2[2].set_ylabel(r"$f$ [$\mu$N]")
    axs2[2].set_title('highest sigmoid value')

    fig2.suptitle(f'slope and maximum static friction for varying velocity, chess layout')
    fig2.tight_layout()
    fig2.savefig(fig_dir + 'varying_vel_rise_maxstatic.png', dpi = 200)

if __name__ == '__main__':

    load_vs_normal_force()
