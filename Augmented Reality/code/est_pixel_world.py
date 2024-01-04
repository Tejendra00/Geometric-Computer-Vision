import numpy as np

def est_pixel_world(pixels, R_wc, t_wc, K):
    """
    Estimate the world coordinates of a point given a set of pixel coordinates.
    The points are assumed to lie on the x-y plane in the world.
    Input:
        pixels: N x 2 coordiantes of pixels
        R_wc: (3, 3) Rotation of camera in world
        t_wc: (3, ) translation from world to camera
        K: 3 x 3 camara intrinsics
    Returns:
        Pw: N x 3 points, the world coordinates of pixels
    """

    ##### STUDENT CODE START #####
    Pw=np.zeros((pixels.shape[0],3))
    Pc=np.zeros((pixels.shape[0],3))
    Pc[:,0:2]=pixels
    Pc[:,-1]=1
    pixels=Pc               # Adding 1 column to pixels matrix.



    R_cw = np.linalg.inv(R_wc)              # Converting reference frame 
    t_cw = np.dot(R_cw,-t_wc)

    for i in range(pixels.shape[0]):
        
        H=np.dot(K,np.column_stack((R_cw[:,0:2],t_cw)))   #H= K.[r1 r2 t]

        H_inv=np.linalg.inv(H)          
        # Normalizing
        H_inv=H_inv/H_inv[-1,-1]                    
    
        Pw[i] = np.dot(H_inv,pixels[i])                 # Pw= H_inv* Pixels

    Pw[:, 0] = Pw[:, 0]/Pw[:,-1]                        # making z=1 first
    Pw[:, 1] = Pw[:, 1]/Pw[:,-1]

    Pw[:,-1]=0                                        # making z=0 as our april tag is on ground.
    
    ##### STUDENT CODE END #####
    return Pw
