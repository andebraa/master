'''
Useful utilities stolen from alexahs!
https://github.com/alexahs/DeepFacet/blob/ce6f43155387fc6f6b309aa23e911189b0182a7e/deepfacet/models/utils.py
'''
import torch
import sys, os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange, tqdm
import glob
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn

class conv2d(nn.Module):
    def __init__(self, 
                 imput_shape, 
                 n_kernels=(8),
                 kernel_sizes=(3,3),
                 n_dense = 16, 
                 padding = 2,
                 stride = 1,
                 init = None,
                 bias = True,
                 batch_norm = False,
                 dropout = None,
                 verbose = True):
        super(Conv2D, self).__init__()

        self.layers = nn.ModuleList()
        #torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, 
        #                padding=0, dilation=1, groups=1, bias=True, 
        #                padding_mode='zeros', device=None, dtype=None)
        self.layers.append(nn.Conv2d(input_shape[0], n_kernels[0], kernel_sizes[0], padding=padding, bias=bias, dilation=dilation)) 
        self.layers.append(nn.BatchNorm2d(n_kernels[0]))

        for i in range(1, len(n_kernels)):
            self.layers.append(nn.Conv2d(n_kernels[i-1], n_kernels[i], kernel_sizes[i], 
                               padding=padding, bias=bias, dilation=dilation)) 
            
            self.layers.append(nn.BatchNorm2d(n_kernels[i])) 
        
        self.layers.append(nn.Flatten())
       

    def outsize(self, input_shape, kernel_size, padding, dialation, stride):
        Hout = ((input_shape[0] + 2*padding[0] - dialation[0] * (kernel_size[0] -1)-1)/stride[0]) +1 
        Wout = ((input_shape[1] + 2*padding[1] - dialation[1] * (kernel_size[1] -1)-1)/stride[1]) +1 
        return int(Hout*Wout)

    def forward(self, x):
        for layer in self.layers:
            x = F.leaky_relu(layer(x))
        return x.view(x.size()[0])




def get_device(computer="gpu", verbose=False):
    if computer == "gpu":
        if torch.cuda.is_available():
            device = torch.device("cuda:0")
            torch.backends.cudnn.benchmark = True
            if verbose:
                print ('Current cuda device: ', torch.cuda.current_device())
    else:
        device = torch.device("cpu")
        if verbose:
            print ('Current device: cpu')

    return device

def r2_score(pred, true):
    if len(pred) == 1:
        return 0
    mean = np.mean(true)
    SS_res = np.sum((true - pred)**2)
    SS_tot = np.sum((true - mean)**2)
    r2 = (1 - SS_res/SS_tot)
    return r2

def MSE(pred, true):
    squared_err = np.sum((pred - true)**2)/len(pred)
    return squared_err




