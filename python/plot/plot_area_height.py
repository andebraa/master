import numpy as np
import matplotlib.pyplot as plt


plt.style.use('seaborn-deep')
#plt.rcParams['figure.figsize'] = 3.5, 5

# plot various heights
for height in [55, 57, 59]:
    areas = np.loadtxt(f"../txt/area_relax/areas_2200K_{height}_hi300.txt")
    #plt.plot(areas/2)
    x = np.linspace(0, 5000, len(areas))
    plt.plot(x, running_mean(areas, 100)/200, label=f"Height: {height} Å")
plt.legend(loc='best')
#plt.grid()
plt.xlabel("Time [ps]")
plt.ylabel(r"Area [nm$^2$]")
plt.show()
