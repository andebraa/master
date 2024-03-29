"""
Crystal Aging Project

Get load curves from push simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""
import re
from glob import glob
from post_utils import extract_displacement

def get_load_curves(asperities = 8, uc = 5):
    # user input
    temp = 2300
    orientation = "100"
    vel = 5
    force = 0.001
    
    grid = (4,4)
    erratic = True


    # paths
    project_dir = '../../'
    push_dir = project_dir + f'simulations/sys_asp{asperities}_uc{uc}/production/'
    if erratic:
        lc_dir = project_dir + 'txt/load_curves/production/'
        ms_dir = project_dir + 'txt/max_static/production/'
    elif grid:
        lc_dir = project_dir + 'txt/load_curves/production/'
        ms_dir = project_dir + 'txt/max_static/production/'
    else:
        lc_dir = project_dir + 'txt/load_curves/'
        ms_dir = project_dir + 'txt/max_static/'

    
   
    if erratic:
        template_logfiles = push_dir + 'sim_temp{}_force{}_asp{}_time{}_initnum{}_errgrid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}_errgrid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}_errgrid{}_{}.txt'
    elif grid:
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_initnum{}_grid{}_{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}_grid{}_{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}_grid{}_{}.txt'
    else: #note single aqsperity system might not be supported as of desember 2021
        template_logfiles = push_dir + 'sim_temp{}_vel{}_force{}_time{}_initnum{}/log.lammps'
        template_lc = lc_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_initnum{}.txt'
        template_ms = ms_dir + 'max_static_temp{}_vel{}_force{}_asp{}_initnum{}.txt'
    

    time = 1000
    for initnum in range(20):
        print(f"initnum: {initnum} time: {time}")
        logfile = template_logfiles.format(temp, force, asperities,time, initnum, grid[0], grid[1])
        print(logfile)


        # extract load curves
        extract_load_curves(logfile, None, 0, 5000, 
                            outfile_load_curves = template_lc.format(temp, vel, force, 
                                                                     asperities, initnum,
                                                                     grid[0], grid[1]),

                            outfile_max_static = template_ms.format(temp, vel, force, 
                                                                    asperities, initnum,
                                                                    grid[0], grid[1]))
        print('load curves written to: \n', template_lc.format(temp, vel, force,
                                                                     asperities, initnum,
                                                                     grid[0], grid[1]))

if __name__ == '__main__':

    asperities = 8
    uc = 5
    temp = 2300
    vel = 5
    time = 1800
    init_time = 0
    initnum = 0
    #force = 0.001
    for force in [0.0001, 0.001, 0.01, 0]:
    #for initnum in range(0, 4):
        print(initnum)
        logfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*_errgrid4_4/log.lammps'
        for logfile in glob(logfiles):
            print('file: ', logfile)
            matches = re.findall('\d+', logfile)
            seed = matches[-3]
            outfile_disp = f'../../txt/displacement/production/displacement_temp{temp}_vel{vel}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}_errgrid4_4.txt'
            print(outfile_disp)
            extract_displacement(logfile, outfile = outfile_disp)
