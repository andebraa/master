"""
File for analyzing stress of asperities under load. In progress

Largely based on Even's crystal aging project get_contact_area
"""
import json 
import numpy as np
import re
from post_utils import get_erratic_contact_area
from ovito.io import import_file, export_file
from ovito.modifiers import *
from ovito.pipeline import *
from glob import glob
from numpy import savetxt, asarray
from tqdm import trange
from scipy.signal import find_peaks
from scipy.constants import value
from lammps_logfile import File, running_mean
import warnings
import json


def erratic_relax_area():
    """
    
    grid (touple): number of asperities in grid. default is one asperity (1,1)
    

    """
    orientation = 100 
    height = 115 # Å 
    force = 0.001 #eV/Å
    grid = (3,3)
    time = 1000 #ps
    delta = time/1e6    

    # paths
    project_dir = '../../'
    relax_dir = project_dir + 'simulations/sys_or{}_hi{}/relax/'
    area_relax_dir = project_dir + 'txt/area_relax/'
    coordination_dir = project_dir + 'txt/coordination/'


    template_dump = relax_dir + 'sim_temp{}_force{}_time{}_seed*_errgrid{}_{}/dump.bin'
    auxiliary_dir = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_errgrid{}_{}_auxiliary.json'
    template_area = area_relax_dir + 'areas_temp{}_force{}_55_hi{}_seed{}_erratic{}_{}'#add the txt in count_coord
    template_coord = coordination_dir + 'coordination_temp{}_force{}_hi{}_seed{}_erratic{}_{}'


    with open(auxiliary_dir.format(orientation, height, grid[0], grid[1])) as auxfile:
        data = auxfile.read() 
    args = json.loads(data) 

    lx, ly = args['lx'], args['ly'] #size of one grid
    if delta is None:
        warnings.warn(r"No $\Delta t$ is given, setting $\Delta t=1$")
        delta = 1

    bool_grid = np.array(args['erratic']) 

    asperity = 0
    temps = [2300]
    for temp in temps:
        dumpfiles = glob(template_dump.format(orientation, height, temp, force, time, grid[0], grid[1]))
        auxiliary_files = glob(auxiliary_dir.format(orientation, height, grid[0], grid[1]))
        for dumpfile in dumpfiles:
            
            pipeline = import_file(dumpfile, multiple_frames = True)

            for i in range(grid[0]):
                for j in range(grid[1]):
                    if bool_grid[i,j]: #is boo_grid is 1, we have an asperity
                        print('asperity at', i,j)
                        print('lx, ly:', lx, ly)
                        seed = re.findall('\d+', dumpfile)[-1]                       
                        print(seed)

                        # first outward slice X direction
                        pipeline.modifiers.append(SliceModifier(
                        distance = (i+1)*lx,
                        normal = (1.0, 0.0, 0.0)))
                        print('i+1 *lx=', (i+1)*lx)

                        # first inward slice X direction
                        pipeline.modifiers.append(SliceModifier(
                        distance = (i)*lx,
                        normal = (1.0, 0.0, 0.0),
                        inverse = True))
                        print('i *lx=', (i)*lx)

                        # first outward slice Y direction
                        pipeline.modifiers.append(SliceModifier(
                        distance = (j+1)*ly,
                        normal = (0.0, 1.0, 0.0)))
                        print('j+1 *ly=', (j+1)*ly)

                        # first outward slice Y direction
                        pipeline.modifiers.append(SliceModifier(
                        distance = (j)*ly,
                        normal = (0.0, 1.0, 0.0), 
                        inverse = True))
                        print('j *ly=', (j)*ly)

                        #cutting out slab etc is handled in post_utils
                        get_erratic_contact_area(pipeline, 
                                                 template_area.format(temp, force, height, seed, grid[0], grid[1]), 
                                                 delta=time/1e6, asperity = asperity, grid = grid)
                        #count_coord_erratic(pipeline, 
                        #                     template_coord.format(temp, force, height, seed))
                        asperity += 1
                        del pipeline.modifiers
                        #pipeline.clear()

if __name__ == '__main__':
    erratic_relax_area()
