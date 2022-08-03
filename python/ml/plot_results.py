import numpy as np
from glob import glob
from utils import *
import matplotlib.pyplot as plt

path = 'CV_results/'

files = glob.glob(path+'*')

random = []
actual = []

fig, axs = plt.subplots(2)
axs = axs.ravel()
print(files)
for i,_file in enumerate(files):
    obj = np.load(_file, allow_pickle = True)
    best_mse = obj['arr_0'][0].mse_test
    best_r2 = obj['arr_0'][0].r2_test
    if 'random' in _file:
        random.append((best_r2, best_mse))
        axs[0].plot(i, best_r2, c='r')
        axs[1].plot(i, best_mse, c='r')
    else:
        actual.append((best_r2, best_mse))
        axs[0].plot(i, best_r2, c='b')
        axs[1].plot(i, best_mse, c='b')

fig.savefig('CV_results/ml_plot.png')
print(random)
print(actual)
