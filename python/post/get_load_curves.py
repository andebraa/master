"""
Crystal Aging Project

Get load curves from push simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from glob import glob
from post_utils import extract_load_curves

def get_load_curves():
    # user input
    temp = 2300
    orientation = "100"
    vel = 5
    force = 0
    
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    push_dir = project_dir + 'simulations/sys_or{}_uc{}/push/'
    if erratic:
        lc_dir = project_dir + 'txt/load_curves/erratic/'
        ms_dir = project_dir + 'txt/max_static/erratic/'
        push_dir += 'erratic/'
    elif grid:
        lc_dir = project_dir + 'txt/load_curves/grid/'
        ms_dir = project_dir + 'txt/max_static/grid/'
        push_dir += 'grid/'
    else:
        lc_dir = project_dir + 'txt/load_curves/'
        ms_dir = project_dir + 'txt/max_static/'

    
   
    if erratic:
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_errgrid{}_{}_chess/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}_chess.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}_chess.txt'
    elif grid:
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_grid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}_grid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}_grid{}_{}.txt'
    else: #note single aqsperity system might not be supported as of desember 2021
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}.txt'
    

    # collect log files
    #seed_dict = {1: [40525,37063,90058],
    #             2: [30643,69590,85108],
    #             3: [33852,81835,65387],
    #             4: [23383,57218,24832],
    #             5: [22125,97481,26403],
    #             6: [84340,13006,94745],
    #             7: [94340,52540,92005],
    #             8: [11394]}
    seed_dict = {3: [44066]}
    time = 700
    for height, seeds in seed_dict.items():
        logfiles = []
        for seed in seeds:
            print(f"seed: {seed}   time: {time}")
            logfile = template_logfiles.format(orientation, height, temp, vel, force, time, seed, grid[0], grid[1])
            print(logfile)
            logfiles.append(logfile)


            # extract load curves
            extract_load_curves(logfile, None, 0, 5000, 
                                outfile_load_curves = template_lc.format(temp, vel, force, 
                                                                         orientation, seed, 
                                                                         grid[0], grid[1]),

                                outfile_max_static = template_ms.format(temp, vel, force, 
                                                                        orientation, seed, 
                                                                        grid[0], grid[1]))
            print('load curves written to: \n', template_lc.format(temp, vel, force,
                                                                         orientation, seed,
                                                                         grid[0], grid[1]))

if __name__ == '__main__':
    get_load_curves()

    '''
    seed_dict = {1: [36015,37461,77220], 2: [49156,64486,73803],
                 3: [30642,74822,90272], 4: [20939,86781,87609],
                 5: [25642,46012,71581], 6: [86406,91501]}
    '''
    '''
    #seed_dict = {1: [40525,37063,90058],
    #             2: [30643,69590,85108],
    #             3: [33852,81835,65387],
    #             4: [23383,57218,24832],
    #             5: [22125,97481,26403],
    #             6: [84340,13006,94745]}
    '''
