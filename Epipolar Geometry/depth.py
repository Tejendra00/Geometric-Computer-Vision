import numpy as np

def depth(flow, confidence, ep, K, thres=2):
    """
    Compute the depth map from the flow and confidence map.
    
    Inputs:
        - flow: optical flow - shape: (H, W, 2)
        - confidence: confidence of the flow estimates - shape: (H, W)
        - ep: epipole - shape: (3,)
        - K: intrinsic calibration matrix - shape: (3, 3)
        - thres: threshold for confidence (optional) - scalar
    
    Output:
        - depth_map: depth at every pixel - shape: (H, W)
    """

    ### STUDENT CODE START ###
    
    # 1. Find where flow is valid (confidence > threshold)
    # 2. Convert these pixel locations to normalized projective coordinates
    # 3. Same for epipole and flow vectors
    # 4. Now find the depths using the formula from the lecture slides

    depth_map = np.zeros_like(confidence)

    flow_x=flow[..., 0]   # Extracting U from flow matrix

    flow_y=flow[..., 1]    # Extracting V from flow matrix

    H,W= flow_x.shape           

    
    valid_idx = np.flatnonzero(confidence>thres)       # getting indexs of pixels which are greater than threshold


    xp = valid_idx % W          # Getting x index of pixels in image frame
    yp = valid_idx // W         # Getting y index of pixels in image frame

    
    flow_x = flow_x[yp,xp]     # Extracting flow for points satisfying conditions
    flow_y = flow_y[yp,xp]
    
    zero_matrix = np.zeros(len(xp))
    one_matrix= np.ones(len(xp))

    Xp=np.column_stack((xp,yp,one_matrix))          # making (xp,yp,1) 

    p_dot=np.column_stack((flow_x,flow_y,zero_matrix))  # making (flow_x,flow_y,0) 
   
    ep_cameraframe = np.dot(np.linalg.inv(K), ep)        # Converting ep in image cooridates to 3d camera frame.


    for i in range (Xp.shape[0]):
        X_cameraframe=np.dot(np.linalg.inv(K),Xp[i])        # Converting Xp in image cooridates to 3d camera frame.

        depth= np.linalg.norm(np.subtract(X_cameraframe,ep_cameraframe))/ np.linalg.norm((p_dot[i]))  # Calculating depth from equation

        depth_map[yp[i], xp[i]] = depth             # because depth_map = size of confidence.


    ### STUDENT CODE END ###
    
    
    ## Truncate the depth map to remove outliers
    
    # require depths to be positive
    truncated_depth_map = np.maximum(depth_map, 0) 
    valid_depths = truncated_depth_map[truncated_depth_map > 0]
    
    # You can change the depth bound for better visualization if you depth is in different scale
    depth_bound = valid_depths.mean() + 10 * np.std(valid_depths)
    print(f'depth bound: {depth_bound}')

    # set depths above the bound to 0 and normalize to [0, 1]
    truncated_depth_map[truncated_depth_map > depth_bound] = 0
    truncated_depth_map = truncated_depth_map / truncated_depth_map.max()



    return truncated_depth_map
