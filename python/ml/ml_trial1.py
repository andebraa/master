import torch
import torch.nn as nn

class conv2d(nn.Module):
    def __init__(self, 
                 imput_shape, 
                 n_kernels=(8,16,32),
                 kernel_sizes=(3,3,3),
                 n_dense = 64, 
                 padding = 1,
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

