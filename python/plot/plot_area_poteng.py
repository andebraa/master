import numpy as np
import matplotlib.pyplot as plt
from lammps_logfile import File, running_mean
from mpl_toolkits.axes_grid1 import make_axes_locatable

from ..regression import lin_reg, poly_reg, nonlin_reg
from ..multiline import multiline

plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 3.5, 5


# Plot 2200K, 2250K and 2300K
obj_2100 = File('/datastorage/sic-friction/simulation/aging/sys_or100_hi300/relax/sim_temp2100_force0.001_time5000_seed28098/log.lammps')
obj_2150 = File('/datastorage/sic-friction/simulation/aging/sys_or100_hi300/relax/sim_temp2150_force0.001_time5000_seed68458/log.lammps')
obj_2200 = File('/datastorage/sic-friction/simulation/large_torque/sim_temp2200_vel0_0_0_0_0_0_0_0_0_0_force0.001_time500_500_500_500_500_500_500_500_500_500_seed86871/log.lammps')
obj_2250 = File('/datastorage/sic-friction/simulation/aging_smooth/sim_temp2250_force0.001_time5000_seed73230/log.lammps')
obj_2300 = File('/datastorage/sic-friction/simulation/aging_smooth/sim_temp2300_force0.001_time5000_seed17361/log.lammps')
obj_2400 = File('/datastorage/sic-friction/simulation/aging/sys_or100_hi300/relax/sim_temp2400_force0.001_time5000_seed93403/log.lammps')
obj_2450 = File('/datastorage/sic-friction/simulation/aging/sys_or100_hi300/relax/sim_temp2450_force0.001_time5000_seed77815/log.lammps')

temps = [2150] #[2100, 2150, 2200, 2250, 2300, 2400, 2450]
objs = [obj_2150] #[obj_2100, obj_2150, obj_2200, obj_2250, obj_2300, obj_2400, obj_2450]

potengs = []
nums = []
areas = []
times = []
times_p = []
for temp, obj in zip(temps, objs):
    poteng = obj.get('PotEng') / 1e6
    data = np.loadtxt(f'../txt/area_relax/areas_{temp}K_55_hi300.txt')
    num, area = data[:, 0], data[:, 1]
    if temp == 2200:
        num = num[::10]
        area = area[::10]
    time = np.linspace(0, 5, len(area))
    time_p = np.linspace(0, 5, len(poteng))

    # ignore elastic part
    max_ind = np.argmax(poteng)
    indx_crys = int(max_ind * len(area) / len(poteng))

    num = num[indx_crys:]
    area = area[indx_crys:]
    time = time[indx_crys:]
    poteng = poteng[max_ind:]
    time_p = time_p[max_ind:]

    nums.append(num)
    areas.append(area)
    times.append(time)
    potengs.append(poteng)
    times_p.append(time_p)

'''
for time, area, temp in zip(times, areas, temps):
    plt.plot(time, area, 'o', markersize=0.2, label=f'$T={temp}K')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
plt.tight_layout()
plt.savefig("../pgf/aging/large_area.pgf")
plt.show()
'''
def U(t, e):
    c = 4.07233157
    tau = 1.44010943
    d = -3.88996977
    return e*(c/(1+t/tau) + d)

def A(t, A0, tau, c):
    tau = 1
    #tau = c # * np.exp((b-1)/c)
    return A0*(1+c*np.log(1+t/tau))

bounds = [[10, 40], [0.001, 10], [-10, 10]]

'''
for time, num, area, temp in zip(times, nums, temps):
    #param = nonlin_reg(time, area, A, bounds)

    plt.scatter(time, num, s=1, alpha=0.4, label=fr'$T={temp}$K')
    plt.scatter(time, area, s=1, alpha=0.4, label=fr'$T={temp}$K')
    #plt.plot(time, A(time, *param), 'k--')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$N(t)$')
plt.tight_layout()
#plt.savefig("../pgf/aging/large_area_regression.pgf") 
plt.show()
'''

# colorbar plot
fig, ax = plt.subplots(2)
lc = multiline(times_p, potengs, temps, ax=ax[0], lw=2, cmap='cividis')
lc = multiline(times, areas, temps, ax=ax[1], lw=2, cmap='cividis')

for time, area, temp in zip(times, areas, temps):
    param = nonlin_reg(time, area, A, bounds)
    ax[1].plot(time, A(time, *param), 'k--')


bounds = [[-10, 10], [-10, 10], [-10, 10]]

for time, poteng, temp in zip(times_p, potengs, temps):
    param = nonlin_reg(time, poteng, U, bounds)
    ax[0].plot(time, U(time, *param), 'k--')

