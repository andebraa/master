import numpy as np
from glob import glob
from utils import *
import matplotlib.pyplot as plt
plt.style.use('seaborn')

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
c = plt.cm.viridis((1 - np.arange(2))/(1 - 0 + 0.1))
for i,_file in enumerate(files_dnn):
    obj = np.load(_file, allow_pickle = True)
    best_mse = obj['arr_0'][0].mse_test
    best_r2 = obj['arr_0'][0].r2_test
    print('i, best config')
    print(_file)
    print(i, obj['arr_0'][0])
    if 'random' in _file:
        random_dnn.append((best_r2, best_mse))
        axs[0].plot(best_mse, best_r2, 'o',c=c[0])
        print('^^random')
    else:
        actual_dnn.append((best_r2, best_mse))
        axs[0].plot(best_mse, best_r2, 'o',c=c[1])


for i,_file in enumerate(files_cnn):
    obj = np.load(_file, allow_pickle = True)
    best_mse = obj['arr_0'][0].mse_test
    best_r2 = obj['arr_0'][0].r2_test
    print('i, best config')
    print(i, obj['arr_0'][1])
    if 'random' in _file:
        random_cnn.append((best_r2, best_mse))
        axs[1].plot(best_mse, best_r2, 'o',c=c[0])
        print('^^random')
    else:
        actual_cnn.append((best_r2, best_mse))
        axs[1].plot(best_mse, best_r2, 'o',c=c[1])

axs[1].set_title('cnn')
axs[0].set_title('dnn')
axs[0].set_xlabel('mse')
axs[1].set_xlabel('mse')
axs[0].set_ylabel('r2')
axs[1].set_ylabel('r2')
plt.tight_layout()
fig.savefig('fig/ml_res.png', dpi = 200)
