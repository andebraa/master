import json
import numpy as np
import matplotlib.pyplot as plt

def coords2nums(coord=None):
    nums = {}
    count = 1
    for y in range(4):
        for x in range(4):
            nums[(x,y)] = count
            count+=1
    if coord is None:
        return coord
    else:
        return nums[coord]


with open ('2asp_init_dict.json') as fp:
#note that seeds contain runs of the same system, so all are similar to seeds[0]
    aux_dict = json.loads(fp.read())

norms = np.zeros((len(aux_dict.keys())))
for i, elem in enumerate(aux_dict.items()):
    print(elem)
    trix = aux_dict[str(i)]
    trix = np.array(trix)

    indices = np.asarray(np.where(trix==1)).T
    norms[i] = np.linalg.norm((indices[0]- indices[1]))
print(norms)
