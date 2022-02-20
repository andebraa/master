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
    height = 80
    vel = 1.25
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
    times = [300]

    #seeds = [12589, 50887]  
    #seeds = [88753,12754,91693] #thicc height 80
    #seeds = [50219, 31693, 19478]# thicc height 83
    # [31906, 35578, 69872, 94879] push seeds who used relax 37144
    #seeds = [81094, 81717, 10840, 89936, 25987, 82860] # thicc 85
    #seeds = [63620,46351,18735, 62648, 89682, 30607] # thicc 90
    #seeds = [17767,58195,19686, 81955,86485,61282] # thicc 95
    #seeds = [96804,43682,88372,64771,82158,63871,95317,18462,11729]#thicc 100
    #seeds = [11084,50879,83355] # thicc 93
    #seeds = [54648,88413,94253] #thicc 103
    #seeds = [92651,19224,85380] #thicc 105
    #seeds = [64798,34149] #thicc 109
    
    # second push run same as first run
    #seeds = [71361,91111,63445] # 80
    #seeds = [12890,62608,29899] # 83
    #seeds = [70529,45585,64900, 66909,27035,43111] # 85 
    #seeds = [81809,93141,56900, 33447,88504,79793] # 90
    #seeds = [75942,21663,49508] # 93
    #seeds = [67321,29830,36667, 77113,99307,62931] # 95
    #seeds = [47606,72506,44762, 47009,37801,56714, 54238,10257,73002] # 100
    #seeds = [71970,74062,60542] # 103
    #seeds = [81636,35286,69718] # 105
    #seeds = [90953,90762,47980] # 109

    #third push run NOTE too short
    #seeds = [76532,67473,86988]
    #seeds = [22135,54054,39337]
    #seeds = [15007,95692,61395, 31234,92172,49033]
    #seeds = [27448,57576,83094, 68672,65867,65400]
    #seeds = [57652,77804,75056]
    #seeds = [37474,72730,76985, 16010,24858,24113]
    #seeds = [19590,75450,95072, 63988,78860,45476, 35593,21768,33674]
    #seeds = [81910,46388,33465]
    #seeds = [23317,44679,86430]
    #seeds = [66411,52069,63812]
    
    #fourth push, 700 long
    #seeds = [97841,88985,79749] #80
    #seeds = [81474,90347,79290] #83
    #seeds = [40328,90215,62491,80371,12038,48116] # 85
    #seeds = [61347,50189,68738, 19022,23781,73474] #90
    #seeds = [27598,75257,74926] # 95
    #seeds = [17821,40450,80080] # 95
    #seeds = [14130,95349,16972] #93
    #seeds = [64180,63781,84634, 64308,93573,48127, 78231,43336,42599] # 100
    #seeds = [28782,23246,41573] # 103
    #seeds = [48834,99626,28475] # 105
    #seeds = [89090,40422,52257] #109

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

if __name__ == '__main__':
    get_load_curves()
