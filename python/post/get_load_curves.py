"""
Crystal Aging Project

Get load curves from push simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""
import re
from glob import glob
from post_utils import extract_load_curves


def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

def get_load_curves():
    asperities = 8
    uc = 5
    temp = 2300
    vel = 5
    time = '*'
    orientation = 110
    window = 10
    #initnum = 0
    force = 0
    #initseed = {0:(77222, 66232, 79443), 1:(29672, 40129), 2:(64364, 32077), 3:(33829, 84296), 
    #            4:(29082, 59000), 5:(16388, 65451), 6:(69759, 69759), 7:(65472, 62780)} #2 asp
    #initseed = {0: (47011, 82042, 22453), 1: (22453, 94902, 87980), 2: (21337, 87980), 3:(11962, 13930),
    #            4: (21979, 89876), 5: (43427, 48032)} # 8 asp
    initseed = {0: (88094, 43563, 94913), 1: (98414, 72415, 75761), 2: (86494, 67638, 60869), 3: (94091, 77768, 81554)}
    
    #for force in [0.0001, 0.001, 0.01, 0]:
    for initnum, seed in initseed.items():


        if isinstance(seed, tuple):
            for see in seed:
                logfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_or{orientation}_time{time}_initnum{initnum}_seed{see}_errgrid4_4/log.lammps'
                print(logfiles)
                if logfiles == []:
                    print(f'Warning, logfile not found; \n seed: {see}')
                for logfile in glob(logfiles):
                    print('--------------------------------------------------------------------------')
                    print('file: ', logfile)
                    matches = re.findall('\d+', logfile)
                    outfile_lc = f'../../txt/load_curves/production/load_curves_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{see}_errgrid4_4.txt'
                    outfile_ms = f'../../txt/max_static/production/max_static_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{see}_errgrid4_4.txt'
                    outfile_rise = f'../../txt/rise/production/rise_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{see}_errgrid4_4.txt'

                    extract_load_curves(logfile, None, 0, window = window, outfile_load_curves = outfile_lc, outfile_max_static = outfile_ms, outfile_rise = outfile_rise)
        else:
            logfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_or{orientation}_time{time}_initnum{initnum}_seed{seed}_errgrid4_4/log.lammps'
            if logfiles == []:
                print(f'Warning, logfile not found; \n seed: {seed}')
            print(logfiles)
            for logfile in glob(logfiles):
                print('--------------------------------------------------------------------------')
                print('file: ', logfile)
                matches = re.findall('\d+', logfile)
                outfile_lc = f'../../txt/load_curves/production/load_curves_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{seed}_errgrid4_4.txt'
                outfile_ms = f'../../txt/max_static/production/max_static_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{seed}_errgrid4_4.txt'
                outfile_rise = f'../../txt/rise/production/rise_temp{temp}_vel{vel}_force{force}_asp{asperities}_or{orientation}_initnum{initnum}_seed{seed}_errgrid4_4.txt'

                extract_load_curves(logfile, None, 0, window = window, outfile_load_curves = outfile_lc, outfile_max_static = outfile_ms, outfile_rise = outfile_rise)


def all_curves(production = True):
    asperities = 8
    uc = 5
    temp = 2300
    vel = 5
    time = 2000 
    orientation = 110
    window = 1500
    #initnum = 0
    force = 0

    if production:
        filetemplate = f'../../simulations/sys_asp{asperities}_uc{uc}/production/dataset/sim_temp{temp}_force{force}_asp{asperities}_or{orientation}_time*_initnum*_seed*_errgrid4_4/log.lammps'
    else:
        filetemplate = f'../../simulations/sys_asp{asperities}_uc{uc}/erratic/sim_temp{temp}_force{force}_asp{asperities}_or{orientation}_time{time}_seed*_errgrid4_4/log.lammps'

    print(filetemplate)
    files = glob(filetemplate)
    print(files)
    for _file in files:
        if production: 
            outfile_lc= '../../txt/load_curves/production/load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
            outfile_ms = '../../txt/max_static/production/max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
            outfile_rise = '../../txt/rise/production/rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
        else:
            outfile_lc= '../../txt/load_curves/erratic/load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
            outfile_ms = '../../txt/max_static/erratic/max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
            outfile_rise = '../../txt/rise/erratic/rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'



        matches = re.findall('\d+', _file)
        seed = matches[-3]
        initnum = matches[-4]
        print(seed, initnum)
        outfile_lc = outfile_lc.format(temp, vel, force, asperities, orientation, initnum, seed) 
        outfile_ms = outfile_ms.format(temp, vel, force, asperities, orientation, initnum,  seed) 
        outfile_rise = outfile_rise.format(temp, vel, force, asperities, orientation, initnum, seed) 

        extract_load_curves(_file, None, 0, window = window, outfile_load_curves = outfile_lc, outfile_max_static = outfile_ms, outfile_rise = outfile_rise)


if __name__ == '__main__':
    #get_load_curves()
    all_curves(production = True)
