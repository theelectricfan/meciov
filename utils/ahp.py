# utils/ahp.py

import numpy as np

def compute_satisfaction_score(criteria: dict) -> float:
    """
    Uses Analytic Hierarchy Process (AHP) to compute satisfaction score.
    Criteria: {price, ber, retransmissions}
    """
    price, ber, retrans = criteria['price'], criteria['ber'], criteria['retrans']

    M = np.array([
        [1, 5, 9],
        [1/5, 1, 3],
        [1/9, 1/3, 1]
    ])


    eigvals, eigvecs = np.linalg.eig(M)
    max_idx = np.argmax(eigvals)
    weights = eigvecs[:, max_idx].real
    weights /= np.sum(weights)

    norm_criteria = np.array([
        1 / (price + 1e-9),
        1 / (ber + 1e-9),
        1 / (retrans + 1e-9) 
    ])
    norm_criteria /= np.sum(norm_criteria)

    score = np.dot(weights, norm_criteria)
    return score
