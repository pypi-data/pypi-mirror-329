import numpy as np
from scipy.optimize import linprog

def get_solution(
        S,
        Phi,
        quantile
):
    S = S.reshape(-1,1)
    Phi = Phi.astype(float)

    zeros = np.zeros((Phi.shape[1],))
    bounds = [(quantile - 1, quantile)] * len(S)
    res = linprog(-1 * S, A_eq=Phi.T, b_eq=zeros, bounds=bounds, method='highs')
    primal_vars = -1 * res.eqlin.marginals.reshape(-1,1)
    dual_vars = res.x.reshape(-1,1)

    return dual_vars, primal_vars

def compute_threshold(
    quantile,
    primals,
    duals,
    phi_calib,
    scores_calib,
    phi_test,
    S_test
):
    def get_current_basis(primals, duals, Phi, S, quantile):
        interp_bools = np.logical_and(
            ~np.isclose(duals, quantile - 1),
            ~np.isclose(duals, quantile)
        )
        if np.sum(interp_bools) == Phi.shape[1]:
            return interp_bools
        preds = -1 * Phi @ primals
        interp_bools = np.isclose(S, preds)
        return interp_bools
    
    dual_threshold = quantile if quantile >= 0.5 else quantile - 1
    
    basis = get_current_basis(primals, duals, phi_calib, scores_calib, quantile)
    S_test = phi_test.T @ primals

    duals = np.concatenate((duals, [0]))
    basis = np.concatenate((basis, [False]))
    phi = np.concatenate((phi_calib, phi_test.reshape(1,-1)), axis=0)
    S = np.concatenate((scores_calib.reshape(-1,1), S_test.reshape(-1,1)), axis=0)

    cur_idx = phi.shape[0] - 1

    while True:
        direction = -1 * np.linalg.solve(phi[basis].T, phi[cur_idx].reshape(-1,1)).flatten()
        active_indices = ~np.isclose(direction, 0)
        active_direction = direction[active_indices]
        active_basis = basis.copy()
        active_basis[np.where(basis)[0][~active_indices]] = False
        positive_step = True if duals[cur_idx] <= 0 else False
        if cur_idx == phi.shape[0] - 1:
            positive_step = True if dual_threshold >= 0 else False

        if positive_step:
            gap_to_bounds = np.maximum(
                (quantile - duals[active_basis]) / active_direction,
                ((quantile - 1) - duals[active_basis]) / active_direction
            )
            step_size = np.min(gap_to_bounds)
            departing_idx = np.where(active_basis)[0][np.argmin(gap_to_bounds)]
        else:
            gap_to_bounds = np.minimum(
                (quantile - duals[active_basis]) / active_direction,
                ((quantile - 1) - duals[active_basis]) / active_direction
            )
            step_size = np.max(gap_to_bounds)
            departing_idx = np.where(active_basis)[0][np.argmax(gap_to_bounds)]
        step_size_clip = np.clip(
            step_size, 
            a_max=quantile - duals[cur_idx], 
            a_min=(quantile - 1) - duals[cur_idx]
        )

        duals[basis] += step_size_clip * direction
        duals[cur_idx] += step_size_clip
        if step_size_clip == step_size:
            basis[departing_idx] = False
            basis[cur_idx] = True
        # print(duals[-1], S[-1])

        if np.isclose(duals[-1], dual_threshold):
            break
        reduced_A = np.linalg.solve(phi[basis].T, phi[~basis].T)
        reduced_costs = (S[~basis].T - S[basis].T @ reduced_A).flatten()
        bottom = reduced_A[-1]
        bottom[np.isclose(bottom, 0)] = np.inf
        req_change = reduced_costs / bottom
        if dual_threshold >= 0:
            ignore_entries = (np.isclose(bottom, 0) | np.asarray(req_change <= 1e-5))  
        else:
            ignore_entries = (np.isclose(bottom, 0) | np.asarray(req_change >= -1e-5))  
        if np.sum(~ignore_entries) == 0:
            S[-1] = np.inf if quantile >= 0.5 else -np.inf
            break
        if dual_threshold >= 0:
            cur_idx = np.where(~basis)[0][np.where(~ignore_entries, req_change, np.inf).argmin()]
            S[-1] += np.min(req_change[~ignore_entries])
        else:
            cur_idx = np.where(~basis)[0][np.where(~ignore_entries, req_change, -np.inf).argmax()]
            S[-1] += np.max(req_change[~ignore_entries])
    threshold = S[-1]
    return threshold