# Import core modules
from .base import RVFLBase
from .regressor import RVFLRegressor
from .classifier import  RVFLClassifier
from .ensemble import RVFLBaggingRegressor, RVFLBaggingClassifier, RVFLBoostingRegressor, RVFLBoostingClassifier
from .mlpedrvfl import MLPedRVFL


# Package metadata
__version__ = "0.1.0"
__author__ = "Rahul Goswami"
__license__ = "MIT"

# Define what gets imported when using `from random_ml import *`
__all__ = [
    "RVFLBase",
    "RVFLRegressor",
    "RVFLClassifier",
    "RVFLBaggingRegressor",
    "RVFLBaggingClassifier",
    "RVFLBoostingRegressor",
    "RVFLBoostingClassifier",
    "MLPedRVFL",
]
