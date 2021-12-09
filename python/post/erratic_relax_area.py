"""
File for analyzing stress of asperities under load. In progress

Largely based on Even's crystal aging project get_contact_area
"""
import json 
import numpy as np
import re
#from post_utils import get_erratic_contact_area #ovitos doesn't like this, copied erratic_contact area in here instead
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
        dumpfiles = glob(template_dump.format(orientation, height, temp, force, time, grid[0], grid[1]))
        for dumpfile in dumpfiles:
            
            
            for i in range(grid[0]):
                for j in range(grid[1]):
                    if bool_grid[i,j]: #is boo_grid is 1, we have an asperity
                        
                        pipeline = import_file(dumpfile, multiple_frames = True)

                        print('asperity at', j,i)
                        print('lx, ly:', lx, ly)
                        #seed = re.findall('\d+', dumpfile)[-1] #glod dumfiles is not implemented                     
                        seed = 10730
                        #data = pipeline.compute()
                        expression = f"Position.X >= {i*lx} && Position.X < {(i+1)*lx} && Position.Y >= {j*ly} && Position.Y < {(j+1)*ly}"
                        
                        #ovito lady code on pipeline istead
                        #pipeline.modifiers.append(ExpressionSelectionModifier(expression=expression))
                        #pipeline.compute()
                        
                        #ovito lady 
                        #data.apply(ExpressionSelectionModifier(expression = expression))
                        #data.apply(InvertSelectionModifier())
                        #data.apply(DeleteSelectedModifier())
                        
                        pipeline = alt_slicer_dicer(pipeline, i, j, lx, ly)
                        
                        export_file(pipeline, f'test_block{i}{j}.data', 'lammps/data', atom_style = 'atomic')
                        
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


def get_erratic_contact_area(pipeline, outfile="area.txt", delta=None,
                             init_time=0, asperity = 1, grid = (1,1)):
    """Get contact area and number of atoms in the
    contact region as a function of time. Utilizing
    Ovito. This script takes a cut out block containing an asperity
    from stress_analysis.py.
    writes a txt for each asperity, numbered from 0

    Parameters
    ----------
    pipeline : ovito object?
        pipeline that has cut out the single asperity
    outfile : str
        file to write the contact area to
    delta : float
        time difference between two frames in ns
        (assume constant delta)
    init_time : float
        initial time given in ns
    asperity : int
        the number of the asperity
    """

    print('start of get-conctact_area')
    if delta is None:
        warnings.warn(r"No $\Delta t$ is given, setting $\Delta t=1$")
        delta = 1

    # Slice:
    pipeline.modifiers.append(SliceModifier(
        distance = 55,
        normal = (0.0, 0.0, 1.0),
        slab_width = 2.0))

    # Cluster analysis:
    pipeline.modifiers.append(ClusterAnalysisModifier(sort_by_size=True))
    # Expression selection:
    pipeline.modifiers.append(ExpressionSelectionModifier(expression='Cluster!=1'))

    # Delete selected:
    pipeline.modifiers.append(DeleteSelectedModifier())

    # Construct surface mesh:
    pipeline.modifiers.append(ConstructSurfaceModifier(radius=20.0, identify_regions=True))

    # Output surface area as a function of time
    times, nums, areas = [], [], []
    for i in trange(pipeline.source.num_frames):
        data = pipeline.compute(frame=i)
        nums.append(data.attributes['ClusterAnalysis.largest_size'])
        # divid area by 2 to find area of one surface and by 100 to go from Å² to nm²
        areas.append(data.attributes['ConstructSurfaceMesh.surface_area'] / 200)

        time = i * delta + init_time
        times.append(time)
    del pipeline

    outfile_ = outfile +'_asperity'+str(asperity)+'.txt'

    header = ("Crystal Aging Project \n"
              "Author: Even Marius Nordhageni \n"
              "\n"
              "Contact area between asperity and lower surface and \n"
              "number of particles in the contact region.  \n"
              "\n"
              "time [ns]\t\t # contact atoms\t contact area [nm^2]\n"
              "number of this asperity: "+str(asperity))

    savetxt(outfile_, asarray([times, nums, areas], dtype=float).T, header=header)
    print('end of get contact area')
    return times, nums, areas



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
