from est_homography import est_homography
import numpy as np

def PnP(Pc, Pw, K=np.eye(3)):
    """
    Solve Perspective-N-Point problem with collineation assumption, given correspondence and intrinsic

    Input:
        Pc: 4x2 numpy array of pixel coordinate of the April tag corners in (x,y) format
        Pw: 4x3 numpy array of world coordinate of the April tag corners in (x,y,z) format
    Returns:
        R: 3x3 numpy array describing camera orientation in the world (R_wc)
        t: (3, ) numpy array describing camera translation in the world (t_wc)

    """

    ##### STUDENT CODE START #####

    # Homography Approach
    H= est_homography(Pw[:,0:2], Pc) 

    H_dash= np.dot(np.linalg.inv(K),H)    # H'=K-1*(K*[r1 r2 r3])
    a=H_dash[:,0]
    b=H_dash[:,1]
    A=np.transpose(np.array([a,b]))

    U, S ,VT= np.linalg.svd(A, full_matrices=False)   # SVD

    B=np.dot(U,VT)
    r1= B[:,0]
    r2=B[:,1]
    r3=np.cross(r1,r2)     # r3=r1xr2
    
    lamb= (S[0]+S[1])/2

    Tcw = np.divide(H_dash[:,-1],lamb)  # t=c/lambda
    Rcw=np.column_stack((r1,r2,r3))      

    R = np.transpose(Rcw)           # Rwc= Transcpose of Rcw
    t=np.dot(R,-Tcw)                

    return R, t

