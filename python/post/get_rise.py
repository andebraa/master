import numpy as np
import matplotlib.pyplot as plt 
import glob

def get_rise():
    '''
    script finding the rise from a sigmoid function fitted to the load curve data
    '''
        # paths
    project_dir = '../../'
    fig_dir = project_dir + 'fig/'

    if production:
        load_curve_dir = project_dir + 'txt/load_curves/production/'
        max_static_dir = project_dir + 'txt/max_static/production/'
        rise_dir = project_dir + 'txt/rise/production/'

        template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid{}_{}.txt'
        template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid{}_{}.txt'
        template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_initnum{}_seed{}_errgrid4_4.txt'
        template_aux = project_dir + 'simulations/sys_asp{}_uc{}/production/sim_temp{}_force{}_asp{}_or{}_time{}_initnum{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'
    else:
        load_curve_dir = project_dir + 'txt/load_curves/erratic/'
        max_static_dir = project_dir + 'txt/max_static/erratic/'
        rise_dir = project_dir + 'txt/rise/erratic/'

        template_lc = load_curve_dir + 'load_curves_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
        template_ms = max_static_dir + 'max_static_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid{}_{}.txt'
        template_r = rise_dir + 'rise_temp{}_vel{}_force{}_asp{}_or{}_seed{}_errgrid4_4.txt'
        template_aux = project_dir + 'simulations/sys_asp{}_uc{}/erratic/sim_temp{}_force{}_asp{}_or{}_time{}_seed{}_errgrid4_4/system_asp{}_or{}_uc{}_initnum{}_errgrid4_4_auxiliary.json'

