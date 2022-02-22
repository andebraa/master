"""
based on get_load_curves. Assumes structure of sim{...}/rerun_time{}/logfile
where the rerun in located within the respective folders. 
reads both, appends rerun to end of file
"""
import os 
from glob import glob
from post_utils import extract_load_curves

def get_load_curves():
    # user input
    temp = 2300
    orientation = "100"
    vel = 1.25
    force = 0.001
    
    grid = (4,4)
    erratic = True


    # collect log files
    orig_time = 700
    rerun_time = 300
    
    # paths
    project_dir = '../../'
    push_dir = project_dir + 'simulations/sys_or{}_hi{}/push/'
    if erratic:
        lc_dir = project_dir + 'txt/load_curves/erratic/'
        ms_dir = project_dir + 'txt/max_static/erratic/'
        push_dir += 'erratic/'

    
    if erratic:
        rerun_template = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_errgrid{}_{}/restart_time{}/log.lammps'
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_seed{}_errgrid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_or{}_seed{}_errgrid{}_{}.txt'

    
    #fourth push, 700 long
    seeds = [97841,88985,79749] #80
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

    heights = [80]#,83,85,90,93,95,100,103,105,109] 

    for height in heights:
        for seed in seeds:
            print(f"seed: {seed}")
            orig_logfile = template_logfiles.format(orientation, height, temp, 
                                                    vel, force, orig_time, seed, 
                                                    grid[0], grid[1])

            rerun_logfile = rerun_template.format(orientation, height, temp, vel, 
                                                  force, orig_time, seed, grid[0], 
                                                  grid[1], rerun_time)

            print('orig_logfile', orig_logfile)
            print('rerun_logfile', rerun_logfile)
            # extract load curves
            extract_load_curves(orig_logfile, None, 0, 5000, 
                                outfile_load_curves = template_lc.format(temp, vel, force, 
                                                                         orientation, seed, 
                                                                         grid[0], grid[1]),

                                outfile_max_static = template_ms.format(temp, vel, force, 
                                                                        orientation, seed, 
                                                                        grid[0], grid[1]), 
                                rerun = rerun_logfile)
            print('load curves written to: \n', template_lc.format(temp, vel, force,
                                                                         orientation, seed,
                                                                     grid[0], grid[1]))
            
if __name__ == '__main__':
    get_load_curves()
