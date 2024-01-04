import numpy as np

def compute_planar_params(flow, K, up=[256, 0], down=[512, 256]):
    """
    Use the flow field to compute the 8 parameters of the planar motion.
    
    Inputs:
        - flow: optical flow - shape: (H, W, 2)
        - K: intrinsic calibration matrix - shape: (3, 3)
        - up: upper left corner of the patch - list of 2 integers
        - down: lower right corner of the patch - list of 2 integers
    Outputs:
        - sol: solution to the linear equation - shape: (8,)
    """
    
    ### STUDENT CODE START ###
    
    # 1. Extract the flow in the patch
    # 2. Normalize the flow by the intrinsic matrix
    # 3. Convert the pixel coordinates to normalized projective coordinates
    # 4. Solve the linear equation of 8 parameters
    # Useful functions: np.meshgrid(), np.linalg.lstsq()
    
    
    ### STUDENT CODE END ###
    
    return sol
    