plt.tight_layout(rect=[0.05, 0.05, 1.0, 0.95])
#fig.subplots_adjust(right=0.7)
#cbar_ax = fig.add_axes([0.75, 0.15, 0.05, 0.7])
divider = make_axes_locatable(ax[1])
cax = divider.new_vertical(size='5%', pad=0.6, pack_start=True)
fig.add_axes(cax)
axcb = fig.colorbar(lc, cax=cax, orientation="horizontal") #, extend='both')
axcb.set_label("Temperature [K]")
ax[1].set_xlabel('$t$ [ns]')
ax[0].set_ylabel('$U(t)$ [MeV]')
ax[1].set_ylabel('$A(t)$ [nm$^2$]')
ax[0].set_xticks([])
ax[0].set_yticks([-5.14, -5.16, -5.18, -5.20, -5.22])
ax[1].set_xticks([0, 1, 2, 3, 4, 5])
plt.savefig("../pgf/aging/poteng_area.pgf")
plt.show()

'''
# comp
fig, ax = plt.subplots()
potengs = np.asarray(potengs)
lc = multiline(times_p, potengs-potengs[:, 0], temps, ax=ax, lw=2, cmap='cividis')

bounds = [[-10, 10], [-10, 10], [-10, 10]]
bounds = [[-10, 10]]

for time, poteng, temp in zip(times_p, potengs, temps):
    param = nonlin_reg(time, poteng-poteng[0], U, bounds)
    ax.plot(time, U(time, *param), 'k--')

plt.show()
'''
stop


# plot log x-scale
plt.scatter(time_2300*1e3, area_2300, alpha=0.5, label=f'$T=2300$K')
plt.scatter(time_2250*1e3, area_2250, alpha=0.5, label=f'$T=2250$K')
plt.scatter(time_2200*1e3, area_2200, alpha=0.5, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ps]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.xscale('log')
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_logx.pgf") 
plt.show()

# take exp of lines
exp_2200 = np.exp((area_2200-b_2200)/a_2200)
exp_2250 = np.exp((area_2250-b_2250)/a_2250)
exp_2300 = np.exp((area_2300-b_2300)/a_2300)

