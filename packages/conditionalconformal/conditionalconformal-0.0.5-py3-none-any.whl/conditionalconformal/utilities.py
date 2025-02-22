import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels

def get_kernel_matrix(x, **kwargs):
    K = pairwise_kernels(
        X=x,
        **kwargs
    ) + 1e-5 * np.eye(len(x))

    K_chol = np.linalg.cholesky(K)
    return K, K_chol