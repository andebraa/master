"""Crystal Aging Project

Bin up atoms by their coordnation number as a
function of time

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

from glob import glob
import numpy as np
import matplotlib.pyplot as plt

from multiline import multiline

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 7, 3

s = 1
alpha = 0.6
lgnd_marker_size = 30

max_ind = 40

# user-input
height = 200
force = 0.001


# paths
project_dir = "../../"
txt_dir = project_dir + "txt/"
fig_dir = project_dir + 'fig/'


def read_coord(temp, seed, max_coord=3, num_bins=20):
    """Take average over seeds
    """
    template = txt_dir + "coordination/coordination_temp{}_force{}_hi{}_seed{}.txt"
    files = template.format(temp, force, height, seed)
    num_coords = []
    for file in glob(files):
        print(file)
        data = np.loadtxt(file)
        data = data.reshape(-1, num_bins, 2)

        num_coord  = np.empty((len(data), max_coord))
        for i in range(len(data)):
            data_ = data[i]
            data_ = data_[data_[:, 1] > 1]
            data_[:, 0] = np.round(data_[:, 0])
            if data_[0, 0] < 0.9:
                data_ = np.delete(data_, 0, 0)
            num_coord[i] = data_[:max_coord, 1]
        num_coords.append(num_coord)
    num_coord = np.mean(num_coords, axis=0)
    return num_coord


def plot_coord(num_coord, number="all"):
    time = np.linspace(0, 5, len(num_coord))
    if number == "all":
        for i in range(len(num_coord[0])):
            plt.scatter(time[max_ind:], (num_coord[max_ind:, i]-num_coord[max_ind, i]) / 1000, s=1, alpha=0.7, label=str(i+1))
    else:
        plt.scatter(time[max_ind:], (num_coord[max_ind:, number]-num_coord[max_ind, number]) / 1000, s=1, alpha=0.7, label=str(number+1))

    plt.legend(loc='best')
    plt.xlabel(r"$t$ [ns]")
    plt.ylabel(r"$N(t)-N(0)$ in thousands")
    plt.show()


def compare(*num_coords, number, labels=None):
    if labels is None:
        labels = len(num_coords) * [str(number+1)]
    for i, num_coord in enumerate(num_coords):
        time = np.linspace(0, 5, len(num_coord))
        plt.scatter(time[max_ind:], (num_coord[max_ind:, number]-num_coord[max_ind, number]) / 1000, alpha=0.7, label=labels[i])

    plt.legend(loc='best')
    plt.xlabel(r"$t$ [ns]")
    plt.ylabel(r"$N_k(t)-N_k(0)$ in thousands")
    plt.show()


if __name__ == "__main__":
    # spread in seeds
    coords = []
    times = []
    temp = 2300
    seeds = [10989, 17361, 29464, 55979, 57200, 90536]
    for seed in seeds:
        num_coord = read_coord(temp, seed, max_coord=3)
        coords.append(num_coord)
    compare(*coords, number=1, labels=seeds)

    # plot
    coords = []
    times = []
    temps = range(2000, 2500, 50)
    temps = [2000, 2150, 2300, 2450]
    for temp in temps:
        num_coord = read_coord(temp, "*", max_coord=3)
        coords.append(num_coord)
        times.append(np.linspace(0, 5, len(num_coord)))
        #plot_coord(num_coord)
    compare(*coords, number=1, labels=temps)


    # plot kink atoms and potential energy
    fig, ax = plt.subplots(1, 3)
    # kink atoms only
    times = np.asarray(times)[:, max_ind:]
    coords = np.asarray(coords)[:, max_ind:, 1] / 1000
    for temp, coord in zip(temps, coords):
        ax[1].scatter(times[0], coord-coord[0], s=s, alpha=alpha, label=fr"$T={temp}$ K")

    # get potential energy files
    poteng_dir = project_dir + 'txt/poteng/'
    template = poteng_dir + 'poteng_temp{}_force{}_seed{}.txt'

    times_elastic = []
    times_crystal = []
    elastic_list = []
    crystal_list = []
    for temp in temps:
        files = template.format(temp, force, "*")
        times, potengs = [], []
        for file in glob(files):
            data = np.loadtxt(file)
            time, poteng = data[:, 0], data[:, 1]
            times.append(time)
            potengs.append(poteng)
        time = np.mean(times, axis=0)
        poteng = np.mean(potengs, axis=0)

        # split between elasticity and crystallization 
        time_elastic = time[:max_ind]
        time_crystal = time[max_ind:]
        elastic = poteng[:max_ind]
        crystal = poteng[max_ind:] * 1e3  # convert from MeV to KeV

        times_elastic.append(time_elastic)
        times_crystal.append(time_crystal)
        elastic_list.append(elastic)
        crystal_list.append(crystal - crystal[0])

    # plot potential energy
    for i, temp in enumerate(temps):
        ax[0].scatter(times_crystal[i], crystal_list[i], s=s, alpha=alpha)

    # potential energy vs kink atoms
    for i, temp in enumerate(temps):
        ax[2].scatter(coords[i]-coords[i][0], crystal_list[i], s=s, alpha=alpha, label=fr"$T={temp}$ K")
    # label axes
    ax[0].set_xlabel(r'$t$ (ns)')
    ax[0].set_ylabel(r'$U(t)-U(0)$ (KeV)')
    ax[1].set_xlabel(r'$t$ (ns)')
    ax[1].set_ylabel(r'$N_k(t)-N_k(0)$ in thousands')
    ax[2].set_ylabel(r'$U(t)-U(0)$ (KeV)')
    ax[2].set_xlabel(r'$N_k(t)-N_k(0)$ in thousands')

    # legend 
    lgnd = ax[2].legend(loc='best')
    for handle in lgnd.legendHandles:
        handle.set_sizes([lgnd_marker_size])

    # xticks
    times = range(1, 6, 2)
    ax[0].set_xticks(times)
    ax[1].set_xticks(times)
    plt.tight_layout()
    plt.savefig(fig_dir + 'png/coord_subplots.png')
    plt.savefig(fig_dir + 'pgf/coord_subplots.pgf')
    plt.show()

