"""
Crystal Aging Project

Postprocess dumpfiles and logfiles

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from ovito.io import import_file, export_file
from ovito.modifiers import *

from numpy import savetxt, asarray
from tqdm import trange
from scipy.signal import find_peaks
from scipy.constants import value
from lammps_logfile import File, running_mean
from scipy.optimize import curve_fit
import warnings
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

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
              "Author: Even Marius Nordhageni & Anders Bråte \n"
              "\n"
              "Contact area between asperity and lower surface and \n"
              "number of particles in the contact region.  \n"
              "\n"
              "time [ns]\t\t # contact atoms\t contact area [nm^2]\n"
              "number of this asperity: "+str(asperity))

    savetxt(outfile_, asarray([times, nums, areas], dtype=float).T, header=header)
    print('end of get contact area')
    return times, nums, areas



def get_contact_area(dumpfile, outfile="area.txt", delta=None,
                     init_time=0):
    """Get contact area and number of atoms in the 
    contact region as a function of time. Utilizing
    Ovito.

    Parameters
    ----------
    dumpfile : str
        dumpfile to be analysed to obtain contact area
    outfile : str
        file to write the contact area to
    delta : float
        time difference between two frames in ns
        (assume constant delta)
    init_time : float
        initial time given in ns
    """
    print('start of get-conctact_area')
    if delta is None:
        warnings.warn(r"No $\Delta t$ is given, setting $\Delta t=1$")
        delta = 1

    # Data import:
    pipeline = import_file(dumpfile, multiple_frames=True)
    
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

    header = ("Crystal Aging Project \n"
              "Author: Even Marius Nordhagen \n"
              "Github repo: github.com/evenmn/crystal-aging \n"
              "\n"
              "Contact area between asperity and lower surface and \n"
              "number of particles in the contact region.  \n"
              "\n"
              "time [ns]\t\t # contact atoms\t contact area [nm^2]")

    savetxt(outfile, asarray([times, nums, areas], dtype=float).T, header=header)
    print('end of get contact area')
    return times, nums, areas


def count_coord(dumpfile, outfile="coord.txt"):
    """Count number of particles with different coordination numbers.
    Utilizing Ovito.
    
    Parameters
    ----------
    dumpfile : str
        dumpfile to be analysed to obtain contact area
    outfile : str
        file to write the contact area to
    """

    # Data import:
    pipeline = import_file(dumpfile, multiple_frames=True)

    # Coordination analysis:
    pipeline.modifiers.append(CoordinationAnalysisModifier(cutoff=2.39))

    # Color coding:
    pipeline.modifiers.append(ColorCodingModifier(
        property='Coordination', 
        start_value=1.0, 
        end_value=4.0))

    # Histogram:
    pipeline.modifiers.append(HistogramModifier(
        operate_on='particles:particles', 
        property='Coordination', 
        bin_count=20))
 
    # Output number of adatoms, kinks, surface and bulk atoms as a function of time
    export_file(pipeline, outfile, "txt/table", key="histogram[Coordination]", multiple_frames=True)
    del pipeline


def extract_load_curves(logfile, delta=None, init_time=0, window=1,
                        outfile_load_curves="load_curves.txt",
                        outfile_max_static="max_static.txt",
                        outfile_rise = 'rise.txt',
                        prominence=0.0001, asperity = False, rerun = False):
    """Extract load curves (-v_fx) from log file and
    save the load curves as text files. Also, find the maximum
    static friction across the log files and save them in one 
    file.

    IF asperity, then the system is either a grid or erratic,
    outputfile wil be numbered accordingly

    Parameters
    ----------
    logfiles : list of str
        list of LAMMPS log files
    delta : float
        time difference between two frames in ns
    init_time : float
        time of initial logfile given in ns
    window : int
        window size for running mean
    outfile_load_curves : str
        where to save the load curves
    outfiles_max_static : str
        where to save the maximum static friction force
    asperity: int or False
        is the logfile part of an asperity? if so gives
        the output a numbered name
    """
    print(outfile_load_curves)
    print(outfile_max_static)
    print('------------------------------------')
    if delta is None:
        warnings.warn("Time different between log files is not given, setting Dt=1")
        delta = 1

    # headers of text files
    header_load_curves = (
          "# Crystal Aging Project \n"
          "# Author: Even Marius Nordhagen \n"
          "# Github repo: github.com/evenmn/crystal-aging \n"
          "# \n"
          "# Load curves for push simulations as a function  \n"
          "# of time. The resistance force (friction) is \n"
          "# assumed to be the negative sum of forces on the \n"
          "# upper plate in the moving direction \n"
          "# \n")

    header_max_static = (
          "# Crystal Aging Project \n"
          "# Author: Even Marius Nordhagen \n"
          "# Github repo: github.com/evenmn/crystal-aging \n"
          "# \n"
          "# Maximum static friction as a function of \n"
          "# waiting time. Assuming that the first prominent \n"
          "# peak of the load curve corresponds to the maximum \n"
          "# static friction force. \n"
          "# \n"
          "# time [ns]\t max friction force [mN] \n")

    # open files
    if asperity:
        outfile_load_curves = outfile_load_curves.split('.')
        outifle_load_curves[0]+f'_asperity{asperity}' 
        outfile_load_curves.join() 

        outfile_max_static = outfile_max_static.split('.')
        outifle_max_static[0]+f'_asperity{asperity}' 
        outfile_max_static.join() 
   
    f_lc = open(outfile_load_curves, 'w')
    f_ms = open(outfile_max_static, 'w+')
    f_r = open(outfile_rise, 'w')
    f_lc.write(header_load_curves)
    f_ms.write(header_max_static)

    #for i, logfile in enumerate(logfiles):
    #push_time = init_time +  delta   # moment when we start pushing
    push_time = 0
    # read log file
    log_obj = File(logfile)

    if rerun:
        log_obj2 = File(rerun)
        rerun_time = log_obj2.get('Time')
        rerun_time += init_time #add the original runtime to the time
        time = np.append(log_obj.get("Time"), rerun_time) /1000  # convert from ps to ns
        fx = -np.append(log_obj.get("v_fx"), log_obj2.get('v_fx')) # change sign of friction force
    
    else:
        try:
            time = log_obj.get("Time") / 1000    # convert from ps to ns
            fx = -log_obj.get("v_fx")            # change sign of friction force
        except:
            return 0


    print("Length of log file: ", len(time))

    # smooth friction force
    fx = running_mean(fx, 1000)

    # convert friction force from eV/Å to μN (micro Newton)
    eV = value(u'elementary charge')  # J
    Å = 1e-10  # m
    fx *= eV / Å  # J/m = N
    fx *= 1e6  # mN

    #-------------------------------------------------------------------------------finding rise
    #finding where push starts, and about where it breaks

    
    #fitting sigmoid to selected interval.
    polfit_start_indx = (np.abs(time - 0.7)).argmin()
    polfit_stop_indx = (np.abs(time - 1.3)).argmin()
    #print(f'polfit start indx, time: {time[polfit_start_indx]}, {polfit_start_indx}')
    #print(f'polfit stop indx, time: {time[polfit_stop_indx]}, {polfit_stop_indx}')
    #translation so it has same shape as load_curve
    polfit_data = np.array((time[polfit_start_indx:polfit_stop_indx],
                           fx[polfit_start_indx:polfit_stop_indx])).T

    #curve fit doesn't like nan. removing theese for now
    non_nan_mask = ~np.isnan(polfit_data[:,1])
    #https://stackoverflow.com/questions/55725139/fit-sigmoid-function-s-shape-curve-to-data-using-python
    time_nnan = polfit_data[non_nan_mask,0]
    fx_nnan = polfit_data[non_nan_mask,1]
    #this was [max(time_nnan), etc and worked.. website says ydata first
    print(fx_nnan)
    p0 = [max(time_nnan), np.median(time_nnan),1,min(fx_nnan)] # this is an mandatory initial guess
    popt, pcov = curve_fit(sigmoid, time_nnan, fx_nnan,p0, method='dogbox')

    
    push_start_indx_nnan = (np.abs(time_nnan - 1.0)).argmin()
    push_stop_indx_nnan = (np.abs(time_nnan-1.1)).argmin()
    
    plt.plot(time, fx)
    plt.plot(time_nnan, sigmoid(time_nnan, *popt))
    plt.savefig('loadcurve.png')

    #repeating selection and polyfit but this time fitting linear func to sigmoid midriff
    midriff = np.array((popt[1] - 0.05, popt[1] + 0.05))

    midriff_start_indx = (np.abs(time_nnan - midriff[0])).argmin()
    midriff_stop_indx = (np.abs(time_nnan - midriff[1])).argmin()

    polfit_data2 = np.array((time_nnan[midriff_start_indx:midriff_stop_indx],
                            fx_nnan[midriff_start_indx:midriff_stop_indx])).T

    rise, intersect = np.polyfit(polfit_data2[:,0], polfit_data2[:,1], 1)

    savetxt(f_r, asarray([rise]))






    # identify first prominent peak, old method
    #peaks, _ = find_peaks(fx, prominence=prominence)
    print('peaks')
    #print(peaks)
    peak = np.max(fx_nnan[push_start_indx_nnan:push_stop_indx_nnan])
    argpeak = np.where(fx_nnan == np.max(fx_nnan[push_start_indx_nnan:push_stop_indx_nnan]))[0][0]
    peaks = (time_nnan[argpeak], peak)
    if np.isnan(peaks).any(): 
        breakpoint()
    else:
        pass
    try:
        first_peak = peaks[0]
    except IndexError:
        first_peak = 0
        warnings.warn("No prominent peaks found, try a lower prominence")

    #running mean before finding rise?
    




    # save data to files
    # we do not really need 250000 points, it just takes up
    # a lot of space and makes the curves hard to plot.
    # 1000 points should be more than sufficient
    time_short = time#time[::250]
    fx_short = fx#fx[::250]
    header_lc_intermediate = (
      " \n"
      f"push time: {push_time} ns \n"
      f"length: {len(time_short)} \n"
      "time [ns]\t\t friction force [mN]")
    savetxt(f_lc, asarray([time_short, fx_short]).T,
            header=header_lc_intermediate)
    f_ms.write(f"{push_time + peaks[0]:.10e} {peaks[1]:.10e} \n")
    f_ms.flush()


    f_lc.close()
    f_ms.close()
    f_r.close()


def extract_potential_energy(logfile, outfile="poteng.txt"):
    log_obj = File(logfile)
    time = log_obj.get('Time') / 1000      # convert from ps to ns
    poteng = log_obj.get('PotEng') / 1e6   # convert from eV to MeV

    time = time[::25]       # 1001 points is more than
    poteng = poteng[::25]   # sufficient

    header = (
          "Crystal Aging Project \n"
          "Author: Even Marius Nordhagen \n"
          "Github repo: github.com/evenmn/crystal-aging \n"
          "\n"
          "Potential energy as a function of time for the \n"
          "relaxation simulations. \n"
          "\n"
          "Time [ns]\t\t Potential energy [MeV]")

    savetxt(outfile, asarray([time, poteng]).T, header=header)


def extract_diffusion_coefficient(logfile, outfile="diffusion.txt"):
    log_obj = File(logfile)
    time = log_obj.get('Time') / 1000    # convert from ps to ns
    diff = log_obj.get('v_diffusion_coeff') / 1e4   # convert from Å^2/ps to cm^2/s

    time = time[::25]   # 1001 points is more than
    diff = diff[::25]   # sufficient

    header = (
          "Crystal Aging Project \n"
          "Author: Even Marius Nordhagen \n"
          "Github repo: github.com/evenmn/crystal-aging \n"
          "\n"
          "Diffusion coefficient as a function of time for \n"
          "the relaxation simulations. \n"
          "\n"
          "Time [ns]\t\t Diffusion coefficient [cm^2/s]")

    savetxt(outfile, asarray([time, diff]).T, header=header)


def extract_displacement(logfile, outfile="pressure.txt"):
    log_obj = File(logfile)
    time = log_obj.get('Time') / 1000     # convert from ps to ns
    press = log_obj.get('v_rx') / 10    # Convert Å to nm 

    header = (
          "Crystal Aging Project \n"
          "Author: Even Marius Nordhagen \n"
          "Github repo: github.com/evenmn/crystal-aging \n"
          "\n"
          "Normal pressure as a function of time for \n"
          "the relaxation simulations. \n"
          "\n"
          "Time [ns]\t\t distance [ns]")

    savetxt(outfile, asarray([time, press]).T, header=header)



if __name__ == '__main__':
    dumpfile = '../../simulations/sys_or100_hi110/relax/sim_temp2300_force0.001_time500_seed66342/dump.bin'
    logfile  = '../../simulations/sys_or100_hi110/relax/sim_temp2300_force0.001_time500_seed66342/log.lammps'
    
    #count_coord(dumpfile)
