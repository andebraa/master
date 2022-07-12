'''
Script that loops though all simulations in a given folder, calculates the rise of the curve and possibly max static,
output is an array shape (N, 4, 4) and (N,) where N is the number of simulatiions and the arrays contain the boolean matrix
and the output rise respectively.
'''
import json
import re
import numpy as np
from glob import glob

def dataset_maker():
    temp = 2300
    vel = 5
    force = 0
    uc = 5
    orientation = 110
    grid = (4,4)
    erratic = True
    asperities = 8
    initnum = 0
    timestep = 0.002
    time = 2000

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

    n = 47
    out_matrix = np.empty((n, 4,4)) #4,4 matrix, 1 rise, 1 max static
    out_y = np.empty((n, 2))
    for i in range(47): #this code now works with producition 
        print(i)
        lc_files = glob(template_lc.format(temp, vel, force, asperities,orientation, i, grid[0], grid[1]))
        matches = re.findall('\d+', lc_files[0])
        seed = matches[-3]

        rise_files = glob(template_r.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        ms_files = glob(template_ms.format(temp, vel, force, asperities, orientation,i, grid[0], grid[1]))
        load_curves = []
        rise = []
        ms = []
        #finding the shortest in case one is longer and it needs to be truncated
        shortest = (1000000000, 0) #length, index
        #for j, lc_file in enumerate(lc_files):
        #    infile = loadtxt(lc_file)
        #    if np.shape(infile)[0] < shortest[0]:
        #        shortest = (np.shape(infile)[0], j)
        #    load_curves.append(np.array(infile))
        #for j, load_curve in enumerate(load_curves):
        #    if j != shortest[1]:
        #        load_curves[j] = load_curves[j][:shortest[0]]
        #
        #    fit_sigmoid(load_curve, fig, axs[i])

        for rise_file in rise_files:
            rise.append(np.loadtxt(rise_file))
        for ms_file in ms_files:
            ms.append(np.loadtxt(ms_file))
        ##finding the auxiliary folder of the run to find the norm
        with open (glob(template_aux.format(asperities, uc, temp, force, asperities, orientation,
                               i, seed, asperities, orientation, uc, seed))[0]) as fp:
            #note that seeds contain runs of the same system, so all are similar to seeds[0]
            aux_dict = json.loads(fp.read())
        
        if len(rise) > 1:
            print('rise')
            print(rise)
            print('ms')
            print(np.shape(ms))
            print(ms)
            rise = np.mean(rise)
            ms = np.mean(ms)
        else:
            rise = rise[0]
            ms = ms[0]
        
    
        print(aux_dict['erratic'])
        out_matrix[i, :,:] = np.array(aux_dict['erratic'])
        print('-------rise---------ms---------')
        print(rise)
        print(ms)
        
        out_y[i,:] = np.array((rise, ms))

if __name__ == '__main__':
    dataset_maker()
        
