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
    vel = 5
    orientation = 110
    grid = (4,4)
    erratic = True
    asperities = 8
    _force = 0

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
    fig2, axs2 = plt.subplots(3, figsize = (12, 8))
    fig3, axs3 = plt.subplots() #fake fig for sigmax
    axs2 = axs2.ravel()
    axs = axs.ravel()
    vary_norm = {0:(43898,74145,26926), 0.0001: (89567,11678,27618), 0.001:(43698,76180,77635), 0.01:(83673,80288,70338)}
    vary_norm_alt = {0:(43898,74145,26926), 0.0001: (89567,11678,27618), 0.001:(43698,76180,77635), 
                     0.004:(99773, 42367, 15120), 0.006:(59398, 92835, 67767), 0.01:(83673,80288,70338)}


    c = plt.cm.viridis((3 - np.arange(len(vary_norm_alt)))/(3 - 0 + 0.01))
    
    ms_force = []
    sigmax_force = []
    forces = []
    for i, (force, seed) in enumerate(vary_norm_alt.items()):

        load_curves_all, load_curves_mean = load_load_curves(temp, vel, force, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)


        max_static_all, max_static_mean = load_max_static(temp, vel, force, asperities, orientation,
                                                        grid, template_lc, template_ms, 0, seed, False)

        rise_all, rise_mean = load_rise(temp, vel, force, asperities, orientation,
                                                        grid, template_r, 0, seed, False)


        _sigmax_force= []
        for j,curve in enumerate(load_curves_all):
        #    axs[i].plot(curve[:,0], curve[:,1], alpha = 0.4, c=c[j])
            axs2[2].plot(force, fit_sigmoid(curve, fig3, axs3), 'o', c=c[j])
            sigmax_force.append(fit_sigmoid(curve, fig3, axs3))
            forces.append(force)
        for j, max_static in enumerate(max_static_all):
        #    axs[i].plot(max_static[0], max_static[1], 'bo')
            axs2[0].plot(force, max_static[1], 'o', c=c[j])
            ms_force.append(max_static[1])
        #axs2[0].plot(normforce, max_static_mean[1], '*', label='mean')
        for j,rise in enumerate(rise_all):
            axs2[1].plot(force, rise, 'o', c = c[j])
        #axs2[1].plot(normforce, rise_mean, '*', label='mean')
        axs2[0].legend()

    
        #axs[i].plot(load_curves_mean[0,:,0], load_curves_mean[0,:,1], label = f'average')
        #axs[i].legend()
        #axs[i].set_xlabel(r"$t_p$ [ns]")
        #axs[i].set_ylabel(r"$f$ [$\mu$N]")
        #axs[i].set_title(f'velocity {vel} [m/s]')
        #axs[i].set_ylim([-0.02, 0.14])

    sigmax_linfit = np.polyfit(forces, sigmax_force, 1)
    polfit_plot_force = np.linspace(forces[0], forces[-1], 100)
    sigmax_linfit_arr = sigmax_linfit[0] * np.array(forces) + sigmax_linfit[1]
    axs2[2].plot(forces, sigmax_linfit_arr, label=f'linfit r2 {r2_score(sigmax_force, sigmax_linfit_arr):.2f}', alpha = 0.6)
    axs2[2].legend()

    ms_linfit = np.polyfit(forces, ms_force, 1)

    ms_linfit_arr = ms_linfit[0] * np.array(forces) + ms_linfit[1] #apply linear fit to ms vels
    axs2[0].plot(forces, ms_linfit_arr, label = f'linfit r2 {r2_score(ms_force, ms_linfit_arr):.2f}', alpha = 0.6)
    axs2[0].legend()
    fig.suptitle(f"Load curves for the chess system with various top plate normal force")
    fig.tight_layout(pad=1.8)
    
    outname = 'vary_force.png'

    print(f'saved fig to {fig_dir + outname}')
    #fig.savefig(fig_dir + outname, dpi = 200)

    axs2[0].set_title('maximum static friction')
    axs2[1].set_title('slope of sigmoid fit')
    axs2[0].set_xlabel('normal force [$\mu$N]')
    axs2[1].set_xlabel('normal force [$\mu$N]')
    axs2[2].set_xlabel('normal force [$\mu$N]')
    axs2[1].set_ylabel(r"$f$ [$\mu$Ns/m]")
    axs2[0].set_ylabel(r"$f$ [$\mu$N]")
    axs2[2].set_ylabel(r"$f$ [$\mu$N]")
    axs2[2].set_title('highest sigmoid value')

    fig2.suptitle(f'maximum static friction, slope of the simoid value and the highest sigmoid value, chess layout')
    fig2.tight_layout()
    fig2.savefig(fig_dir + 'varying_force_rise_normforce.png', dpi = 200)

if __name__ == '__main__':

    load_vs_normal_force()
