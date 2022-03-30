import os 
import json
import random
import numpy as np
import itertools 
from tqdm import tqdm
def nums2coords(nums=None): 
    #convert tuple of asperity numbers to cordinates
    #(1,3) -> [[1,0],[1,0]] 
    
    mapping = {}
    count = 1
    for y in range(4):
        for x in range(4):
            mapping[count] = (x,y)
            count += 1
    print('mapping')
    print(mapping)
    if nums is None:
        return mapping
    else:
        return mapping[nums]

def coords2nums(coord=None):
    nums = {}
    count = 1
    for y in range(4):
        for x in range(4):
            nums[(x,y)] = count
            count+=1
    if coord is None:
        return coord
    else:
        return nums[coord]

def shift(direction, p):
    #shift point p one step in direction (x,y)
    i,j = direction
    n = 4
    return ((p[0] +i)%n, (p[1] + j)%n) 

def nums2matrix(nums):
    mapping = nums2coords()
    print(nums)
    print('mapping ',mapping)
    indx = np.zeros((4*4)) 
    matrix = np.zeros((4,4))
    for item in nums:
        print('num: ', item)
        print('map of item: ', mapping[item])
        matrix[mapping[item]] = 1
        indx[item] = 1 
    print(matrix)
    return matrix

def gen_config_library(store_json = False):
    '''
    Script that generates a csv of all unique 2d boolean matrix, wrt
    periodic boundary conditions in the x and y direction. 
    Only conscidering translational symmetries
    '''
    grid_nums = list(range(1,4*4+1))
    combinations = itertools.combinations(grid_nums, 8)
    print('here')
    all_comb = set()
    removed_comb = set() 

    nums2coords_map = nums2coords()
    coords2nums_map = {v: k for k, v in nums2coords_map.items()}
    #print('num2coords map ', nums2coords_map)
    #print('coords2nums map ', coords2nums_map)
    test = set()
    for i in combinations:
        #print(i)
        all_comb.add(i)

    print(len(all_comb))
    indx = [0,1,2,3]
    periodic_directions = [np.array((x,y)) for x in indx for y in indx if not (x==y==0)] 
    for setup in tqdm(all_comb):
        if setup in removed_comb:
            continue #skip iteration if already removed
        
        orig_coords = []
        for num in setup:
            orig_coords.append(nums2coords_map[num])
            

        for axis in (None, 0,1):
            if axis != None:
                orig_coords = np.flip(orig_coords, axis=axis)
            for direction in periodic_directions:
                shifted_coords=[]
                shifted_nums = [] 

                #for i in range(4):
                #    for j in range(2):
                #        shifted_coords.append(np.roll(orig_coords, i, axis=j))
                for coord in orig_coords:
                    shifted_coords.append(shift(direction, coord))
                for coord in shifted_coords:
                    shifted_nums.append(coords2nums(coord))

                #sort shifted nums, all_comb is always sorted
                shifted_nums.sort()

                removed_comb.add(tuple(shifted_nums)) #can't contain duplicates
        
        for axis in (0,1):
            flipped_coords = []
            flipped_nums = [] 

    res = all_comb.difference(removed_comb)    
    if store_json:
        keys = range(len(res))
        ran_res = random.sample(list(res), k = len(res))
        print(len(ran_res))
        res_dict = dict(zip(keys, ran_res))
        print('res_dict ', res_dict)
        print(len(res_dict))
        print(len(ran_res))
        with open('config_library.json', 'w') as fp:
            json.dump(res_dict, fp)
        #outdict = {key = res[key] for key in keys} 

    return all_comb.difference(removed_comb)
    

if __name__ == '__main__':
    unique_comb = gen_config_library(store_json = True)
    #matrix = nums2matrix([1,14])
