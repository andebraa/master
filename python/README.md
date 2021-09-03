# Python scripts
In this directory we provide all Python scripts needed to reproduce our results. 

## Pre
The pre-processing scripts utilize [molecular-builder](https://github.com/henriasv/molecular-builder.git), which again is built on top of the [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/).

## Run 
The run scripts utilize [lammps-simulator](https://github.com/evenmn/lammps-simulator.git) to launch the simulations. To run the LAMMPS simulations, a working LAMMPS executable compiled with the 'manybody', 'rigid' and 'python' packages is required. In practise, the simulations have to be run on a GPU (or similar) to maintain reasonable wall-clock simulation times. For this, the 'kokkos' package is also highly recommended.

## Post
To post-process the simulation files (log and dump files) we use [lammps-logfile](https://github.com/henriasv/lammps-logfile.git) (log files) and [Ovito](https://www.ovito.org/) (dump files).

## Plot
To generate plots, we use [matplotlib](https://matplotlib.org/) and convert them to [PGFPlots](http://pgfplots.sourceforge.net/). 
