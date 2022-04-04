import numpy as np
import json 
from setup_system import setup_system
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
#config_matrix = np.load('config_list.npy')
#print(config_matrix)
#print(config_matrix.shape)
config_matrix = [np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]])]
init_path = '~/master/initial_system/production'

init_dict = {}

for i,matrix in enumerate(config_matrix):
    init_dict[i] = matrix
    setup_system(matrix, i)

with open('init_dict.json', 'w') as fp:
    json.dump(init_dict, fp, cls = NumpyEncoder)
