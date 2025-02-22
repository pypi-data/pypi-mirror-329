import numpy as np
import osqp

from scipy.sparse import csc_array
from sklearn.metrics.pairwise import pairwise_kernels


def get_solution(lambda_, K, S, Phi, quantile):                
    radius = 1 / lambda_

    n = Phi.shape[0]
    p = Phi.shape[1]

    C = radius / n

    prob = osqp.OSQP()

    A = np.concatenate((Phi.T, np.eye(n)), axis=0)
    lb = np.concatenate(
        (np.zeros((p,)), 
         C * (quantile - 1) * np.ones((n, )))
    )
    ub = np.concatenate(
        (np.zeros((p,)), 
         C * quantile * np.ones((n, )))
    )
    prob.setup(
        P=csc_array(K), 
        q=-1 * S,
        A=csc_array(A), 
        l=lb,
        u=ub,
        eps_abs=1e-5,
        eps_rel=1e-5
    )

    res = prob.solve()

    dual_vars = res.x.reshape(-1,1)
    primal_vars = res.y[:p].reshape(-1,1)

    return dual_vars, primal_vars

def _get_active_constraints(quantile, duals):
    duals 


def compute_threshold(
    quantile,
    primals,
    duals,
    phi_calib,
    scores_calib,
    phi_test,
    S_test
):
    