'''
Attempt at 2d ncc using keras.
https://towardsdatascience.com/mnist-cnn-python-c61a5bce7a19
'''
import keras
from keras.datasets import fashion_mnist 
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    X = np.load('temp_out_matrix.npy')
    Y = np.load('temp_out_y.npy')

    xtrain, xtest, ytrain, ytest = train_test_split(X,Y, test_size=0.33, 
                                                    random_state = 69)
    print(xtrain)
    print('øøøøøøøøøøøøøøøøøøøøøøøøøø')
    print(xtest)
    print(ytrain)
    print(ytest)
    return xtrain, xtest, ytrain, ytest

load_data()

