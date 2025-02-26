import torch
from torch import nn
import torch.nn.init as init
import numpy as np

class FFNN(nn.Module):
    """
    A Random Fixed Feedforward Neural Network (for hidden state generation).
    Supports configurable activation functions.
    """

    def __init__(self, in_dim, out_dim, seed = 23,
                 weight_init="uniform",
                 activation="relu",
                 mean=0.0, std=1,
                 a=0, b=1,
                 ffnn = None):
        """
        Initializes the FFNN with randomized fixed weights.

        Args:
            in_dim (int): Input feature dimension.
            out_dim (int): Output feature dimension.
            seed (int): Random seed.
            weight_init (str): Weight initialization method.
                              Options: "normal", "uniform", "xavier_uniform", "kaiming_normal", "orthogonal".
                              Default: "normal".
            activation (str): Activation function to use. Options: "relu", "sigmoid", "tanh", "leaky_relu", "sin".
                              Default: "relu".
            mean (float): Mean for normal initialization.
            std (float): Std deviation for normal initialization.
            a (float): Lower bound for uniform initialization.
            b (float): Upper bound for uniform initialization.
        """
        super(FFNN, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.weight_init = weight_init.lower()
        self.activation = activation.lower()
        self.mean = mean
        self.std = std
        self.a = a
        self.b = b
        if seed is None:
            seed = np.random.default_rng().integers(0, 2 ** 8)
        elif seed is int:
            seed= np.random.default_rng(seed).integers(0, 2 ** 8)
        elif seed is np.random.Generator:
            seed = seed.integer(0, 2 ** 32)
        else:
            ValueError("Seed must be an integer or numpy.random.Generator")

        if ffnn is not None:
            self.ffnn = ffnn
        else:
            self.ffnn = nn.Linear(in_dim, out_dim)
        self._initialize_weights(seed)



    def _initialize_weights(self, seed = 23):
        """Applies the specified weight initialization method."""
        genrator = torch.Generator()
        genrator.manual_seed(int(seed))

        if self.weight_init == "normal":
            init.normal_(self.ffnn.weight, mean=self.mean, std=self.std, generator = genrator)
        elif self.weight_init == "uniform":
            init.uniform_(self.ffnn.weight, a=self.a, b=self.b, generator = genrator)
        elif self.weight_init == "xavier_uniform":
            init.xavier_uniform_(self.ffnn.weight, generator = genrator)
        elif self.weight_init == "kaiming_normal":
            init.kaiming_normal_(self.ffnn.weight, generator = genrator)
        elif self.weight_init == "orthogonal":
            init.orthogonal_(self.ffnn.weight, generator = genrator)
        else:
            raise ValueError(f"Unknown weight initialization: {self.weight_init}")

        init.zeros_(self.ffnn.bias)

    def forward(self, x):
        """Forward pass through the FFNN with the selected activation function."""
        x = self.ffnn(x)

        if self.activation == "relu":
            return torch.relu(x)
        elif self.activation == "sigmoid":
            return torch.sigmoid(x)
        elif self.activation == "tanh":
            return torch.tanh(x)
        elif self.activation == "leaky_relu":
            return torch.nn.functional.leaky_relu(x, negative_slope=0.01)
        elif self.activation == "sin":
            return torch.sin(x)
        else:
            raise ValueError(f"Unknown activation function: {self.activation}")
