from ovito.io import import_file, export_file
from ovito.modifiers import *
from ovito.pipeline import *

dumpfile = '/home/andebraa/master/initial_system/erratic/system_or100_hi115_errgrid3_3.data'

pipeline = import_file(dumpfile)#, multiple_frames = True)

lx = 100.27080000000001
ly = 100.27080000000001

i = 0
j = 0

# first outward slice X direction
pipeline.modifiers.append(SliceModifier(
distance = (i+1)*lx,
normal = (1.0, 0.0, 0.0)))
print('i+1 *lx=', (i+1)*lx)
print('inverse false')

# first inward slice X direction
pipeline.modifiers.append(SliceModifier(
distance = (i)*lx,
normal = (1.0, 0.0, 0.0),
inverse = True))
print('i *lx=', (i)*lx)
print('inverse')

# first outward slice Y direction
pipeline.modifiers.append(SliceModifier(
distance = (j+1)*ly,
normal = (0.0, 1.0, 0.0)))
print('j+1 *ly=', (j+1)*ly)
print('inverse false')

# first outward slice Y direction
pipeline.modifiers.append(SliceModifier(
distance = (j)*ly,
normal = (0.0, 1.0, 0.0),
inverse = True))
print('j *ly=', (j)*ly)
print('inverse')

pipeline.add_to_scene()
