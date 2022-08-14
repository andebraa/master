import os 
import json
from json import JSONEncoder
import random
import numpy as np
import itertools 
from tqdm import tqdm
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
def nums2coords(nums=None): 
    #convert tuple of asperity numbers to cordinates
    #(1,3) -> [[1,0],[4,0]] 
    
    mapping = {}
    count = 1
    for y in range(4):
        for x in range(4):
            mapping[count] = (x,y)
            count += 1
    if nums is None:
        return mapping
    else:
        return mapping[nums]

def coords2nums(coord=None):
    '''
    convert coordinates to numbers in matrix
    [[3,0], [0,0]] -> (4,1)
    '''
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
    indx = np.zeros((4*4)) 
    matrix = np.zeros((4,4))
    for item in nums:
        matrix[mapping[item]] = 1
    return matrix

def gen_config_library(store_json = False):
    '''
    Script that generates a csv of all unique 2d boolean matrix, wrt
    periodic boundary conditions in the x and y direction. 
    Only conscidering translational symmetries
    '''
    grid_nums = list(range(1,4*4+1))
    combinations = itertools.combinations(grid_nums, 2)
    _combinations = []
    for i in combinations:
        _combinations.append(i)
    random.shuffle(_combinations)
    combinations = _combinations
    all_comb = set()
    removed_comb = set() 

    nums2coords_map = nums2coords()
    coords2nums_map = {v: k for k, v in nums2coords_map.items()}
    for i in combinations:
        all_comb.add(i)
    indx = [0,1,2,3]
    periodic_directions = [np.array((x,y)) for x in indx for y in indx if not (x==y==0)] 


    for setup in tqdm(all_comb):
        if setup in removed_comb:
            continue #skip iteration if already removed

        orig_coords = []
        for num in setup:
            orig_coords.append(nums2coords_map[num])


        for axis in (None, 0, 1, (0,1)):
            if axis != None:
                flip_coords = np.flip(orig_coords, axis=axis)
            else:
                flip_coords = orig_coords
            for direction in periodic_directions:
                shifted_coords=[]
                shifted_nums = [] 
                for coord in flip_coords:
                    shifted_coords.append(shift(direction, coord))
                for coord in shifted_coords:
                    shifted_nums.append(coords2nums(coord))

                #sort shifted nums, all_comb is always sorted
                shifted_nums.sort()
                shifted_nums = tuple(shifted_nums)
                if shifted_nums == setup:
                    continue 
                removed_comb.add(tuple(shifted_nums)) #can't contain duplicates
        
    res = all_comb.difference(removed_comb)    
    matrix_list = np.zeros((len(res), 4, 4))
    if store_json:
        keys = range(len(res))
        ran_res = random.sample(list(res), k = len(res))
        res_dict = dict(zip(keys, ran_res))
        for key, value in res_dict.items():
            print('key, value ',key, value)
            matrix_list[key,:,:] = nums2matrix(value)
        #np.save('2asp_config_list_test.npy', matrix_list)
        #outdict = {key = res[key] for key in keys} 

    return all_comb.difference(removed_comb)
    
def test_asperity_number():
    matrices = np.load('config_list.npy')     
    for i, matrix in enumerate(matrices):
        assert np.sum(matrix) == 8


def combine_combinations():
    '''
    gen config doesn't always find all systems, but this seems random. 
    attempt to have two different calls to gen_config_library and see
    if we can find any entries that are not shared by the two
    '''
    def fetch_new_system(dat2 = None):
        dat1 = gen_config_library(store_json=False)
        if dat2 is not None:
            while dat1 == dat2:
                dat1=gen_config_library(store_json=False)
        
        #convert numbered asperities to lists of coridnates. these can be shifted
        dat1_coords = []
        for elem in dat1:
            elem_coords = []
            for num in elem:
                elem_coords.append(nums2coords_map[num])
            dat1_coords.append(elem_coords)

        return dat1, dat1_coords

    nums2coords_map = nums2coords()
    coords2nums_map = {v: k for k, v in nums2coords_map.items()}

    dat2, dat2_coords = fetch_new_system()

    indx = [0,1,2,3]
    unique_systems = []
    periodic_directions = [np.array((x,y)) for x in indx for y in indx if not (x==y==0)]
    print(dat2)
    
    while unique_systems == []:
        dat1, dat1_coords = fetch_new_system(dat2)
        #pick out systems which occur in dat1, which are unique from dat 2
        for system in filter(lambda system: system not in dat2_coords, dat1_coords):
            print(system)
            unique = True
            for axis in (None, 0, 1, (0,1)):
                if axis != None:
                    flip_coords = np.flip(system, axis = axis)
                else:
                    flip_coords = system
                for direction in periodic_directions:
                    shifted_coords = []
                    shifted_nums = []
                    for coord in flip_coords:
                        shifted_coords.append(shift(direction, coord))
                    for coord in shifted_coords:
                        shifted_nums.append(coords2nums(coord))
                    if tuple(shifted_nums) in dat2:
                        unique = False 
                        break 
                if not unique:
                    break
            if not unique:
                break
        if unique:
            unique_systems.append(system)

    print('dat1 ', dat1)
    print('dat2 ', dat2)
    unique_nums = []
    for system in unique_systems:
        system_nums =  []
        for coord in system:
            system_nums.append(coords2nums_map[coord])
    print('unique: ', unique_nums)

if __name__ == '__main__':
    #unique_comb = gen_config_library(store_json = True)
    combine_combinations()

    #test_asperity_number()
    #matrix = nums2matrix([1,14])
