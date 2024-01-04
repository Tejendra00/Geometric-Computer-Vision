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

    ##### STUDENT CODE START #####
    A=[]                            #Generating an emtpty list to assign values later
    for i in range(4):
            Xx= X[i,0]              # Taking one x,y coordinates in each loop
            Xy= X[i,1]              # for both goal and logo
            Yx= Y[i,0]
            Yy=Y [i,1]
            ax= [-Xx, -Xy, -1, 0, 0, 0, Xx*Yx , Xy*Yx, Yx]     # Using already derived equation fot finding H.
            ay =[ 0, 0, 0, -Xx, -Xy, -1, Xx*Yy, Xy*Yy, Yy]
            A.append(ax)
            A.append(ay)
    A=np.array(A)                    # Converting list to array to resolve any ambiguity when matrix multipication.

    U, S ,VT= np.linalg.svd(A)       # SVD with VT- V Transpose.

    V=np.transpose(VT)
    h = V[:,-1]                      # Take the last column of V
    H=np.reshape(h,(3,3))            # Making H from 9x1 - 3x3 matrix

    ##### STUDENT CODE END #####

    return H
