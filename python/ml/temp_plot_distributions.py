import numpy as np
import matplotlib.pyplot as plt

randx = np.load('rand_matrix.npy')
randy = np.load('rand_y.npy')
x = np.load('out_matrix.npy')
y = np.load('out_y.npy')

print(y)
print(np.shape(y))
fig, ax = plt.subplots(3,2)
#ax = ax.ravel()

print(ax)
print(np.shape(ax))
#ax[0].set_title('random data')
#ax[0].hist(randy[:,2]) 
#ax[1].set_title('actual data')
#ax[1].hist(y[:,2])

for i in range(3):
    ax[i,0].hist(randy[:,i])
    ax[i,1].hist(y[:,i])
ax[0,0].set_title('random max static')
ax[0,1].set_title('actual max static')
ax[1,0].set_title('random sigmoid slope')
ax[1,1].set_title('actual sigmoid slope')
ax[2,0].set_title('random max sigmoid')
ax[2,1].set_title('actual max sigmoid')

plt.tight_layout()
plt.savefig('fig/ml_data_distribution.png', dpi = 200)
