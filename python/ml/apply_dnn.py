from sklearn.model_selection import KFold, train_test_split
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import utils
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
import itertools as it
from tqdm import trange
from dataclasses import dataclass
from typing import OrderedDict
from apply_cnn import *
from models import *

        

class GridSearchDNN(GridSearch):
    def __init__(self, search_params, model_cls, train_func, device, mode):
        super().__init__(search_params, model_cls, train_func, device, mode)

    def _fit(self, params, X, y, epochs, kfold_splits):

        batch_size = params.get("batch_size") or 32
        learning_rate = params.get("learning_rate") or 1e-5
        model_params = {
            "input_shape": X[0].shape[0],
            "n_layers": params["n_layers"],
            "n_nodes": params["n_nodes"],
            "bias": params["bias"]
        }

        count = 0
        r2_scores = []

        best_train_loader = None
        best_val_loader = None
        r2_local_best = np.NINF
        mse_local_best = np.Inf

        best_model_state = None
        best_history = None


        metrics = {
            "r2_train": [],
            "r2_val": [],
            "mse_train": [],
            "mse_val": []
        }


        for train_idx, val_idx in KFold(n_splits=kfold_splits, random_state=0, shuffle=True).split(X):

            data_train = utils.CustomDataset(X[train_idx], y[train_idx])
            data_val = utils.CustomDataset(X[val_idx], y[val_idx])

            train_loader = DataLoader(data_train, batch_size=batch_size, shuffle=False)
            val_loader = DataLoader(data_val, batch_size=batch_size, shuffle=False)

            model = self.model_cls(**model_params, verbose=False).to(self.device)
            model.apply(He_init_DNN)

            optimizer = optim.Adam(model.parameters(), lr=learning_rate)

            train_model_params = {
                "model": model,
                "device": self.device,
                "train_loader": train_loader,
                "val_loader": val_loader,
                "epochs": epochs,
                "criterion": self.criterion,
                "optimizer": optimizer,
                "save_model_path": None
            }

            history, model_state = self.train_model(**train_model_params)

            true_train, pred_train = utils.test_model(model, self.device, self.criterion, train_loader, plot_predictions=False, verbose=False, title="train")
            true_val, pred_val = utils.test_model(model, self.device, self.criterion, val_loader, plot_predictions=False, verbose=False, title="val")

            r2_train = utils.r2_score(pred_train, true_train)
            r2_val = utils.r2_score(pred_val, true_val)

            mse_train = utils.MSE(pred_train, true_train)
            mse_val = utils.MSE(pred_val, true_val)

            metrics["r2_train"].append(r2_train)
            metrics["r2_val"].append(r2_val)
            metrics["mse_train"].append(mse_train)
            metrics["mse_val"].append(mse_val)

            if self.mode == "r2":
                if r2_val > r2_local_best:
                    best_model_state = model_state
                    best_history = history
                    r2_local_best = r2_val
                    mse_local_best = mse_val
            elif self.mode == "mse":
                if mse_val < mse_local_best:
                    best_model_state = model_state
                    best_history = history
                    mse_local_best = mse_val
                    r2_local_best = r2_val

        mean_r2 = np.mean(metrics["r2_val"])
        mean_mse = np.mean(metrics["mse_val"])

        results = {
            "model": model,
            "model_state": best_model_state,
            "r2_val": np.mean(metrics["r2_val"]),
            "mse_val": np.mean(metrics["mse_val"]),
            "r2_train": np.mean(metrics["r2_train"]),
            "mse_train": np.mean(metrics["mse_train"]),
            "history": best_history
        }

        return results


def run_dnn_search(epochs, mode):

    random = True
    padding = 1
    X_CV, y_CV, X_test, y_test = utils.load_data(padding, method = 'dnn', random = random) #X_CV, y_CV, X_test, y_test
    device = utils.get_device("cpu", verbose = True)

    n_nodes_list = 2**np.arange(2, 9) # 4 - 1024 nodes
    n_layers_list = 2**np.arange(2, 9) # 2 - 128 layers

    search_params = {
        "n_nodes": n_nodes_list,
        "n_layers": n_layers_list,
        "learning_rate": [1e-3, 1e-4, 1e-5],
        "batch_size": [32, 64],
        "bias": [1, 2]
    }

    splits = 5

    gridsearch = GridSearchDNN(search_params, dnn, utils.train_model, device, mode = mode)
    best_inds, best_instance_vars, final_params, results = gridsearch.fit(X_CV, y_CV, epochs, splits, verbose=True)

    model = best_instance_vars["model"]
    test_loader = DataLoader(utils.CustomDataset(X_test, y_test))
    history = best_instance_vars["history"]
    test_true, test_pred = utils.test_model(model, device, nn.MSELoss, test_loader, title="test")
    r2_test = utils.r2_score(test_pred, test_true)
    mse_test = utils.MSE(test_pred, test_true)

    final_state = best_instance_vars["model_state"]
    print(f"{r2_test=}")
    print(f"{mse_test=}")
    print(f"{best_inds=}")
    print(f"{final_params=}")

    final_result = utils.FinalResult(r2_test, mse_test, final_params, final_state, test_true, test_pred, history)
    results = list(results)
    results.insert(0, final_result)

    seed = np.random.randint(10000, 100000)
    if random:
        outname = f"CV_results/scores_dnn_{mode}_epochs{epochs}_pad{padding}_splits{splits}_{seed}_sigmax_random.npz"
    else:
        outname = f"CV_results/scores_dnn_{mode}_epochs{epochs}_pad{padding}_splits{splits}_{seed}_sigmax.npz"
    if os.path.exists(outname):
        print(f"WARNING: {outname} exists. Exiting..")
        return
    else:
        print(f"running search, saving to {outname}")

    np.savez(outname, results, allow_pickle=True)
    print(f"wrote {outname}")


def main():
    epochs = 400
    mode = 'mse'

    run_dnn_search(epochs=epochs, mode=mode)

if __name__ == '__main__':
    main()