def train_model(model,device,train_loader,val_loader,epochs,
                criterion,optimizer,scheduler = None,
                save_model_path = None,train_r2_criterion = None,verbose=False):

    if save_model_path is not None:
        if not os.path.exists(save_model_path):
            os.makedirs(save_model_path)

    loss_val_list = []
    loss_train_list = []
    r2_val_list = []
    r2_train_list = []
    if verbose:
        pbar = trange(epochs)
    else:
        pbar = range(epochs)

    best_model_state = None
    best_r2 = np.NINF
    for epoch in pbar:
        cum_loss = 0
        cum_r2 = 0
        num_batch_train = 0
        num_batch_val = 0
        for batch, (X, y) in enumerate(train_loader):
            X, y = X.to(device), y.to(device)

            # Compute prediction error
            pred = model(X)
            loss = criterion(pred, y)
            with torch.set_grad_enabled(False):
                r2 = r2_score(pred.cpu().numpy(), y.cpu().numpy(), False)
                cum_r2 += r2

            # Accumulate errors
            cum_loss += loss.item()
            num_batch_train += 1

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Validation
        cum_loss_val = 0
        cum_r2_val = 0

        if val_loader is not None:
            with torch.set_grad_enabled(False):
                for _batch, (X_val, y_val) in enumerate(val_loader):
                    X_val, y_val = X_val.to(device), y_val.to(device)
                    pred_val = model(X_val)
                    loss_val = criterion(pred_val, y_val)
                    r2_val = r2_score(pred_val.cpu().numpy(), y_val.cpu().numpy(), debug=False)

                    cum_loss_val += loss_val.item()
                    cum_r2_val += r2_val
                    num_batch_val += 1

        if scheduler is not None:
            scheduler.step()

        cum_loss /= num_batch_train
        cum_r2 /= num_batch_train
        if val_loader is not None:
            cum_loss_val /= num_batch_val
            cum_r2_val /= num_batch_val

        loss_train_list.append(cum_loss)
        r2_train_list.append(cum_r2)
        if val_loader is not None:
            loss_val_list.append(cum_loss_val)
            r2_val_list.append(cum_r2_val)

        if train_r2_criterion is not None:
            if cum_r2 <= train_r2_criterion and cum_r2 >= train_r2_criterion-0.1:
                if cum_r2_val > best_r2:
                    best_r2 = cum_r2_val
                    best_model_state = model.state_dict()
                    best_idx = epoch
        elif (cum_r2_val > best_r2):
            best_r2 = cum_r2_val
            best_model_state = model.state_dict()

        if verbose:
            if val_loader is not None:
                pbar_items = {
                    "loss_train": f"{cum_loss:.2e}",
                    "r2_train": f"{cum_r2:.2e}",
                    "loss_val": f"{cum_loss_val:.2e}",
                    "r2_val": f"{cum_r2_val:.2e}"
                }
            else:
                pbar_items = {
                    "loss_train": f"{cum_loss:.2e}",
                    "r2_train": f"{cum_r2:.2e}"
                }
            pbar.set_postfix(pbar_items)

        #save model
        if save_model_path is not None:
            torch.save(model.state_dict(), os.path.join(save_model_path, f"epoch_{epoch}.pth"))

    if verbose:
        print("Loss train:", loss_train_list[-1])
        print("R2 train:", r2_train_list[-1])
        if val_loader is not None:
            print("Loss val:", loss_val_list[-1])
            print("R2 val:", r2_val_list[-1])

    if val_loader is not None:
        history = {
            "loss_train": loss_train_list,
            "loss_val": loss_val_list,
            "r2_train": r2_train_list,
            "r2_val": r2_val_list
        }
    else:
        history = {
            "loss_train": loss_train_list,
            "r2_train": r2_train_list,
        }

    return history, best_model_state

def pp(a, padding): 
    ''' 
    adds periodic boundary padding to matrix 
    ''' 
    newdim = (a.shape[0], a.shape[1] + (padding*2), a.shape[2] + (padding*2)) 
    b = np.zeros((newdim)) 
    for i,m in enumerate(a): 
        for j in range(b.shape[1]): 
            for k in range(b.shape[2]): 
                b[i,j,k] = m[(j-padding)%m.shape[0],(k-padding)%m.shape[1]] 
 
    return b, newdim 
 
 
def load_data(padding = 2): 
    #NOTE, dnn; torch, cnn torch 
    X = np.load('temp_out_matrix.npy') 
    Y = np.load('temp_out_y.npy') 
 
    #shuffle 
    indx = np.arange(0, X.shape[0]) 
    np.random.shuffle(indx) 
 
    X = X[indx] 
    Y = Y[indx] 
 
    xtrain, xtest, ytrain, ytest = train_test_split(X,Y, test_size=0.33, 
                                                    random_state = 69) 
 
    #add padding 
    xtrain, newdim = pp(xtrain, padding) 
    xtest, newdim = pp(xtest, padding) 
 
    xtrain = xtrain.reshape(newdim[0], 1, newdim[1], newdim[2]) #usure  
     
    return xtrain, ytrain, xtest, ytest 

