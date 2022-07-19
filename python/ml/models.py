import torch
import torch.nn as nn
import torch.nn.functional as F


class dnn(nn.Module):
    def __init__(self, input_shape, n_layers, n_nodes, bias=True, verbose=False):
        super(dnn, self).__init__()
        self.layers = nn.ModuleList([nn.Linear(input_shape, n_nodes, bias=bias)])
        for i in range(n_layers-1):
            self.layers.append(nn.Linear(n_nodes, n_nodes, bias=bias))
        self.layers.append(nn.Linear(n_nodes, 1))

        if verbose:
            print(self)

    def forward(self, x):
        for layer in self.layers:
            x = F.leaky_relu(layer(x))
        return x.view(x.size()[0])


def He_init_DNN(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight)



def He_init_CNN(m):
    if isinstance(m, nn.Linear) or isinstance(m, nn.Conv3d):
        nn.init.kaiming_normal_(m.weight)


class conv2d(nn.Module):
    def __init__(self, input_shape, n_kernels=(8, 16, 32), kernel_sizes=(3, 3, 3), n_dense=64, padding=1, init=None, bias=True, verbose=True):
        super(Conv2D, self).__init__()
        dilation = 1
        self.layers = nn.ModuleList()
        self.layers.append(nn.Conv2d(input_shape[0], n_kernels[0], kernel_sizes[0], padding=padding, bias=bias, dilation=dilation))
        self.layers.append(nn.BatchNorm2d(n_kernels[0]))
        for i in range(1, len(n_kernels)):
            self.layers.append(nn.Conv2d(n_kernels[i-1], n_kernels[i], kernel_sizes[i], padding=padding, bias=bias, dilation=dilation))
            self.layers.append(nn.BatchNorm2d(n_kernels[i]))
        self.layers.append(nn.Flatten())
        dense_inp_shape = self.final_conv_out_shape(input_shape, kernel_sizes, padding, dilation)*n_kernels[-1]
        self.layers.append(nn.Linear(dense_inp_shape, n_dense, bias=bias))
        self.layers.append(nn.Linear(n_dense, 1))

        if init is not None:
            for layer in self.layers:
                if not isinstance(layer, nn.Flatten):
                    init(layer.weight)

        if verbose:
            print(self)

    def final_conv_out_shape(self, input_shape, kernel_sizes, pad, dilation):
        stride = 1
        out_h = input_shape[1]
        out_w = input_shape[2]
        for kernel in kernel_sizes:
            out_h = np.floor((out_h + 2*pad - dilation * (kernel-1) - 1)/stride + 1)
            out_w = np.floor((out_w + 2*pad - dilation * (kernel-1) - 1)/stride + 1)

        return int(out_h*out_w)

    def forward(self, x):
        for layer in self.layers:
            x = F.leaky_relu(layer(x))
        return x.view(x.size()[0])


if __name__ == '__main__':
    pass
