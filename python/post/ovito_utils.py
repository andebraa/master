import pandas as pd
from ovito.io import *
import re
from ovito.modifiers import *
import numpy
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def compute_max_z(frame, data):
    data.attributes["High_Z"] = numpy.max(data.particles["Position"][:,2])

def max_z_finder(asperities, uc, temp, time, initnum):

    highz_dir = '../../txt/high_z/'
    max_zs = []
    avg_max = []
    for force in [0, 0.0001, 0.001, 0.01]:
        dumpfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*_errgrid4_4/dump.bin'
        for dumpfile in glob(dumpfiles):

            pipeline = import_file(dumpfile)
            seed = re.findall('\d+', dumpfile)[-3]
            print(dumpfile)
            #print(pipeline.data.particles['Position'][:,2])
            #stop
            pipeline.modifiers.append(compute_max_z)
            output = pipeline.compute()
            outfiles = highz_dir + f"maxz_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}.txt"
            export_file(pipeline, outfiles, "txt", columns=["Timestep", "High_Z"], multiple_frames = True)
    
def plot_max_z(asperities, uc, temp, time, initnum):
    fig, axs = plt.subplots(2,2, figsize = (10,10))

    axs = axs.ravel()
    for i, force in enumerate([0, 0.0001, 0.001, 0.01]):
        heights = []
        files = highz_dir + f"maxz_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*.txt"
        for _file in glob(files):
            print(_file)
            seed = re.findall(r'\d+', _file)[-1]
            print(seed)
            #df = pd.read_csv(_file, sep = '')
            data = np.loadtxt(_file)
            frames = []
            height = []
            for row in data:
                frames.append(row[0])
                height.append(row[1])
            frames = np.array(frames)
            height = np.array(height)
            heights.append(height)
            axs[i].plot(frames, height, label = seed)
            
        avg_max.append(np.mean(heights, axis = 0))
        axs[i].set_title(str(force))
        axs[i].plot(frames, avg_max[i], label = 'average')
        axs[i].legend()
    plt.savefig('test.png')

def displacement_x(asperities, uc, temp, time, initnum):
    xdist_dir = '../../txt/xdist/'

    for force in [0, 0.0001, 0.001, 0.01]:
        dumpfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*_errgrid4_4/dump.bin'
        for dumpfile in dumpfiles:
            pipeline = import_file(dumpfile)
            pipeline.modifiers.CalculateDisplacementsModifier()
            output = pipeline.compute()

            outfiles = xdist_dir + f"xdist_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}.txt"
            export_file(pipeline, outfiles, "txt", columns=["Timestep", "Displacement.X"], multiple_frames = True)

if __name__ == '__main__':
    asperities = 8
    uc = 5
    temp = 2300
    time = 1800
    initnum = 0

    highz_dir = '../../txt/high_z/'
    max_zs = []
    avg_max = []
    max_z_finder(asperities, uc, temp, time, initnum)
    displacement_x(asperities, uc, temp, time, initnum)
    #plot_max_z(asperities, uc, temp, time, initnum)
