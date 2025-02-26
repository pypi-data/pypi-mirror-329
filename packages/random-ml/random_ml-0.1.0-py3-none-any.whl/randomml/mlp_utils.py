import numpy as np


def mlp_forward_intermediate(mlp, X):
    """
    Computes the forward pass through the trained MLPRegressor to obtain:
    - intermediate layer activations
    - final output layer values

    Args:
        mlp (MLPRegressor): A trained MLPRegressor instance.
        X (ndarray): Input data array.

    Returns:
        tuple: (list of intermediate layer activations, final output layer values)
    """
    A = X
    intermediates = []

    # Process hidden layers
    for i in range(len(mlp.coefs_) - 1):
        A = A @ mlp.coefs_[i] + mlp.intercepts_[i]
        A = np.maximum(A, 0)  # ReLU activation
        intermediates.append(A)

    # Process output layer
    out = A @ mlp.coefs_[-1] + mlp.intercepts_[-1]

    return intermediates, out
