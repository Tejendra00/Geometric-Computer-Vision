from lse import least_squares_estimation
import numpy as np

def ransac_estimator(X1, X2, num_iterations=1000):
    sample_size = 8
    eps = 10**-4
    best_num_inliers = -1
    best_inliers = None
    best_E = None
    e3 = np.array([0, 0, 1])
    hat_e3 = np.cross(np.eye(3), e3)

    for i in range(num_iterations):
        inliers = []
        permuted_indices = np.random.RandomState(seed=(i*10)).permutation(np.arange(X1.shape[0]))
        sample_indices = permuted_indices[:sample_size]
        test_indices = permuted_indices[sample_size:]

        E = least_squares_estimation(X1[sample_indices], X2[sample_indices])

        for j in test_indices:
            dx2 = (np.linalg.norm((X2[j].T) @ E @ X1[j]))**2
            dx2 = dx2 / (np.linalg.norm(hat_e3 @ E @ X1[j])**2)

            dx1 = (np.linalg.norm((X1[j].T) @ E.T @ X2[j]))**2
            dx1 = dx1 / (np.linalg.norm(hat_e3 @ E.T @ X2[j])**2)

            if (dx1 + dx2) < eps:
                inliers.append(int(j))

        if len(inliers) > best_num_inliers:
            best_num_inliers = len(inliers)
            best_E = E
            best_inliers = inliers
            best_inliers=np.array(best_inliers)
            best_inliers = np.append(sample_indices, best_inliers)

    return best_E, best_inliers
