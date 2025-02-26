import numpy as np
from .base import RVFLBase
from sklearn.base import RegressorMixin



class RVFLRegressor(RVFLBase, RegressorMixin):
    """
    RVFL-based regression model extending RVFLBase.
    """

    def __init__(self, in_dim, n_nodes=100, activation='sigmoid', direct_link=True, alpha=None, ridge=True, random_state=None):
        """
        Initializes the RVFLRegressor.

        Args:
            in_dim (int): Input feature dimension.
            n_hidden_units (int): Number of hidden units (default: 100).
            activation (str): Activation function for hidden layer (default: 'relu').
            direct_link (bool): Whether to include direct input-output connection (default: True).
            alpha (float): Regularization strength for Ridge regression.
            ridge (bool): Use Ridge regression if True; else use Moore-Penrose Pseudoinverse.
            random_state (int, optional): Seed for reproducibility.
        """
        if random_state is None:
            self.random_state = np.random.default_rng(213155).integers(0, 2 ** 32)
        elif random_state is int:
            self.random_state = np.random.default_rng(random_state).integers(0, 2 ** 32)
        else:
            self.random_state = random_state
        super().__init__(in_dim=in_dim, n_nodes=n_nodes, activation=activation, direct_link=direct_link, alpha=alpha, ridge=ridge, random_state=random_state)

    def fit(self, X, y, sample_weight=None):
        """Calls base fit function."""
        return super().fit(X, y, sample_weight=sample_weight)

    def predict(self, X):
        """Calls base predict function."""
        return super().predict(X)
