[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Aging due to crystallization
In this project, we study the friction aging due to crystallization, which is responsible for the time-dependent static friction. Ref article. equations. 

INSERT ASPERITY EVOLUTION ILLUSTRATION

### Evolution of the contact area
The evolution of the contact area can be described by  

INSERT AREA EQUATION (as a figure)

### Time-dependent static friction

INSERT F = Z * S (as a figure)

INSERT S = ... (as a figure)

All files needed to reproduce the article can be found here.

## Structure of this repo
Both preprocessing, simulation launching, postprocessing and plotting is done in Python. The actual simulations are run using LAMMPS. Below, we have made a sketch of the structure of this repository. All actions are performed from the python directory: System setup is done by running the file `python/pre/setup_system.py`, launching simulations is done by running one of the files `python/run/run_*.py`, postprocessing dump files using Ovito is done by `python/post/ovito_utils.py` and plotting is done by the files `python/plot/plot*.py`. 
```
├── initial_system
├── lammps
├── python
│   ├── pre
│   ├── run
│   ├── post
│   └── plot
├── txt
│   ├── area_push
│   ├── area_relax
│   ├── coordination
│   └── max_static
├── fig
|   ├── png
│   └── pgf
└── README.md
```

## Preprocessing
We preprocess the system using [molecular-builder](https://github.com/henriasv/molecular-builder), which again is built around the [ASE](https://wiki.fysik.dtu.dk/ase/) package. The asperity was prepared by carving out a rectangular octahedron from a 3C-SiC block with distance 11.19 nm between the (110) planes and the center of the asperity, and then a convex rectangular dodecahedron with distance 11.70 nm between the (111) planes and the center of the asperity. That makes the asperity similar to the equilibrium shapes of 3C-SiC found by Sveinsson et al. [[1]](#sveinsson). Then the asperity was cut and attached to the upper plate. The lower plate is just a (30nm x 30nm x 5nm) 3C-SiC block oriented either with the (100) or (110) plane pointing in z-direction. Random atoms were removed from the upper layer of the lower surface using Perlin noise. This is done by the file `python/pre/setup_system.py`, which can be tweeked.

## Launch simulations
To launch the LAMMPS molecular dynamics simulations, we use the [lammps-simulator](https://github.com/evenmn/lammps-simulator) package. We perform two types of LAMMPS simulations: Relaxation simulations where the asperity is at rest and push simulations where the asperity is moved at a constant velocity. The simulations are run from `python/run/run_relax.py` and `python/run/run_push.py` respectively, which again call `lammps/in.relax` and `lammps/in.push`. The simulations are computationally intensive.

We perform molecular dynamics simulations of the system in LAMMPS [REF], with the SiC force-field and parameters found by Vashishta et al. [REF] The uppermost and lowermost 1 nm of the system is held rigid (but the lower plate is allowed to move freely in the z-direction). A Langevin thermostat [REF] with damping time (??) is applied on the regions defined by z E [1, 2]nm U [18, 19]nm, which effectively sets the temperature of the system. The equation of motion is solved by a Verlet integration scheme [REF] with a time step of 2 fs and periodic boundary conditions. All simulations were run on NVIDIA A100 graphics cards using the KOKKOS package in LAMMPS.

## Postprocessing
The contact area analysis and coordination analysis are done using OVITO [REF]. The script for this is found in `python/post/ovito_utils.py`. The max static friction was found as the first prominent peak of the load curves when pushing the asperity. The contact area for the various simulations as a function of time is saved as text files in `txt/area_relax` or `txt/area_push`. The max static friction is ...

## Plotting
We use matplotlib [REF] to plot the graphs, and convert them to PGF-format for better rendering in LaTeX. To plot either the text files or LAMMPS log files, use the scripts in `python/plot`. Generated plots can be found in the `fig` directory. 

## References
<a name="sveinsson"></a> [1] [Henrik Andersen Sveinsson, Anders Hafreager, Rajiv K. Kalia, Aiichiro Nakano, Priya Vashishta, and Anders Malthe-Sørenssen
Crystal Growth & Design 2020 20 (4), 2147-2152
DOI: 10.1021/acs.cgd.9b00612 ](https://pubs.acs.org/doi/10.1021/acs.cgd.9b00612)  

## License
[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
