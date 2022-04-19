from ovito.io import *
from ovito.modifiers import *
import numpy

def compute_max_z(frame, data):
    data.attributes["High_Z"] = numpy.max(data.particles["Position"][:,2])

max_zs = []
for force in [0, 0.001, 0.01, 0.1]:
    dumpfiles = f'../../simulations/sys_asp{asperities}_uc{uc}/production/sim_temp{temp}_force{force}_asp{asperities}_time{time}_initnum{initnum}_seed*_errgrid4_4/dump.bin'
    for dumpfile in glob(dumpfiles):

        pipeline = import_file(dumpfile)

        print(pipeline.data.particles['Position'][:,2])
        stop
        #pipeline.modifiers.append(compute_max_z)
        #export_file(pipeline, "max_z.txt", "txt", columns=["Frame", "High_Z"], multiple_frames = True)
