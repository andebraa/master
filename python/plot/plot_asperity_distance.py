import re
import json
from glob import glob
from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from multiline import multiline
from matplotlib import style
from scipy.optimize import curve_fit
from plot_utils import sigmoid, rip_norm, fit_sigmoid
plt.style.use('seaborn')

def plot_max_static_dist():
    '''
    is there any correlation between asperity distance and max static?
    '''
        # user input
    temp = 2300
    vel = 5
    orientation = 110
    grid = (4,4)
    erratic = True
    asperities = 8
    initnum = 0
    time = 2000
    force = 0
    uc = 5

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
    template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/dataset/sim_temp{}_force{}_asp{}_or{}_time*_initnum{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'

    fig, axs = plt.subplots(2)
    axs = axs.ravel()

    for i in range(300): #this code now works with producition
        lc_files = glob(template_lc.format(temp, vel, force, asperities,orientation, i, grid[0], grid[1]))
        print(lc_files)
        lc_file = lc_files[0]

        matches = re.findall('\d+', lc_file)
        seed = matches[-3]

        rise_files = glob(template_r.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        ms_files = glob(template_ms.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        rise_file = rise_files[0]
        ms_file = ms_files[0]
        
        infile = loadtxt(lc_file)
        load_curve = np.array(infile)
        rise = loadtxt(rise_file)
        ms = np.array(loadtxt(ms_file))

        #fit_sigmoid(load_curve, fig, axs[i])
        ##finding the auxiliary folder of the run to find the norm
        with open (glob(template_aux.format(asperities, uc, temp, force, asperities, orientation,
                              i, seed, asperities, orientation, uc, seed))[0]) as fp:
            #note that seeds contain runs of the same system, so all are similar to seeds[0]
            aux_dict = json.loads(fp.read())


        matrix_norm = rip_norm(aux_dict['erratic'])
        print('twat')
        print(rise)
        print(ms)
        axs[0].plot(matrix_norm, rise, 'o', c='b')
        axs[1].plot(matrix_norm, ms[1], 'o', c = 'b')



    axs[0].set_xlabel('norm of asperity distance')
    axs[0].set_ylabel('rise of simoid fit')
    axs[1].set_xlabel('norm of asperity distance')
    axs[1].set_ylabel('max static')
    fig.tight_layout(pad=0.8, h_pad = 1.0)
    
    fig.suptitle(f"the rise and max static as a function of the norm of asperity distances, \n temp {temp}, force {force}, vel {vel}, asperities {asperities}, orientation {orientation}")
    fig.savefig(fig_dir + 'png/asperity_distance_v_maxstatic.png')

if __name__ == '__main__':
    plot_max_static_dist()
