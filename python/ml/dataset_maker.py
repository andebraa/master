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

    # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'
    highz_dir = '../../txt/high_z/'

    load_curve_dir = project_dir + 'txt/load_curves/production/'
    max_static_dir = project_dir + 'txt/max_static/production/'
    rise_dir = project_dir + 'txt/rise/production/'


    template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum*_seed*_errgrid{}_{}.txt'
    template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed*_errgrid{}_{}.txt'
    template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed*_errgrid4_4.txt'
    template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/dataset/sim_temp{}_force{}_asp{}_or{}_time*_initnum{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'

    lc_files = glob(template_lc.format(temp, vel, force, asperities,orientation, grid[0], grid[1]))
    n = len(lc_files)
    print('len lc files: ', n)
    out_matrix = np.zeros((n, 4,4)) #4,4 matrix, 1 rise, 1 max static
    out_y = np.zeros((n, 2))
    for i, lc_file in enumerate(lc_files): #this code now works with producition
        try:
            matches = re.findall('\d+', lc_file)
        except:
            print(i)
            print('failed to run')
            continue #not all files are completed. if this is the case, continue onto next one
        seed = matches[-3]
        initnum = matches[-4]

        rise_files = glob(template_r.format(temp, vel, force, asperities, orientation,initnum, grid[0], grid[1]))
        ms_files = glob(template_ms.format(temp, vel, force, asperities, orientation,initnum, grid[0], grid[1]))
        load_curves = []
        rise = []
        ms = []

        for rise_file in rise_files:
            rise.append(np.loadtxt(rise_file))
        for ms_file in ms_files:
            ms.append(np.loadtxt(ms_file)[1])
        ##finding the auxiliary folder of the run to find the norm
        with open (glob(template_aux.format(asperities, uc, temp, force, asperities, orientation,
                               initnum, seed, asperities, orientation, uc, seed))[0]) as fp:
            #note that seeds contain runs of the same system, so all are similar to seeds[0]
            aux_dict = json.loads(fp.read())
        
        if len(rise) > 1:
            rise = np.mean(rise)
            ms = np.mean(ms, axis = 0)
        else:
            rise = rise[0]
            ms = ms[0]
        
    
        out_matrix[i, :,:] = np.array(aux_dict['erratic'])
        out_y[i,:]= np.array((rise,ms))
    print(out_y)
    print(out_matrix)
    print('number of datasets: ', len(out_y))
    np.save( 'temp_out_y.npy', out_y)
    np.save('temp_out_matrix.npy', out_matrix)


def random_dataset():
    '''
    Script that makes a random datset of matrices and values for rise and ms. 
    If we attempt to apply machine learning to this, will we se the same results as 
    for the simulated dataset? 
    '''

    real_matrix = np.load('../pre/config_list.npy')
    real_y = np.load('temp_out_y.npy')
    print(np.shape(real_y))
    print(real_y)
    avg_ms, avg_rise = np.mean(real_y, axis=0)
    std_ms, std_rise = np.std(real_y, axis=0)#overflow here
    print(std_ms, std_rise)
    
    N = 200 #number of fake samples
    matrices = np.load('../pre/config_list.npy')
    out_matrix = np.empty((N, 4,4))
    out_y = np.empty((N,2))
    
    for i in range(N):
        out_matrix[i, :,:] = matrices[np.random.randint(0, len(matrices))] #select random matrix setup
        rand_ms = np.random.normal(avg_ms, std_ms)
        rand_rise = np.random.normal(avg_rise, std_rise)

        out_y[i, :] = np.array((rand_ms, rand_rise))

        
    np.save('random_matrix.npy', out_matrix)
    np.save('rand_out_y.npy', out_y)



if __name__ == '__main__':
    dataset_maker()
    random_dataset()
        
