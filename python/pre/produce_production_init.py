import numpy as np
import json 
from setup_system import setup_system

config_matrix = np.load('config_list.npy')
print(config_matrix)
print(config_matrix.shape)
for matrix in config_matrix:
    setup_system(matrix)
    stop
