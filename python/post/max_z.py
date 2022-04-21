from ovito.io import *
import re
from ovito.modifiers import *
import numpy
from glob import glob

def compute_max_z(frame, data):
    data.attributes["High_Z"] = numpy.max(data.particles["Position"][:,2])

def max_z_finder():
    asperities = 8
    uc = 5
    temp = 2300
    time = 1000
    initnum = 0

    highz_dir = '../../txt/high_z/'
    max_zs = []
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
            export_file(pipeline, highz_dir + "maxz_temp{temperature}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed{seed}.txt", "txt", columns=["Frame", "High_Z"], multiple_frames = True)
if __name__ == '__main__':
    max_z_finder()
