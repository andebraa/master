import numpy as np
import matplotlib.pyplot as plt 

# user input
#temps = range(2000, 2500, 50)
temps = [2300]
force = 0.001
orientation = "100"
height = 110
save = True

data = np.loadtxt('../../txt/area_relax/areas_temp2300_force0.001_55_hi115_seed69_erratic3_3_asperity0.txt')

time, num, area = data[:, 0], data[:, 1], data[:, 2]

#nums = np.asarray(nums)
#areas = np.asarray(areas)


# ignore elastic part
max_ind = 35

num = num[max_ind:]
area = area[max_ind:]
time = time[max_ind:]
print(time)

plt.plot(time, area)
plt.savefig('temp_asperity0.png') 
