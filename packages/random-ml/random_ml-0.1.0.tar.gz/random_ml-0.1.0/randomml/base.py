import warnings
import numpy as np
import torch
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import Ridge, RidgeCV
from numpy.linalg import pinv
from typing import Optional, Union, Literal

from .ffnn import FFNN  # Assuming ffnn.py is in the same directory or package


class RVFLBase(BaseEstimator, TransformerMixin):
    """
    Base class for Random Vector Functional Link (RVFL) networks.
    """

    def __init__(
        self,
        in_dim: int,
        n_nodes: int = 100,
        alpha: Optional[Union[float, np.ndarray]] = None,
        ridge: bool = True,
        direct_link: bool = True,
        activation: Literal["sigmoid", "relu", "tanh"] = "sigmoid",
        random_state: int = 23,
    ):
        """
        Initializes the RVFL base model.

        Args:
            in_dim: Input feature dimension.
            n_nodes: Number of enhancement nodes. Defaults to 100.
            alpha: Regularization strength for Ridge regression.
                   If None, alpha will be selected using LOOCV over a log scale.
                   Can be a float for fixed Ridge regularization or an array-like
                   of alphas for RidgeCV. In the case of Moore-Penrose pseudoinverse (ridge=False),
                   alpha is still used as a regularization parameter to improve stability.
                   Defaults to None.
            ridge: Use Ridge regression if True; else use Moore-Penrose Pseudoinverse.
                   Defaults to True.
            direct_link: Whether to include direct input-output connections.
                         Defaults to True.
            activation: Activation function for FFNN. Options are "sigmoid", "relu", "tanh".
                        Defaults to "sigmoid".
            random_state: Seed for reproducibility. Defaults to 23.
        """
        self.in_dim = in_dim
        self.n_nodes = n_nodes
        self.alpha = alpha
        self.ridge = ridge
        self.direct_link = direct_link
        self.activation = activation
        self.random_state = random_state


        self.ffnn = FFNN(in_dim, n_nodes, seed=random_state, activation=activation)
        self.beta = None

        if alpha is None:
            warnings.warn(
                "Alpha is not given, it will be selected using LOOCV from -6 to 6, using 100 values log scale.",
                UserWarning,
            )
            self.alpha = np.logspace(-6, 6, 100)
            self.ridge = True
        elif isinstance(alpha, float):
            if alpha <= 0:
                warnings.warn(
                    "Alpha is non-positive, it will be treated as a fixed regularization parameter.",
                    UserWarning,
                )
            self.alpha = alpha
            self.ridge = True
        else:
            self.alpha = alpha



    def __setattr__(self, key, value):
        """
        Custom attribute setter to:
        1. Store `random_state`.
        2. Ensure FFNN seed and weights are updated when `random_state` changes.
        """
        if key == "random_state":
            self.__dict__[key] = value  # Store random_state
            #
            if hasattr(self, "ffnn") and isinstance(self.ffnn, FFNN):
                self.ffnn.seed = value  # Update FFNN seed
                self.ffnn._initialize_weights(value)  # Reinitialize weights

        else:
            self.__dict__[key] = value  # Default behavior for other attributes


    def _compute_hidden_layer(self, X: np.ndarray) -> np.ndarray:
        """Computes the hidden state using FFNN."""
        X_tensor = torch.tensor(X, dtype=torch.float32)
        return self.ffnn(X_tensor).detach().numpy()

    def _compute_beta(self, H: np.ndarray, y: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> np.ndarray:
        """Computes the output weights (beta) using Ridge or Moore-Penrose."""
        if self.ridge:
            if isinstance(self.alpha, (float, int)):
                ridge_model = Ridge(alpha=self.alpha, fit_intercept=False)
            else:  # Assume self.alpha is array-like for RidgeCV
                ridge_model = RidgeCV(alphas=self.alpha, fit_intercept=False, cv=5) # Added cv=5 for RidgeCV
            ridge_model.fit(H, y, sample_weight=sample_weight)
            return ridge_model.coef_.T
        else:
            # alpha is used as regularization here as well for stability
            return pinv(H + self.alpha * np.eye(H.shape[1])) @ y

    def fit(self, X: np.ndarray, y: np.ndarray, sample_weight: Optional[np.ndarray] = None) -> "RVFLBase":
        """
        Fits the RVFL model.

        Args:
            X: Input features.
            y: Target values.
            sample_weight: Sample weights (for AdaBoost compatibility). Defaults to None.

        Returns:
            self: Returns the fitted estimator.
        """
        H = self._compute_hidden_layer(X)

        # Include direct links if enabled
        H_with_bias = np.hstack((X, H)) if self.direct_link else H

        # Compute output weights (beta)
        self.beta = self._compute_beta(H_with_bias, y, sample_weight)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the target values.

        Args:
            X: Input features.

        Returns:
            Predicted values.
        """
        if self.beta is None:
            raise RuntimeError("The model must be trained before predicting.")

        H = self._compute_hidden_layer(X)
        H_with_bias = np.hstack((X, H)) if self.direct_link else H

        return H_with_bias @ self.beta