import json

with open('system_or100_hi115_errgrid3_3_auxiliary.json' ,'r') as file:
    auxiliary = json.load(file) 

print(auxiliary)

print(auxiliary['lx'] * auxiliary['grid'][0])
