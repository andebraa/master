import numpy as np
from datetime import datetime
import json
from json import JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    """
    class from https://pynative.com/python-serialize-numpy-ndarray-into-json/
    attempt to fix json type files not accepting arrays
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self,obj)

def runlogger(runtype, uc, temp, vel, force, runtime, relax_seed,grid = 'erratic', push_seed = 0, asperities=8, orientation = 100):
    curr_time = datetime.now()
    
    elems = {'time': curr_time.strftime('%Y-%m-%d %H:%M:%S'), 'runtype': runtype, 'uc': uc, 'temp': temp,
            'vel': vel, 'force': force, 'runtime':runtime, 'relax_seed': relax_seed, 'push_seed': push_seed, 
            'asperities': asperities, 'orientation': orientation}

    with open(r'/home/users/andebraa/master/python/runlog.csv', 'a') as f:
        json.dump(elems, f, cls=NumpyArrayEncoder)
if __name__ == '__main__':
    runlogger('push', 1, 2300, 5, 0.001, 50000, 42069)