plt.plot(time_2300, exp_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp.pgf") 
plt.show()

# take exp of lines, same a and b 
exp_2200 = np.exp((area_2200-b_2300)/a_2300)
exp_2250 = np.exp((area_2250-b_2300)/a_2300)
exp_2300 = np.exp((area_2300-b_2300)/a_2300)

plt.title(rf"$a$={a_2300:.5f}, $b$={b_2300:.5f}")
plt.plot(time_2300, exp_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_common.pgf") 
plt.show()

# take exp of lines and do linear regression
a_lin_2200 = reg(time_2200, exp_2200, 1, bias=False)
a_lin_2250 = reg(time_2250, exp_2250, 1, bias=False)
a_lin_2300 = reg(time_2300, exp_2300, 1, bias=False)

plt.plot(time_2300, exp_2300, label=rf'$T=2300$K, $t^*$ = {1/a_lin_2300[0]:.5f}')
plt.plot(time_2250, exp_2250, label=rf'$T=2250$K, $t^*$ = {1/a_lin_2250[0]:.5f}')
plt.plot(time_2200, exp_2200, label=rf'$T=2200$K, $t^*$ = {1/a_lin_2200[0]:.5f}')
plt.plot(time_2200, a_lin_2200*time_2200, 'k--')
plt.plot(time_2250, a_lin_2250*time_2250, 'k--')
plt.plot(time_2300, a_lin_2300*time_2300, 'k--')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_common_slope.pgf") 
plt.show()









### redo with smoothed graphs
area_2200 = running_mean(area_2200, len(area_2200) // 200)
area_2250 = running_mean(area_2250, len(area_2250) // 200)
area_2300 = running_mean(area_2300, len(area_2300) // 200)

# plot contact area
plt.plot(time_2300, area_2300, label=f'$T=2300$K')
plt.plot(time_2250, area_2250, label=f'$T=2250$K')
plt.plot(time_2200, area_2200, label=f'$T=2200$K')
plt.legend(loc='best')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_smooth.pgf") 
plt.show()

# plot contact area area collapse
plt.plot(time_2300, (area_2300)*0.79, label=f'$T=2300$K')
plt.plot(time_2250, (area_2250)*0.89, label=f'$T=2250$K')
plt.plot(time_2200, (area_2200), label=f'$T=2200$K')
plt.legend(loc='best')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_smooth_area_collapse.pgf") 
plt.show()

# plot contact area with regression
plt.plot(time_2300, area_2300, label=f'$T=2300$K')
plt.plot(time_2250, area_2250, label=f'$T=2250$K')
plt.plot(time_2200, area_2200, label=f'$T=2200$K')
plt.plot(time_2200, a_2200*np.log(time_2200) + b_2200, 'k--')
plt.plot(time_2250, a_2250*np.log(time_2250) + b_2250, 'k--')
plt.plot(time_2300, a_2300*np.log(time_2300) + b_2300, 'k--')
plt.legend(loc='best')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_regression_smooth.pgf") 
plt.show()

# plot contact area with common regression
plt.plot(time_2300, area_2300, label=f'$T=2300$K')
plt.plot(time_2250, area_2250, label=f'$T=2250$K')
plt.plot(time_2200, area_2200, label=f'$T=2200$K')
plt.plot(time_2200, a_2300*(np.log(time_2200 * a_lin_2200)) + b_2300, 'k--')
plt.plot(time_2250, a_2300*(np.log(time_2250 * a_lin_2250)) + b_2300, 'k--')
plt.plot(time_2300, a_2300*(np.log(time_2300 * a_lin_2300)) + b_2300, 'k--')
plt.legend(loc='best')
plt.xlabel(r'$t$ [ns]')
plt.ylabel(r'$A(t)$ [nm$^2$]')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_regression_common_smooth.pgf") 
plt.show()


# take exp of lines with different a and b
exp_2200 = np.exp((area_2200-b_2200)/a_2200)
exp_2250 = np.exp((area_2250-b_2250)/a_2250)
exp_2300 = np.exp((area_2300-b_2300)/a_2300)

plt.plot(time_2300, exp_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_smooth.pgf") 
plt.show()


# take exp of lines with common a and b
exp_2200 = np.exp((area_2200-b_2300)/a_2300)
exp_2250 = np.exp((area_2250-b_2300)/a_2300)
exp_2300 = np.exp((area_2300-b_2300)/a_2300)

plt.plot(time_2300, exp_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_common_smooth.pgf") 
plt.show()


# take exp of lines and do regression
exp_2200 = np.exp((area_2200-b_2300)/a_2300)
exp_2250 = np.exp((area_2250-b_2300)/a_2300)
exp_2300 = np.exp((area_2300-b_2300)/a_2300)

plt.plot(time_2300, exp_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200, label=f'$T=2200$K')
plt.plot(time_2200, a_lin_2200*time_2200, 'k--')
plt.plot(time_2250, a_lin_2250*time_2250, 'k--')
plt.plot(time_2300, a_lin_2300*time_2300, 'k--')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_common_slope_smooth.pgf") 
plt.show()


# collapse exp
plt.plot(time_2300, exp_2300/a_lin_2300, label=f'$T=2300$K')
plt.plot(time_2250, exp_2250/a_lin_2250, label=f'$T=2250$K')
plt.plot(time_2200, exp_2200/a_lin_2200, label=f'$T=2200$K')
plt.xlabel(r"$t$ [ns]")
plt.ylabel(r"$\exp((A(t)-b)/a)$")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_exp_common_collapse_smooth.pgf") 
plt.show()

# collapse A(t)
plt.plot(time_2300 * a_lin_2300, area_2300, label=rf'$T=2300$K $t^*$={1/a_lin_2300[0]:.5f}')
plt.plot(time_2250 * a_lin_2250, area_2250, label=rf'$T=2250$K $t^*$={1/a_lin_2250[0]:.5f}')
plt.plot(time_2200 * a_lin_2200, area_2200, label=rf'$T=2200$K $t^*$={1/a_lin_2200[0]:.5f}')
plt.xlabel(r"$t/t^*$")
plt.ylabel(r"$A(t/t^*)$ [nm$^2$]")
plt.legend(loc='best')
#plt.grid()
plt.tight_layout()
plt.savefig("../pgf/aging/large_area_time_collapse_smooth.pgf") 
plt.show()


# area change
da_2200 = np.diff(area_2200, append=0)
da_2250 = np.diff(area_2250, append=0)
da_2300 = np.diff(area_2300, append=0)

da_2200 = running_mean(da_2200, len(da_2200)//10)
da_2250 = running_mean(da_2250, len(da_2250)//10)
da_2300 = running_mean(da_2300, len(da_2300)//10)

plt.plot(time_2200, da_2200, label=f'$T=2200$K')
plt.plot(time_2250, da_2250, label=f'$T=2250$K')
plt.plot(time_2300, da_2300, label=f'$T=2300$K')
plt.yscale('log')
plt.show()
