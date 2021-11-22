from ovito.io import import_file, export_file

pipeline = import_file(dumpfile, multiple_frames = True)

i = 1
j = 0

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

pipeline.ass_to_scene()
