import numpy as np
import matplotlib.pyplot as plt

def plot_flow(image, flow_image, confidence, threshmin=10):
    """
    Plot a flow field of one frame of the data.
    
    Inputs:
        - image: grayscale image - shape: (H, W)
        - flow_image: optical flow - shape: (H, W, 2)
        - confidence: confidence of the flow estimates - shape: (H, W)
        - threshmin: threshold for confidence (optional) - scalar
    """
    
    ### STUDENT CODE START ###
    
    plt.imshow(image, cmap='gray')
    
    # Define a threshold mask based on confidence
    mask = confidence > threshmin

    
    # # Extract x and y components of the flow field
    flow_y = flow_image[:, :, 1]    
    flow_x = flow_image[:, :, 0]
    

    H, W = image.shape  

    # Create a grid of coordinates for the flow field
 
    x, y = np.meshgrid(np.arange(0,W),np.arange(0,H))

    
    # Plot the flow field using plt.quiver
    plt.quiver(x[mask],y[mask],flow_x[mask],-flow_y[mask],color='red',scale=15)   # -y because quiver has y is upwards


    return





    

