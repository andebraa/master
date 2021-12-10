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
    relax_dir = project_dir + 'simulations/sys_or{}_hi{}/relax/erratic/'
    area_relax_dir = project_dir + 'txt/area_relax/'
    coordination_dir = project_dir + 'txt/coordination/'


    template_dump = relax_dir + 'sim_temp{}_force{}_time{}_seed*_errgrid{}_{}/dump.bin'
    auxiliary_dir = project_dir + 'initial_system/erratic/aux/system_or{}_hi{}_errgrid{}_{}_auxiliary.json'
    template_area = area_relax_dir + 'erratic/areas_temp{}_force{}_55_hi{}_seed{}_erratic{}_{}'#add the txt in count_coord
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
        print(template_dump.format(orientation, height, temp, force, time, grid[0], grid[1]))
        dumpfiles = glob(template_dump.format(orientation, height, temp, force, time, grid[0], grid[1]))
        print(dumpfiles)
        for dumpfile in dumpfiles:
            
            
            for i in range(grid[0]):
                for j in range(grid[1]):
                    if bool_grid[i,j]: #is boo_grid is 1, we have an asperity
                        
                        pipeline = import_file(dumpfile, multiple_frames = True)

                        print('asperity at', j,i)
                        print('lx, ly:', lx, ly)
                        #seed = re.findall('\d+', dumpfile)[-1] #glod dumfiles is not implemented                     
                        seed = 10730
                        expression = f"Position.X >= {i*lx} && Position.X < {(i+1)*lx} && Position.Y >= {j*ly} && Position.Y < {(j+1)*ly}"
                        
                        
                        pipeline = alt_slicer_dicer(pipeline, i, j, lx, ly)
                        
                        #export_file(pipeline, f'test_block{i}{j}.data', 'lammps/data', atom_style = 'atomic')
                        
                        get_erratic_contact_area(pipeline, 
                                                 template_area.format(temp, 
                                                                      force, 
                                                                      height, 
                                                                      seed, 
                                                                      grid[0], 
                                                                      grid[1]), 
                                                 delta=time/1e6, asperity = asperity, grid = grid)
                        asperity += 1

                        #del(data)



def alt_slicer_dicer(pipeline, i, j, lx, ly):
    """
    Instead of four slices, two inverse, i slice twice with a slice in x and y direction
    with lx and ly thickness. Original idea from even
    Note, slice extends from the middle
    """
    # X direction slice
    pipeline.modifiers.append(SliceModifier(
    distance = (i)*lx+ lx/2,
    normal = (1.0, 0.0, 0.0),
    slab_width = lx))
    print('X direction slice ',i*lx,' to ',i*lx + lx)
    
    
    # Y direction slice
    pipeline.modifiers.append(SliceModifier(
    distance = (j)*ly+ ly/2,
    normal = (0.0, 1.0, 0.0),
    slab_width = ly))
    print('Y direction slice ',j*ly,' to ',j*ly + ly)

    return pipeline


def slicer_dicer(pipeline, i, j, lx, ly):
    """
    my original attempt at slicing away asperity. Even uses a slice with width > 0, maybe 
    this is an option.
    This code currently does not work. 
    """
    # first outward slice X direction
    pipeline.modifiers.append(SliceModifier(
    distance = (i+1)*lx,
    normal = (1.0, 0.0, 0.0)))
    print('first, 1,0,0')
    print('i+1 *lx=', (i+1)*lx)
    
    #pipeline.add_to_scene()
    # first inward slice X direction
    pipeline.modifiers.append(SliceModifier(
    distance = (i)*lx,
    normal = (1.0, 0.0, 0.0),
    inverse = True))
    print('second, inverse, 1,0,0')
    print('i *lx=', (i)*lx)

    # first outward slice Y direction
    pipeline.modifiers.append(SliceModifier(
    distance = (j+1)*ly,
    normal = (0.0, 1.0, 0.0)))
    print('third, 0,1,0')
    print('j+1 *ly=', (j+1)*ly)

    # first outward slice Y direction
    pipeline.modifiers.append(SliceModifier(
    distance = (j)*ly,
    normal = (0.0, 1.0, 0.0),
    inverse = True))
    print('fourth, inverse, 0,1,0')
    print('j *ly=', (j)*ly)

    return pipeline

if __name__ == '__main__':
    erratic_relax_area()
