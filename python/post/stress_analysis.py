"""
File for analyzing stress of asperities under load. In progress

Largely based on Even's crystal aging project get_contact_area
"""
import json 
import numpy as np

from ovito.io import import_file, export_file
from ovito.modifiers import *
from ovito.pipeline import *

from numpy import savetxt, asarray
from tqdm import trange
from scipy.signal import find_peaks
from scipy.constants import value
from lammps_logfile import File, running_mean
import warnings


def anal_stress(dumpfile, outfile="area.txt", delta=None,
                     init_time=0i, grid = (1,1))):
    """
    
    grid (touple): number of asperities in grid. default is one asperity (1,1)
    """
    orientation = '115' 
    height = 200 # Å 
    force = 0.001 #eV/Å
    


    # paths
    project_dir = '../../'
    relax_dir = project_dir + 'simulations/sys_or{}_hi{}/relax/'
    area_relax_dir = project_dir + 'txt/area_relax/'
    coordination_dir = project_dir + 'txt/coordination/'


    template_dump = relax_dir + 'sim_temp{}_force{}_time{}_seed*/dump.bin'
    auxiliary_dir = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_errgrid{}_{}_auxiliary.json'
    template_area = area_relax_dir + 'areas_temp{}_force{}_55_hi{}_seed{}.txt'
    template_coord = coordination_dir + 'coordination_temp{}_force{}_hi{}_seed{}.txt'


    with open(auxiliary_dir.format(orientation, height, grid[0], grid[1])) as auxfile:
        data = auxfile.read() 
    args = json.loads(data) 

    if delta is None:
        warnings.warn(r"No $\Delta t$ is given, setting $\Delta t=1$")
        delta = 1

    bool_grid = np.array(args['erratic']) 

    pipeline = import_file(dumpfile, multiple_frames = True)
    
    #slice through each asperity, fairly high up to avvoid bending and other factors 
    for i in range(grid[0]):
        for j in range(grid[1]):
            if bool_grid[i,j]: #is boo_grid is 1, we have an asperity
                pipeline.append(SliceModifier(
                    distance = 60, #this is the height of the slice, should be high up, MODIFY
                    normal = (0.0, 1.0, 0.0),
                    slab_width = 0.0) #unsure about this too.
                                      #If zero, the modifier cuts away everything on one side of the cutting plane.

