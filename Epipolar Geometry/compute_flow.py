import numpy as np

def flow_lk_patch(Ix, Iy, It, x, y, size=5):
    """
    Find the Lucas-Kanade optical flow on a single square patch.
    The patch is centered at (y, x), therefore it generally extends
    from x-size//2 to x+size//2 (inclusive), same for y, EXCEPT when
    exceeding image boundaries!
    
    WARNING: Pay attention to how you index the images! The first coordinate
    is actually the y-coordinate, and the second coordinate is the x-coordinate.
    
    Inputs:
        - Ix: image gradient along the x-dimension - shape: (H, W)
        - Iy: image gradient along the y-dimension - shape: (H, W)
        - It: image time-derivative - shape: (H, W)
        - x: SECOND coordinate of patch center - integer in range [0, W-1]
        - y: FIRST coordinate of patch center - integer in range [0, H-1]
        - size: optional parameter to change the side length of the patch in pixels
    
    Outputs:
        - flow: flow estimate for this patch - shape: (2,)
        - conf: confidence of the flow estimates - scalar
    """

    ### STUDENT CODE START ###
    Ix_column = Ix[y-size//2 : (y+size//2) +1 , (x-size//2) : ((x+size//2) +1)].flatten().reshape(-1,1)
    Iy_column = Iy[y-size//2 : (y+size//2) +1 , (x-size//2) : ((x+size//2) +1)].flatten().reshape(-1,1)
    It_column = It[y-size//2 : (y+size//2) +1 , (x-size//2) : ((x+size//2) +1)].flatten().reshape(-1,1)

    A= np.hstack((Ix_column, Iy_column))
    B= -It_column

    flow,_,_,conf = np.linalg.lstsq(A, B, rcond=-1)
    conf=np.min(conf)
   
    ### STUDENT CODE END ###

    return flow.reshape(-1,), conf


def flow_lk(Ix, Iy, It, size=5):
    """
    Compute the Lucas-Kanade flow for all patches of an image.
    To do this, iteratively call flow_lk_patch for all possible patches.
    
    WARNING: Pay attention to how you index the images! The first coordinate
    is actually the y-coordinate, and the second coordinate is the x-coordinate.
    
    Inputs:
        - Ix: image gradient along the x-dimension - shape: (H, W)
        - Iy: image gradient along the y-dimension - shape: (H, W)
        - It: image time-derivative
    Outputs:
        - image_flow: flow estimate for each patch - shape: (H, W, 2)
        - confidence: confidence of the flow estimates - shape: (H, W)
    """
    H, W = Ix.shape

    Ix = np.pad(Ix, ((2, 2), (2, 2)), mode='constant', constant_values=0)      # Padding image with 0 
    Iy = np.pad(Iy, ((2, 2), (2, 2)), mode='constant', constant_values=0)
    It = np.pad(It, ((2, 2), (2, 2)), mode='constant', constant_values=0)

    
    image_flow = np.zeros((H, W, 2))
    confidence = np.zeros((H, W))
    ### STUDENT CODE START ###
    # double for-loop to iterate over all patches
    for i in range(size//2,H+4-size//2):
        for j in range(size//2, W+4-size//2):
            flowing,confidence_val=flow_lk_patch(Ix, Iy, It, j, i, size=5)
            image_flow[i-2, j-2] = flowing
            confidence[i-2, j-2] = confidence_val


    
    ### STUDENT CODE END ###
    
    return image_flow, confidence

    

