import numpy as np

def est_homography(X, Y):
    """
    Calculates the homography of two planes, from the plane defined by X
    to the plane defined by Y. In this assignment, X are the coordinates of the
    four corners of the soccer goal while Y are the four corners of the penn logo

    Input:
        X: 4x2 matrix of (x,y) coordinates of goal corners in video frame
        Y: 4x2 matrix of (x,y) coordinates of logo corners in penn logo
    Returns:
        H: 3x3 homogeneours transformation matrix s.t. Y ~ H*X

    """

    # ##### STUDENT CODE START #####
    X_ = np.hstack([X, np.ones([X.shape[0],1])])
    
    A = np.zeros([8,9])
    A[0::2, 0:3] = -1 * X_
    A[1::2, 3:6] = -1 * X_
    A[0::2, 6:9] = X_ * Y[:,[0]]
    A[1::2, 6:9] = X_ * Y[:,[1]]
    
    B, C, V = np.linalg.svd(A)
    H = V[-1,:] / V[-1, -1]
    H = np.reshape(H, [3,3])

    ##### STUDENT CODE END #####

    return H