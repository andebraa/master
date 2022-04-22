import pandas as pd
from ovito.io import *
import re
from ovito.modifiers import *
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def compute_max_z(frame, data):
    data.attributes["High_Z"] = numpy.max(data.particles["Position"][:,2])

def max_z_finder(asperities, uc, temp, time, initnum):

    highz_dir = '../../txt/high_z/'
    max_zs = []
    avg_max = []
    for force in [0, 0.001, 0.01, 0.1]:
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
            export_file(pipeline, outfiles, "txt", columns=["Frame", "High_Z"], multiple_frames = True)
    
def plot_max_z(asperities, uc, temp, time, initnum):
    fig, axs = plt.subplots(2,2)

    axs = axs.ravel()
    for i, force in enumerate([0, 0.001, 0.01, 0.1]):
        heights = []
        files = highz_dir + f"maxz_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*.txt"
        for _file in glob(files):
            print(_file)
            seed = re.findall(r'\d', _file)[-1]
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

            
        avg_max.append(np.mean(heights, axis = 0))
        print(frames, avg_max)
        axs[i].plot(frames, avg_max[0], label = force)
    plt.legend()
    plt.savefig('test.png')
if __name__ == '__main__':
    asperities = 8
    uc = 5
    temp = 2300
    time = 1000
    initnum = 0

    highz_dir = '../../txt/high_z/'
    max_zs = []
    avg_max = []
    #max_z_finder(asperities, uc, temp, time, initnum)
    plot_max_z(asperities, uc, temp, time, initnum)
