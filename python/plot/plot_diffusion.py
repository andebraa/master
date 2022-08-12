
from numpy import loadtxt, asarray, mean
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from regression import nonlin_reg, multiple_reg

#plt.style.use('seaborn-deep')
plt.rcParams['figure.figsize'] = 7, 9

def plot_diffusion():
    
