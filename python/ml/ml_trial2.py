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


def pp(a, padding):
    b = np.zeros((a.shape[0], a.shape[1] + (padding*2), a.shape[2] + (padding*2)))
    print(a.shape)
    print(b.shape)
    print(len(a[0,:]))
    for i,m in enumerate(a):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                b[i,j,k] = m[(j-padding)%m.shape[0],(k-padding)%m.shape[1]]

    return b


def load_data(padding = 2):
    X = np.load('temp_out_matrix.npy')
    Y = np.load('temp_out_y.npy')

    xtrain, xtest, ytrain, ytest = train_test_split(X,Y, test_size=0.33, 
                                                    random_state = 69)
    
    #add padding
    xtrain = pp(xtrain, padding)
    xtest = pp(xtest, padding)
    print(xtest.shape)
    print(xtrain.shape)
    stop

    xtrain = xtrain.reshape(-1, 4,4, 1)
    xtest = xtest.reshape(-1, 4,4, 1)
    return xtrain, xtest, ytrain, ytest

xtrain, xtest, ytrain, ytest = load_data()

print(xtrain.shape)
print(xtest.shape)

stop

ytrain = to_categorical(ytrain)
ytest = to_categorical(ytest)

model = Sequential()

model.add(Conv2D(64, (3,3), input_shape=(4, 4, 1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(10))
model.add(Activation('softmax'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])

model.fit(train_X, train_Y_one_hot, batch_size=64, epochs=5)
'''
import keras
from keras.datasets import fashion_mnist 
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

(train_X,train_Y), (test_X,test_Y) = fashion_mnist.load_data()

train_X = train_X.reshape(-1, 28,28, 1)
test_X = test_X.reshape(-1, 28,28, 1)

train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X / 255
test_X = test_X / 255

train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)

model = Sequential()

model.add(Conv2D(64, (3,3), input_shape=(28, 28, 1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(10))
model.add(Activation('softmax'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])

model.fit(train_X, train_Y_one_hot, batch_size=64, epochs=5)

test_loss, test_acc = model.evaluate(test_X, test_Y_one_hot)
print('Test loss', test_loss)
print('Test accuracy', test_acc)

predictions = model.predict(test_X)
print(np.argmax(np.round(predictions[0])))

plt.imshow(test_X[0].reshape(28, 28), cmap = plt.cm.binary)
plt.show()

'''


