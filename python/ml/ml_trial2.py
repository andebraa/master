'''
Attempt at 2d ncc using keras.
https://towardsdatascience.com/mnist-cnn-python-c61a5bce7a19
'''
import keras
from keras.datasets import fashion_mnist 
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
load_data()
