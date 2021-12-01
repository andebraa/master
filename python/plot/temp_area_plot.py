import numpy as np
import matplotlib.pyplot as plt 

# user input
#temps = range(2000, 2500, 50)
temps = [2300]
force = 0.001
orientation = "100"
height = 110
save = True

data1 = np.loadtxt('../../txt/area_relax/areas_temp2300_force0.001_55_hi115_seed69_erratic3_3_asperity0.txt')
data2 = np.loadtxt('../../txt/area_relax/areas_temp2300_force0.001_55_hi115_seed69_erratic3_3_asperity1.txt')
data3 = np.loadtxt('../../txt/area_relax/areas_temp2300_force0.001_55_hi115_seed69_erratic3_3_asperity3.txt')

time1, num1, area1 = data1[:, 0], data1[:, 1], data1[:, 2]
time2, num2, area2 = data2[:, 0], data2[:, 1], data2[:, 2]
time3, num3, area3 = data3[:, 0], data3[:, 1], data3[:, 2]

#nums = np.asarray(nums)
#areas = np.asarray(areas)


# ignore elastic part
max_ind = 35

num1 = num1[max_ind:]; area1 = area1[max_ind:]; time1 = time1[max_ind:]
num2 = num2[max_ind:]; area2 = area2[max_ind:]; time2 = time2[max_ind:]
num3 = num3[max_ind:]; area3 = area3[max_ind:]; time3 = time3[max_ind:]
#print(time)

plt.plot(time1, area1, label='asperity 1')
plt.plot(time2, area2, label='asperity 2')
plt.plot(time3, area3, label='asperity 3')
plt.legend()
plt.savefig('temp_asperities.png') 
