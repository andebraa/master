import numpy as np
import json 
from setup_system import setup_system
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

asperities = 8

if asperities == 2:
    config_matrix = np.load('2asp_config_list.npy')
elif asperities == 8:
    config_matrix = np.load('config_list.npy')

#print(config_matrix)
#print(config_matrix.shape)
#config_matrix = [np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]])]

init_dict = {}

for i,matrix in enumerate(config_matrix):
    init_dict[i] = matrix
    setup_system(matrix, i, asperities = asperities)

if asperities == 8:

    with open('8asp_init_dict.json', 'w') as fp:
        json.dump(init_dict, fp, cls = NumpyEncoder)
elif asperities ==2:
    with open('2asp_init_dict.json', 'w') as fp:
        json.dump(init_dict, fp, cls = NumpyEncoder)

