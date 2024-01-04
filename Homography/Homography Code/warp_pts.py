import numpy as np
from est_homography import est_homography


def warp_pts(X, Y, interior_pts):
    """
    First compute homography from video_pts to logo_pts using X and Y,
    and then use this homography to warp all points inside the soccer goal

    Input:
        X: 4x2 matrix of (x,y) coordinates of goal corners in video frame
        Y: 4x2 matrix of (x,y) coordinates of logo corners in penn logo
        interior_pts: Nx2 matrix of points inside goal
    Returns:
        warped_pts: Nx2 matrix containing new coordinates for interior_pts.
        These coordinate describe where a point inside the goal will be warped
        to inside the penn logo. For this assignment, you can keep these new
        coordinates as float numbers.

    """

    # You should Complete est_homography first!
    H = est_homography(X, Y)

    warped_pts=np.zeros((interior_pts.shape[0], 2),dtype=float)     # Generating zero array of size of Nx2

    for i in range(interior_pts.shape[0]):

        X_goal= interior_pts[i,0]                                   # Take each x,y of interior goal.
        Y_goal= interior_pts[i,1]

        goal_matrix= np.array([X_goal, Y_goal ,1])                  # Making Homogenous matrix
        warped_matrix= np.dot(H, goal_matrix)                       # Y ~ H.X

        warped_matrix= warped_matrix/warped_matrix[2]               # Normalizing the Mtarix.

        warped_pts[i, 0] = warped_matrix[0]                         # Assigning the values.
        warped_pts[i, 1] = warped_matrix[1]

    ##### STUDENT CODE END #####

    return warped_pts
