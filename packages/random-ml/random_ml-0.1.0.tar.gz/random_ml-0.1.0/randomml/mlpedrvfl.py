import numpy as np
import torch
from torch import nn
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from .ffnn import FFNN  # Hidden state generator

class MLPedRVFL(BaseEstimator, RegressorMixin):
    """
    MLPedRVFL: Combines edRVFL-style embedding layers with MLP intermediate layer features.
    """

    def __init__(self,
                 in_dim,
                 alpha=0.1,
                 n_nodes=100,
                 n_layers=1,
                 activation="relu",
                 direct_link=True, 
                 aggregate="mean",
                 random_state=42):
        """
        Initializes the MLPedRVFL model.

        Args:
            in_dim (int): Input feature dimension.
            alpha (float): Ridge regression regularization strength.
            n_nodes (int): Number of nodes per hidden layer.
            n_layers (int): Number of hidden layers.
            activation (str): Activation function for FFNN layers.
            direct_link (bool): Whether to use direct input-output connection.
            aggregate (str): Aggregation method for predictions. Options: "mean", "median".
            random_state (int): Random seed for reproducibility.
        """
        self.in_dim = in_dim
        self.n_nodes = n_nodes
        self.alpha = alpha
        self.n_layers = n_layers
        self.activation = activation
        self.direct_link = direct_link
        self.aggregate = aggregate.lower()
        if random_state is None:
            self.random_state = np.random.default_rng(213155).integers(0, 2 ** 32)
        elif random_state is int:
            self.random_state = np.random.default_rng(random_state).integers(0, 2 ** 32)
        else:
            self.random_state = random_state

        if n_layers < 1:
            raise ValueError("Number of layers should be at least 1")
        if self.aggregate not in ["mean", "median"]:
            raise ValueError("aggregate must be either 'mean' or 'median'")

        # Define FFNN layers
        layers_nodes_in = [in_dim] + [n_nodes + in_dim for _ in range(n_layers)]
        layers_nodes_out = [n_nodes for _ in range(n_layers + 1)]

        self.kan = nn.ModuleList(
            [FFNN(layers_nodes_in[i], layers_nodes_out[i],seed = self.random_state + i, activation=activation)
             for i in range(n_layers + 1)]
        )

        # MLP model with `n_layers` hidden layers
        self.mlp = MLPRegressor(
            hidden_layer_sizes=(n_nodes,) * n_layers,
            random_state=self.random_state,
            activation='relu',
            solver='adam',
        )


    def fit(self, X, y, sample_weight=None):
        """
        Fits the MLPedRVFL model.

        Args:
            X (ndarray): Training features.
            y (ndarray): Training target.
            sample_weight (ndarray, optional): Sample weights (for AdaBoost compatibility).

        Returns:
            self
        """
        X, y = np.array(X), np.array(y)

        # Fit the MLP model first
        self.mlp.fit(X, y)
        intermediates, mlp_out = self._mlp_forward_intermediate(X)

        prev = X
        self.rvfl = []

        for i in range(len(self.kan)):
            # Compute FFNN hidden state
            x_embed = self.kan[i](torch.tensor(prev).float()).detach().numpy()

            # Include direct links if enabled
            prev_embed = np.concatenate((prev, x_embed), axis=1) if self.direct_link else x_embed

            # Add MLP features
            mlp_feature = intermediates[i] if i < self.n_layers else mlp_out.reshape(-1, 1)
            feat_for_ridge = np.concatenate((prev_embed, mlp_feature), axis=1)

            # Train Ridge Regression (supports sample_weight for boosting)
            ridge = Ridge(alpha=self.alpha)
            ridge.fit(feat_for_ridge, y, sample_weight=sample_weight)
            self.rvfl.append(ridge)

            prev = np.concatenate((X, x_embed), axis=1)

        return self

    def predict(self, X):
        """
        Predicts target values.

        Args:
            X (ndarray): Input features.

        Returns:
            ndarray: Aggregated predictions (either mean or median).
        """
        X = np.array(X)
        intermediates, mlp_out = self._mlp_forward_intermediate(X)
        prev = X
        pred = np.zeros((X.shape[0], len(self.rvfl)))

        for i in range(len(self.rvfl)):
            # Compute FFNN hidden state
            x_embed = self.kan[i](torch.tensor(prev).float()).detach().numpy()

            # Include direct links if enabled
            prev_embed = np.concatenate((prev, x_embed), axis=1) if self.direct_link else x_embed

            # Add MLP features
            mlp_feature = intermediates[i] if i < self.n_layers else mlp_out.reshape(-1, 1)
            feat_for_ridge = np.concatenate((prev_embed, mlp_feature), axis=1)

            # Predict using trained Ridge model
            pred[:, i] = self.rvfl[i].predict(feat_for_ridge).ravel()
            prev = np.concatenate((X, x_embed), axis=1)

        if self.aggregate == "mean":
            return pred.mean(axis=1)
        else:  # "median"
            return np.median(pred, axis=1)

    def _mlp_forward_intermediate(self, X):
        """
        Computes forward pass through MLPRegressor to get intermediate layer activations.

        Args:
            X (ndarray): Input data.

        Returns:
            tuple: (List of intermediate layer activations, Final output layer value)
        """
        A = X
        intermediates = []

        for i in range(len(self.mlp.coefs_) - 1):
            A = A @ self.mlp.coefs_[i] + self.mlp.intercepts_[i]
            A = np.maximum(A, 0)  # ReLU activation
            intermediates.append(A)

        out = A @ self.mlp.coefs_[-1] + self.mlp.intercepts_[-1]
        return intermediates, out

