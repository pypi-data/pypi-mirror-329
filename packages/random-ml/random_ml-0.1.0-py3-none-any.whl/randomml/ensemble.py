import numpy as np
from sklearn.ensemble import BaggingRegressor, BaggingClassifier, AdaBoostRegressor, AdaBoostClassifier
from randomml.regressor import RVFLRegressor
from randomml.classifier import RVFLClassifier

class RVFLBaggingRegressor:
    """
    Bagging-based ensemble of RVFLRegressor using sklearn's BaggingRegressor.
    """

    def __init__(self, in_dim, rvfl_kwargs=None, n_estimators=10, random_state=None):
        """
        Initializes the Bagging-based RVFLRegressor.

        Args:
            in_dim (int): Input feature dimension.
            rvfl_kwargs (dict, optional): Keyword arguments for RVFLRegressor.
            n_estimators (int): Number of base learners.
            random_state (int, optional): Random seed for reproducibility.
        """
        rvfl_kwargs = rvfl_kwargs or {}
        base_estimator = RVFLRegressor(in_dim=in_dim, **rvfl_kwargs)

        self.model = BaggingRegressor(
            estimator=base_estimator,
            n_estimators=n_estimators,
            random_state=random_state
        )

    def fit(self, X, y):
        """Fits the Bagging RVFLRegressor."""
        self.model.fit(X, y)
        return self

    def predict(self, X):
        """Predicts using the ensemble model."""
        return self.model.predict(X)


class RVFLBaggingClassifier:
    """
    Bagging-based ensemble of RVFLClassifier using sklearn's BaggingClassifier.
    """

    def __init__(self, in_dim, rvfl_kwargs=None, n_estimators=10, random_state=None):
        """
        Initializes the Bagging-based RVFLClassifier.

        Args:
            in_dim (int): Input feature dimension.
            rvfl_kwargs (dict, optional): Keyword arguments for RVFLClassifier.
            n_estimators (int): Number of base learners.
            random_state (int, optional): Random seed for reproducibility.
        """
        rvfl_kwargs = rvfl_kwargs or {'random_state': random_state}
        base_estimator = RVFLClassifier(in_dim=in_dim, **rvfl_kwargs)


        self.model = BaggingClassifier(
            estimator=base_estimator,
            n_estimators=n_estimators,
            random_state=random_state
        )

    def fit(self, X, y):
        """Fits the Bagging RVFLClassifier."""
        self.model.fit(X, y)
        return self

    def predict(self, X):
        """Predicts using the ensemble model."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predicts class probabilities."""
        return self.model.predict_proba(X)


class RVFLBoostingRegressor:
    """
    Boosting-based ensemble of RVFLRegressor using sklearn's AdaBoostRegressor.
    """

    def __init__(self, in_dim, rvfl_kwargs=None, n_estimators=50, learning_rate=1.0, random_state=None):
        """
        Initializes the Boosting-based RVFLRegressor.

        Args:
            in_dim (int): Input feature dimension.
            rvfl_kwargs (dict, optional): Keyword arguments for RVFLRegressor.
            n_estimators (int): Number of boosting iterations.
            learning_rate (float): Learning rate for boosting.
            random_state (int, optional): Random seed for reproducibility.
        """
        rvfl_kwargs = rvfl_kwargs or {}
        base_estimator = RVFLRegressor(in_dim=in_dim, **rvfl_kwargs)

        self.model = AdaBoostRegressor(
            estimator=base_estimator,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state
        )

    def fit(self, X, y, sample_weight=None):
        """Fits the Boosting RVFLRegressor."""
        self.model.fit(X, y, sample_weight=sample_weight)
        return self

    def predict(self, X):
        """Predicts using the ensemble model."""
        return self.model.predict(X)


class RVFLBoostingClassifier:
    """
    Boosting-based ensemble of RVFLClassifier using sklearn's AdaBoostClassifier.
    """

    def __init__(self, in_dim, rvfl_kwargs=None, n_estimators=50, learning_rate=1.0, random_state=None):
        """
        Initializes the Boosting-based RVFLClassifier.

        Args:
            in_dim (int): Input feature dimension.
            rvfl_kwargs (dict, optional): Keyword arguments for RVFLClassifier.
            n_estimators (int): Number of boosting iterations.
            learning_rate (float): Learning rate for boosting.
            random_state (int, optional): Random seed for reproducibility.
        """
        rvfl_kwargs = rvfl_kwargs or {}
        base_estimator = RVFLClassifier(in_dim=in_dim, **rvfl_kwargs)

        self.model = AdaBoostClassifier(
            estimator=base_estimator,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state
        )

    def fit(self, X, y, sample_weight=None):
        """Fits the Boosting RVFLClassifier."""
        self.model.fit(X, y, sample_weight=sample_weight)
        return self

    def predict(self, X):
        """Predicts using the ensemble model."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predicts class probabilities."""
        return self.model.predict_proba(X)
