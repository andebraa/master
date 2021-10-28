"""
Crystal Aging Project

Script for generating SiC system with lower surface, asperity
and upper plate. We utilize molecular builder [1].

SiC crystals are associated with three symmetry planes with
Miller indices (100), (110) and (111). Molecular-builder creates
bulk crystals oriented after the (100) symmetry plane [2]. However,
for a SiC nanoparticle, only (110) and (111) facets will be observed.
Therefore, it is often convenient to orient the bulk after these
planes.

[1] https://github.com/hensiasv/molecular-builder
[2] Sveinsson et al., Direct Atomic Simulations of Facet Formation and
Equilibrium Shapes of SiC Nanoparticles

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
from molecular_builder import create_bulk_crystal, carve_geometry
from molecular_builder.geometry import PlaneGeometry, BoxGeometry, OctahedronGeometry, DodecahedronGeometry, ProceduralSurfaceGeometry


def orient_110(name, size):
    """Orient crystal such that (110) point along z-axis
    """
    # start from crystal that has lengths (2*max(size), 2*max(size), size[2])
    # this should be sufficient to rotate the crystal as we want
    len_100 = 2 * max(size)

    # rotate around the axis with less size
    size_100 = list(size)
    size_100[2] = len_100
    if size[0] < size[1]:
        rot_ind = 0
        size_100[1] = len_100
    else:
        rot_ind = 1
        size_100[0] = len_100

    atoms = create_bulk_crystal(name, size_100)

    # define points on 110 symmetry planes
    points = [(0, 0, len_100/2),
              (0, 0, len_100/2),
              (len_100, len_100, len_100/2),
              (len_100, len_100, len_100/2)]

    # define normal vectors of 110 symmetry planes
    if rot_ind == 0:
        normals = [(0, -1, -1),
                   (0, -1, +1),
                   (0, +1, +1),
                   (0, +1, -1)]
    else:
        normals = [(-1, 0, -1),
                   (-1, 0, +1),
                   (+1, 0, +1),
                   (+1, 0, -1)]

    # remove corners in rotation plane, i.e., remove half of the particles
    geometry = PlaneGeometry(points, normals)
    carve_geometry(atoms, geometry, side='out')

    # rotate remaining particles 45 degrees around center
    center = np.array(size_100) / 2
    if rot_ind == 0:
        atoms.rotate(45, 'x', center=center)
    else:
        atoms.rotate(45, 'y', center=center)

    # carve out desired block
    geometry = BoxGeometry(length=size, center=center)
    carve_geometry(atoms, geometry, side='out')

    # set tight cell
    atoms.set_cell(size)

    # shift particles such that initial boundaries are at the boundaries
    if rot_ind == 0:
        atoms.positions += (0, size[1]/2, size[2]/2)
    else:
        atoms.positions += (size[0]/2, 0, size[2]/2)

    # shift in z-direction
    positions = atoms.get_positions()
    min_z = np.min(positions[:, 2])
    atoms.positions -= (0, 0, min_z)

    return atoms


def orient_111(name, size):
    """Orient crystal such that (111) point along z-axis
    """
    raise NotImplementedError("orient_111 is not implemented yet!")


def gen_system(lx=300, ly=300, ax=150, ay=150, hl=50, hu=150, hup=2,
               octa_d=3, dode_d=3, lower_orient="100", remove_atoms=True,
               path='../../initial_system/'):
    """Generate system. Default parameters correspond to large aging system.
    All lengths are given in units of Å.

    Parameters:
    -----------
    lx : float
        length of system in x-direction. Default=300
    ly : float
        length of system in y-direction. Default=300
    ax : float
        initial center of asperity in x-direction. Default=150
    ay : float
        initial center of asperity in y-direction. Default=150
    hl : float
        height of lower surface. Default=50
    hu : float
        height of upper part, including asperity. Default=150
    hup : float
        gap size between lower surface and asperity. Default=2
    octa_d : float (int)
        distance from asperity center to octahedron planes. Set
        octa_d=ly/100 to make it span the system. Default=3
    dode_d : float (int)
        distance from asperity center to dodecahedron planes.
        Set dode_d=ly/100 to make it span the system. Default=3
    lower_orient : str
        orientation of lower surface (which symmetry plane
        points in z-direction. Default="100"
    remove_atoms : bool
        remove atoms from lower surface to increase the surface
        free energy. Default=True
    path : str
        path to where the initial system should be stored
    """

    # total system height
    lz = hl + hu

    # create lower surface
    if lower_orient == "100":
        lower = create_bulk_crystal("silicon_carbide_3c", (lx, ly, hl))
    elif lower_orient == "110":
        lower = orient_110("silicon_carbide_3c", (lx, ly, hl))
    else:
        raise NotImplementedError

    # carve out asperity
    asperity = create_bulk_crystal("silicon_carbide_3c", (lx, ly, lz + 5))
    geometry = OctahedronGeometry(octa_d, (ax, ay, lz - 10))  # d=n*3.90nm
    carve_geometry(asperity, geometry, side='out')
    geometry = DodecahedronGeometry(dode_d, (ax, ay, lz - 10))  # d=n*3.73nm
    carve_geometry(asperity, geometry, side='out')
    geometry = PlaneGeometry((0, 0, hl + 2), (0, 0, -1))
    carve_geometry(asperity, geometry, side="out")
    asperity.write(path + f"asperity_or{lower_orient}_hi{lz}.data", format="lammps-data")

    # cut asperity and attach to upper plate
    geometry = PlaneGeometry((0, 0, lz - hup - 2), (0, 0, 1))
    carve_geometry(asperity, geometry, side="out")
    upper = create_bulk_crystal("silicon_carbide_3c", (lx, ly, hup))
    upper.positions += (0, 0, lz - hup - 2)

    if remove_atoms:
        geometry = ProceduralSurfaceGeometry(point=(0, 0, hl + 2),
                                             normal=(0, 0, 1),
                                             thickness=5,
                                             scale=100,
                                             method='simplex',
                                             threshold=-0.1,
                                             repeat=True)
        carve_geometry(lower, geometry, side="out")

    lower.write(path + f"lower_or{lower_orient}_hi{lz}.data", format="lammps-data")

    system = asperity + lower + upper

    # replicate system
    system = system.repeat((2, 2, 1))

    # remove asperity at (0, 0)
    geometry = BoxGeometry(lo_corner=(0, 0, hl + 2), hi_corner=(lx, ly, lz - hup - 3))
    carve_geometry(system, geometry, side='in')

    system_file = path + f"system_or{lower_orient}_hi{lz}.data"
    system.write(system_file, format="lammps-data")
    print("System written to: ", system_file)

    return system, asperity, lower


if __name__ == "__main__":
    sic_110 = orient_110("silicon_carbide_3c", (100, 100, 20))
    print(len(sic_110))
    sic_110.write("sic_110.data", format="lammps-data")
