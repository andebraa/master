import torch
import torch.nn as nn

class conv2d(nn.Module):
    def __init__(self, 
                 imput_shape, 
                 n_kernels=(8,16,32),
                 n_dense = 64, 
                 padding = 1,
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
        self.layers.append(nn.Conv2d(input_shape[0], 

