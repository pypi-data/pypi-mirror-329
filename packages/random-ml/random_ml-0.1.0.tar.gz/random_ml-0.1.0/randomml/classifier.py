import numpy as np
from sklearn.utils import check_array
from sklearn.utils.multiclass import check_classification_targets

from .base import RVFLBase
from sklearn.base import ClassifierMixin


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils import check_array
from scipy.special import softmax, expit as sigmoid  # expit is the sigmoid function
from randomml.base import RVFLBase

class RVFLClassifier(RVFLBase, ClassifierMixin):
    """
    RVFL-based classification model extending RVFLBase.
    Uses softmax activation for multi-class classification.
    """

    def __init__(self, in_dim, n_nodes=100, activation='sigmoid', direct_link=True, alpha=None, ridge=True, random_state=None):
        """
        Initializes the RVFLClassifier.

        Args:
            in_dim (int): Input feature dimension.
            n_hidden_units (int): Number of hidden units (default: 100).
            activation (str): Activation function for hidden layer (default: 'relu').
            direct_link (bool): Whether to include direct input-output connection (default: True).
            alpha (float): Regularization strength for Ridge regression.
            ridge (bool): Use Ridge regression if True; else use Moore-Penrose Pseudoinverse.
            random_state (int, optional): Seed for reproducibility.
        """

        super().__init__(in_dim=in_dim, n_nodes=n_nodes, activation=activation, direct_link=direct_link, alpha=alpha, ridge=ridge, random_state=random_state)
        self.classes_ = None  # Will be set during `fit()`



    def fit(self, X, y, sample_weight=None):
        """
        Fits the RVFLClassifier.

        Args:
            X (ndarray): Training features.
            y (ndarray): Training labels.
            sample_weight (ndarray, optional): Sample weights (for AdaBoost compatibility).

        Returns:
            self
        """
        check_classification_targets(y)  # Ensure y contains valid class labels
        X = check_array(X, accept_sparse='csr', ensure_2d=True)  # Validate input format
        self.classes_ = np.unique(y)  # Store unique class labels

        return super().fit(X, y, sample_weight=sample_weight)

    def predict_proba(self, X):
        """
        Predicts class probabilities.

        Args:
            X (ndarray): Input features.

        Returns:
            ndarray: Predicted class probabilities.
        """
        raw_outputs = super().predict(X)

        if len(self.classes_) == 2:  # Binary classification
            prob_pos = sigmoid(raw_outputs)
            return np.column_stack([1 - prob_pos, prob_pos])  # [P(class 0), P(class 1)]
        else:  # Multi-class classification
            return softmax(raw_outputs, axis=1)

    def predict(self, X):
        """
        Predicts class labels.

        Args:
            X (ndarray): Input features.

        Returns:
            ndarray: Predicted class labels.
        """
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

