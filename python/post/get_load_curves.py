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
    height = 90
    vel = 5
    force = 0.001
    
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
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
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_errgrid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}.txt'
    elif grid:
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_grid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}_grid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}_grid{}_{}.txt'
    else: #note single aqsperity system might not be supported as of desember 2021
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}.txt'
    

    # collect log files
    times = [1000]
    seeds = [53538]

    for seed in seeds:
        logfiles = []
        for time in times:
            print(f"seed: {seed}   time: {time}")
            logfile = template_logfiles.format(orientation, height, temp, vel, force, time, seed, grid[0], grid[1])
            print(logfile)
            logfiles.append(logfile)


        # extract load curves
        extract_load_curves(logfiles, None, 0, 5000, 
                            outfile_load_curves = template_lc.format(temp, vel, force, 
                                                                     orientation, seed, 
                                                                     grid[0], grid[1]),

                            outfile_max_static = template_ms.format(temp, vel, force, 
                                                                    orientation, seed, 
                                                                    grid[0], grid[1]))
        print('load curves written to: \n', template_lc.format(temp, vel, force,
                                                                     orientation, seed,
                                                                     grid[0], grid[1]))

def get_erratic_load():
    """
    Might not be interesting to look at load curves per asperity
    """
    temp = 2300
    orientation = "100"
    height = 200
    vel = 5
    force = 0.001

    grid = (3,3)

    # paths
    project_dir = '../../'
    push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
    lc_dir = project_dir + 'txt/load_curves/'
    ms_dir = project_dir + 'txt/max_static/'

    template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}/log.lammps'
    template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}.txt'
    template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}.txt'

    auxiliary_dir = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_errgrid{}_{}_auxiliary.json'


    with open(auxiliary_dir.format(orientation, height, grid[0], grid[1])) as auxfile:
        data = auxfile.read()
    args = json.loads(data)



    # collect log files
    times = range(125000, 2500001, 125000) 
    seeds = [17361, 29464, 55979, 57200, 90536]
    
    asperity = 0
    for i in range(grid[0]):
        for j in range(grid[1]):
            if args['grid'][i][j]:

        
                extract_load_curves(logfiles, None, 0, 5000, 
                    template_lc.format(temp, vel, force, orientation, seed),
                    template_ms.format(temp, vel, force, orientation, seed),
                    asperity)

                asperity += 1
    #for seed in seeds:
    #    logfiles = []
    #    for time in times:
    #        print(f"seed: {seed}   time: {time}")
    #        logfile = template_logfiles.format(orientation, height, temp, vel, force, time, seed)
    #        logfiles.append(logfile)
#
#
#        # extract load curves
#        extract_load_curves(logfiles, None, 0, 5000, 
#                            template_lc.format(temp, vel, force, orientation, seed),
#                            template_ms.format(temp, vel, force, orientation, seed))
if __name__ == '__main__':
    get_load_curves()
