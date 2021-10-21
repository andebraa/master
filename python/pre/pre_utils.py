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
import re
import numpy as np
from molecular_builder import create_bulk_crystal, carve_geometry
from molecular_builder.geometry import PlaneGeometry, BoxGeometry, OctahedronGeometry, DodecahedronGeometry, ProceduralSurfaceGeometry
from ase import Atoms 

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

    

    system = asperity + lower + upper
    

    return system#, asperity, lower



def empty_square(lx=300, ly=300, ax=150, ay=150, hl=50, hu=150, hup=2,
               octa_d=3, dode_d=3, lower_orient="100", remove_atoms=True,
               path='../../initial_system/'):

    """
    Same as gen_system. produces a tile without an asperity. 
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

    #Can i just hash this out and it'll still work?
    # carve out asperity
    asperity = create_bulk_crystal("silicon_carbide_3c", (lx, ly, lz + 5))
    geometry = OctahedronGeometry(octa_d, (ax, ay, lz - 10))  # d=n*3.90nm
    carve_geometry(asperity, geometry, side='out')
    geometry = DodecahedronGeometry(dode_d, (ax, ay, lz - 10))  # d=n*3.73nm
    carve_geometry(asperity, geometry, side='out')
    geometry = PlaneGeometry((0, 0, hl + 2), (0, 0, -1))
    carve_geometry(asperity, geometry, side="out")
    

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



    system = lower + upper


    return system#, asperity, lower


def gen_grid_system(lx=300, ly=300, ax=150, ay=150, hl=50, hu=150, hup=2,
               octa_d=3, dode_d=3, lower_orient="100", remove_atoms=True,
               path='../../initial_system/', grid = (3,3), erratic = False):
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
    grid : tuple
        shape of the system as asperities are copied in a grid
    erratic: bool
        If erratic, the function will return top and bottom plate seperate from
        asperities, for use in erratic grid where asperites are edited
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
    #asperity.write(path + f"asperity_or{lower_orient}_hi{lz}.data", format="lammps-data")

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

    #lower.write(path + f"lower_or{lower_orient}_hi{lz}.data", format="lammps-data")


    if erratic: #seperate lower, upper and asperity, so removal of asperities is easier
        asperity_system = asperity.repeat((grid[0], grid[1], 1)) 
        lower_upper_system = lower + upper 
        lower_upper_system = lower_upper_system.repeat((grid[0], grid[1], 1)) 
        return lower_upper_system, asperity_system
    system = asperity + lower + upper
    system = system.repeat((grid[0], grid[1], 1))


    return system

def erratic_setup(lx=99.9, ly=100, ax=50, ay=50, hl=50, hu=60, hup=2,
               octa_d=39.0, dode_d=37.3, lower_orient="100", remove_atoms=True,
               path='../../initial_system/', grid = (3,3)):

    """
    script for generating a system with squares of asperities and without. grid input is in this
    instance a boolean array which describes the location of asperities.
    """
    # total system height
    lz = hl + hu

    bool_grid = np.random.randint(0,2,size=grid).astype(tuple)
    

    system = 0
    systems = Atoms()
    tolerance = 0 #add a little extra space, to avvoid crashing 
     

    #we call a nXn grid, and then remove asperities that we don't want
    top_bot_system, asperity_system = gen_grid_system(lx=99.9, ly=100, ax=50, ay=50, hl=50, hu=60, hup=2,
                                                      octa_d=39.0, dode_d=37.3, lower_orient="100", remove_atoms=True,
                                                      path='../../initial_system/', grid = grid)

    #finding the size of the system, and then dividing this into grid cells
    shape = re.findall(r'Cell\(\[(\d+\.\d+), (\d+\.\d+), (\d+\.\d+)\]\)', str(system.get_cell()))
    shape = [float(shape[0][0]), float(shape[0][1]), float(shape[0][2])]

    sys_lx, sys_ly, sys_lz = shape #the size of the whole system
    lx_actual, ly_actual = sys_lx/grid[0], sys_ly/grid[1] #the size of one partition

    print(lx_actual, ly_actual)    
    #divide the system into squares nXn. linspace(start, stop, num)
    partition = (np.linspace(0,lx_actual, grid[0]), np.linspace(0,ly_actual, grid[1])) 
    

    #TODO seperate asperities from lower and upper, i.e return lower and upper in one system, and asperity in another,
    # this way you can remove asperities witout worrying about upper and lower
    # modify gen_grid_system to perhaps take this as an argument

    for i in range(len(partition[0])):
        for j in range(len(partition[1])):
            
            if not bool_grid[i,j]: #if bool_grid == false , remove asperity
                #lx_actual is midpoint of partition, then it jumps the length of a partition to find next midpoint
                #OctahedronGeometry(d, center = [0,0,0]) 
                #geometry = OctahedronGeometry(octa_d, ((lx_actual/2 + lx_actual*i), ly_actual/2 + ly_actual*i, lz -10)) 
                geometry = BoxGeometry(center=((lx_actual/2 + lx_actual*i), ly_actual/2 + ly_actual*i, lz -10), 
                                       length = (lx_actual, ly_actual, lz))                                         
                carve_geometry(asperity_system, geometry, side = 'in') #carve inverse of when it was created
            else:
                pass #keep asperity
    system = top_bot_system + asperity_system #combine now edited asperities and top and bottom
        
    """ #keeping for archive pourposes
    for i in range(len(bool_grid[0])):
        for j in range(len(bool_grid[:,0])):
            
            print(bool_grid[i,j])
            if bool_grid[i,j]:
                system = empty_square(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                      remove_atoms, path)

            else:
                system = gen_system(lx, ly, ax, ay, hl, hu, hup, octa_d, dode_d, lower_orient,
                                    remove_atoms, path)

            shape = re.findall(r'Cell\(\[(\d+\.\d+), (\d+\.\d+), (\d+\.\d+)\]\)', str(system.get_cell()))
            shape = [float(shape[0][0]), float(shape[0][1]), float(shape[0][2])]
            xy = np.array((1,1,0))

            lx_actual, ly_actual, lz_actual = shape

            system.positions += ((lx_actual+tolerance)*i, (ly_actual+tolerance)*j, 0) #atoms.position from ASE 
            systems += system

    """
    return system



if __name__ == "__main__":
    pass
    #sic_110 = orient_110("silicon_carbide_3c", (200, 100, 20))
    #print(len(sic_110))
    #sic_110.write("sic_110.data", format="lammps-data")
