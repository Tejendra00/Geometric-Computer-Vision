import numpy as np
from scipy.ndimage import convolve1d
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from matplotlib.patches import Rectangle


# Use the following kernels for computing the image gradients
# G: a Gaussian smoothing kernel, used to smooth across the axes orthogonal to the gradient AFTER the gradient is computed
# H: the derivative kernel, that outputs a measure of the difference between neighboring pixels (derivative of a Gaussian)
KERNEL_G = np.array([0.015625, 0.093750, 0.234375, 0.312500, 0.234375, 0.093750, 0.015625])
KERNEL_H = np.array([0.03125, 0.12500, 0.15625, 0, -0.15625, -0.1250, -0.03125])

def compute_Ix(imgs):
    """
    Compute the gradient of the images along the x-dimension.
    
    WARNING: The first coordinate of the gradient is actually the y-coordinate,
    which means here you're computing the gradient along axis=1, NOT 0!
    
    Inputs:
        - imgs: image volume, axis semantics: first = y, second = x, third = t  
        - shape: (H, W, N)
    Outputs:
        - Ix: image gradient along the x-dimension 
        - shape: (H, W, N)
    """



    ### STUDENT CODE START ###
    Ix= convolve1d(imgs,KERNEL_H,axis=1)
    Ix= convolve1d(Ix,KERNEL_G,axis=0)
    Ix= convolve1d(Ix,KERNEL_G,axis=2)

    ### STUDENT CODE END ###
    
    return Ix

def compute_Iy(imgs):
    """
    Compute the gradient of the images along the x-dimension.
    
    WARNING: The first coordinate of the gradient is actually the y-coordinate,
    which means here you're computing the gradient along axis=0, NOT 1!
    
    Inputs:
        - imgs: image volume, axis semantics: first = y, second = x, third = t 
        - shape: (H, W, N)
    Outputs:
        - Iy: image gradient along the y-dimension - shape: (H, W, N)
    """

    ### STUDENT CODE START ###
    Iy= convolve1d(imgs,KERNEL_H,axis=0)
    Iy= convolve1d(Iy,KERNEL_G,axis=1)
    Iy= convolve1d(Iy,KERNEL_G,axis=2)
    
    ### STUDENT CODE END ###
    
    return Iy

def compute_It(imgs):
    """
    Compute the gradient of the images along the x-dimension.
    
    WARNING: The first coordinate of the gradient is actually the y-coordinate,
    which means here you're computing the gradient along axis=0, NOT 1!
    
    Inputs:
        - imgs: image volume, axis semantics: first = y, second = x, third = t 
        - shape: (H, W, N)
    Outputs:
        - It: temporal image gradient - shape: (H, W, N)
    """
    
    ### STUDENT CODE START ###
    It= convolve1d(imgs,KERNEL_H,axis=2)
    It= convolve1d(It,KERNEL_G,axis=1)
    It= convolve1d(It,KERNEL_G,axis=0)
    
    ### STUDENT CODE END ###
    
    return It
