import numpy as np
from glob import glob
from utils import *
import matplotlib.pyplot as plt

path_dnn = 'CV_results/dnn/'
path_cnn = 'CV_results/cnn/'


files_dnn = glob.glob(path_dnn+'*')
files_cnn = glob.glob(path_cnn+'*')

random_dnn = []
actual_dnn = []

random_cnn = []
actual_cnn = []

fig, axs = plt.subplots(2)
axs = axs.ravel()
for i,_file in enumerate(files_dnn):
    obj = np.load(_file, allow_pickle = True)
    best_mse = obj['arr_0'][0].mse_test
    best_r2 = obj['arr_0'][0].r2_test
    if 'random' in _file:
        random_dnn.append((best_r2, best_mse))
        axs[0].plot(best_mse, best_r2, 'o',c='r')
    else:
        actual_dnn.append((best_r2, best_mse))
        axs[0].plot(best_mse, best_r2, 'o',c='b')


for i,_file in enumerate(files_cnn):
    obj = np.load(_file, allow_pickle = True)
    best_mse = obj['arr_0'][0].mse_test
    best_r2 = obj['arr_0'][0].r2_test
    if 'random' in _file:
        random_cnn.append((best_r2, best_mse))
        axs[1].plot(best_mse, best_r2, 'o',c='r')
    else:
        actual_cnn.append((best_r2, best_mse))
        axs[1].plot(best_mse, best_r2, 'o',c='b')

axs[1].set_title('cnn')
axs[0].set_title('dnn')
fig.savefig('fig/ml_plot.png')
