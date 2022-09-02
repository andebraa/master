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
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split

def get_device(computer="gpu", verbose=False):
    if computer == "gpu":
        print(torch.cuda.list_gpu_processes())
        print(torch.cuda.device_count())
        if torch.cuda.is_available():
            device = torch.device("cuda:0")
            torch.backends.cudnn.benchmark = True
            if verbose:
                print ('Current cuda device: ', torch.cuda.current_device())
    else:
        device = torch.device("cpu")
        if verbose:
            print ('Current device: cpu')

    print(device)
    return device

def r2_score(pred, true):
    if len(pred) == 1:
        return 0
    mean = np.mean(true)
    SS_res = np.sum((true - pred)**2)
    SS_tot = np.sum((true - mean)**2)
    r2 = (1 - SS_res/SS_tot)
    return r2


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
                r2 = r2_score(pred.cpu().numpy(), y.cpu().numpy())
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
                    r2_val = r2_score(pred_val.cpu().numpy(), y_val.cpu().numpy())

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
 
 
def load_data(padding = 2, method = 'cnn', random = False): 
    
    if random:
        X = np.load('rand_matrix.npy') 
        Y = np.load('rand_y.npy') 
        Y = Y[:,2]

    else:
        X = np.load('out_matrix.npy') 
        Y = np.load('out_y.npy') 
        Y = Y[:,2]
 
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
 
    if method == 'cnn': 
        xtrain = np.expand_dims(xtrain,1)
        xtest = np.expand_dims(xtest,1)
    else:
        xtrain = xtrain.reshape(-1, xtrain.shape[0]).T
        xtest = xtest.reshape(-1 ,xtest.shape[0]).T
    #xtrain = xtrain.reshape(None,newdim[0], newdim[1], newdim[2]) #usure  
     
    return xtrain, ytrain, xtest, ytest 




class CustomDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        input = self.X[idx,:]
        target = self.y[idx]
        return (input, target)

class Result:
    def __init__(self,
                r2_train:float,
                r2_val:float,
                mse_train:float,
                mse_val:float,
                model_params:dict):

        self.r2_train = r2_train
        self.r2_val = r2_val
        self.mse_train = mse_train
        self.mse_val = mse_val
        self.model_params = model_params

    def __lt__(self, other):
        return self.r2_val < other.r2_val

    def __repr__(self):
        return f"{self.__class__.__name__}({self.r2_train=:.5f}, {self.r2_val=:.5f}, {self.mse_train=:.5f}, {self.mse_val=:.5f}, {self.model_params=})"

class FinalResult:
    def __init__(self, r2_test, mse_test, model_params, model_state, true, pred, history):
        self.r2_test = r2_test
        self.mse_test = mse_test
        self.model_params = model_params
        self.model_state = model_state
        self.true = true
        self.pred = pred
        self.history = history

    def __repr__(self):
        return f"{self.__class__.__name__}({self.r2_test=:.5f}, {self.mse_test=:.5f}, {self.model_params=})"

def test_model(model, device, criterion, test_loader, plot_predictions=True, title=None, savefig='testfig.png', verbose=True):
    num_batches = 0
    model.eval()
    true_list = []
    pred_list = []
    with torch.no_grad():
        for batch, (X, y) in enumerate(test_loader):
            X, y = X.to(device), y.to(device)
            pred = model(X)
            true_list.extend(y.cpu().numpy())
            pred_list.extend(pred.cpu().numpy())
            num_batches += 1


    true_list = np.asarray(true_list)
    pred_list = np.asarray(pred_list)

    loss = MSE(pred_list, true_list)
    r2 = r2_score(pred_list, true_list)

    if verbose:
        print(f"{title:10s}: MSE: {loss:.3e}, R2: {r2:.3e}")


    if plot_predictions:
        x0 = np.min(true_list)
        x1 = np.max(true_list)
        y0 = np.min(pred_list)
        y1 = np.max(pred_list)

        fig, ax = plt.subplots(figsize=(8, 8))

        ax.scatter(true_list, pred_list, c="b", alpha=0.5)



        ax.legend()
        if title is not None:
            ax.set_title(f"{title}\nMSE:{loss:.2e}, R2:{r2:.2f}")
        else:
            ax.set_title(f"MSE:{loss:.2e}, R2:{r2:.2f}")

        if savefig is not None:
            plt.savefig(savefig)

    return true_list, pred_list


def MSE(pred, true):
    squared_err = np.sum((pred - true)**2)/len(pred)
    return squared_err


class Result:
    def __init__(self,
                r2_train:float,
                r2_val:float,
                mse_train:float,
                mse_val:float,
                model_params:dict):

        self.r2_train = r2_train
        self.r2_val = r2_val
        self.mse_train = mse_train
        self.mse_val = mse_val
        self.model_params = model_params

    def __lt__(self, other):
        return self.r2_val < other.r2_val

    def __repr__(self):
        return f"{self.__class__.__name__}({self.r2_train=:.5f}, {self.r2_val=:.5f}, {self.mse_train=:.5f}, {self.mse_val=:.5f}, {self.model_params=})"

class FinalResult:
    def __init__(self, r2_test, mse_test, model_params, model_state, true, pred, history):
        self.r2_test = r2_test
        self.mse_test = mse_test
        self.model_params = model_params
        self.model_state = model_state
        self.true = true
        self.pred = pred
        self.history = history

    def __repr__(self):
        return f"{self.__class__.__name__}({self.r2_test=:.5f}, {self.mse_test=:.5f}, {self.model_params=})"

