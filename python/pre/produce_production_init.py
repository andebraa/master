import numpy as np
import json 
from setup_system import setup_system

with open('config_library.json') as json_file:
    configjson = json.load(json_file)

print(configjson)

for num in configjson.keys():
    setup_system(configjson[num])
    stop
