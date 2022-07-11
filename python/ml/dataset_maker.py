'''
Script that loops though all simulations in a given folder, calculates the rise of the curve and possibly max static,
output is an array shape (N, 4, 4) and (N,) where N is the number of simulatiions and the arrays contain the boolean matrix
and the output rise respectively.
'''

import numpy as np

def dataset_maker():
    temp = 2300
    vel = 5
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
    template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/sim_temp{}_force{}_asp{}_or{}_time*_initnum{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'

    fig, axs = plt.subplots(5,2, figsize = (20,20))
    axs = axs.ravel()

    fig2, axs2 = plt.subplots()

    c = plt.cm.viridis((9 - np.arange(10))/(9 - 0 + 0.01))

    for i in range(10): #this code now works with producition 
        lc_files = glob(template_lc.format(temp, vel, force, asperities,orientation, i, grid[0], grid[1]))
        print(lc_files)

        matches = re.findall('\d+', lc_files[0])
        seed = matches[-3]

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

            fit_sigmoid(load_curve, fig, axs[i])

        for rise_file in rise_files:
            rise.append(loadtxt(rise_file))
        for ms_file in ms_files:
            print(ms_file)
            ms.append(ms_file)
        ##finding the auxiliary folder of the run to find the norm
        with open (glob(template_aux.format(asperities, uc, temp, force, asperities, orientation,
                              i, seed, asperities, orientation, uc, seed))[0]) as fp:
            #note that seeds contain runs of the same system, so all are similar to seeds[0]
            aux_dict = json.loads(fp.read())


        matrix_norm = rip_norm(aux_dict['erratic'])

        
