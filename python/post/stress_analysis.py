"""
File for analyzing stress of asperities under load. In progress

Largely based on Even's crystal aging project get_contact_area
"""

from ovito.io import import_file, export_file
from ovito.modifiers import *

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
    
    if delta is None:
        warnings.warn(r"No $\Delta t$ is given, setting $\Delta t=1$")
        delta = 1

    pipeline = import_file(dumpfile, multiple_frames = True)
    
    #slice through each asperity, fairly high up to avvoid bending and other factors 
    for i in range(grid[0]):
        for j in range(grid[1]):
            pipeline.append(SliceModifier(
                distance = 60, #this is the height of the slice, should be high up, MODIFY
                normal = (0.0, 1.0, 0.0),
                slab_width = 0.0) #unsure about this too.
                                  #If zero, the modifier cuts away everything on one side of the cutting plane.

