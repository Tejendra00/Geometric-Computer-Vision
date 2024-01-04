import numpy as np

def epipole(flow_x, flow_y, smin, thresh, num_iterations=None):
    """
    Compute the epipole from the flows,
    
    Inputs:
        - flow_x: optical flow on the x-direction - shape: (H, W)
        - flow_y: optical flow on the y-direction - shape: (H, W)
        - smin: confidence of the flow estimates - shape: (H, W)
        - thresh: threshold for confidence - scalar
    	- Ignore num_iterations
    Outputs:
        - ep: epipole - shape: (3,)
    """
    # Logic to compute the points you should use for your estimation
    # We only look at image points above the threshold in our image
    # Due to memory constraints, we cannot use all points on the autograder
    # Hence, we give you valid_idx which are the flattened indices of points
    # to use in the estimation estimation problem 

    H,W= flow_x.shape
    good_idx = np.flatnonzero(smin>thresh)
    permuted_indices = np.random.RandomState(seed=10).permutation(
        good_idx
    )
    valid_idx=permuted_indices[:3000]

    ### STUDENT CODE START - PART 1 ###


    xp = valid_idx % W          # Getting x index of pixels in image frame
    yp = valid_idx // W         # Getting y index of pixels in image frame


    flow_x = flow_x[yp,xp]     # Extracting flow for points satisfying conditions
    flow_y = flow_y[yp,xp]

    xp=xp-W//2               # Centering the corrdinates as while calculating Epipole the image center 
    yp=yp-H//2               #is at (0,0) is in center

    zero_matrix = np.zeros(len(xp))
    one_matrix= np.ones(len(xp))

    Xp=np.column_stack((xp,yp,one_matrix))     # making (xp,yp,1) 

    U=np.column_stack((flow_x,flow_y,zero_matrix))

    # Solve the linear system (ep)T*A = 0 for the epipole
    A = np.cross(Xp, U)                                               
    _, _, V = np.linalg.svd(A,full_matrices=False)
    ep = V[-1]                        
 
    return ep