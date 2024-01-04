import numpy as np


def P3P(Pc, Pw, K=np.eye(3)):
    """
    Solve Perspective-3-Point problem, given correspondence and intrinsic

    Input:
        Pc: 4x2 numpy array of pixel coordinate of the April tag corners in (x,y) format
        Pw: 4x3 numpy array of world coordinate of the April tag corners in (x,y,z) format
    Returns:
        R: 3x3 numpy array describing camera orientation in the world (R_wc)
        t: (3,) numpy array describing camera translation in the world (t_wc)

    """

    ##### STUDENT CODE START #####

    # Invoke Procrustes function to find R, t
    # You may need to select the R and t that could transoform all 4 points correctly. 
    # R,t = Procrustes(Pc_3d, Pw[1:4])
    ##### STUDENT CODE END #####


 
    f= K[0,0]                   # Extracting Focus  
    u= Pc[:,0]
    v=Pc[:,1]
    j=np.zeros((3,3))
    for i in range(3):
        j[i]=np.array([u[i]-K[0,2], v[i]-K[1,2],f])         # Find J direction unit vector and 
        mag=np.linalg.norm(j[i])                            # subtracting camera center so as to get relative U and V
        j[i]= np.divide(j[i],mag)   


    cos_alpha=np.dot(j[1],j[2])                             
    ca=cos_alpha
    cos_beta=np.dot(j[0],j[2])
    cb=cos_beta
    cos_gamma= np.dot(j[0],j[1])
    cg=cos_gamma
    
    a= np.linalg.norm(Pw[1]-Pw[2])                        # Finding distance between 2 points
    b= np.linalg.norm(Pw[0]-Pw[2])
    c= np.linalg.norm(Pw[0]-Pw[1])

    #Random variables for the coefficients
    var1=((a**2-c**2)/b**2)                         
    var2=((a**2+c**2)/b**2)
    var3=((b**2-c**2)/b**2)
    var4=((b**2-a**2)/b**2)
    
    a2=a**2
    b2=b**2
    c2=c**2

    # Finding Grunets Variables

    A0= (1+var1)**2 - (4*a2*cg**2)/b2

    A1= 4*(-var1*(1+var1)*cb  + (2*a2*(cg**2)*cb)/b2  -  (1-var2)*ca*cg) 

    A2= 2*( (var1**2) - 1 + ((2*var1**2)*cb**2) + (2*var3*ca**2)  - 4*var2*ca*cb*cg + 2*var4*cg**2 )

    A3= 4*(var1* (1-var1)*cb - (1-var2)*ca*cg + (2*c2*(ca**2)*cb)/b2)

    A4= (var1-1)**2 - (4*c2*ca**2)/b2

    coeff=[A4,A3,A2,A1,A0]

    soln= np.roots(coeff)   
    Vs_value = []

    # Iterate through the roots and keep only real roots
    for root in soln:
        if (np.isreal(root) and root>0):            # Getting only real and positive roots as it is distance varible
            Vs_value.append(root.real)              

    # Initalizing variable arrays
    Vs_value=np.array(Vs_value)                      
    Us_value= np.zeros((Vs_value.shape[0],1))       
    S1_value= np.zeros((Vs_value.shape[0],1))
    S2_value= np.zeros((Vs_value.shape[0],1))
    S3_value= np.zeros((Vs_value.shape[0],1))
    P1dash_value= []
    P2dash_value= []
    P3dash_value= []

    for i in range(Vs_value.shape[0]):
        # Finding U values from Vs value 
        Us_value[i]= (((-1+var1)*(Vs_value[i]**2))  - 2*var1*cb*Vs_value[i]+1+var1)/(2*(cg-Vs_value[i]*ca))
        # Finding S1 using Vs and Us 
        S1_value[i]=np.sqrt((a2)/(Us_value[i]**2+Vs_value[i]**2 -2*Us_value[i]*Vs_value[i]*ca))
        
        #Finding S2 S3 
        S2_value[i]= Us_value[i]*S1_value[i]
        S3_value[i]= Vs_value[i]*S1_value[i]
        
        # Finding Pc in 3d frame
        P1dash_value.append((S1_value[i,0]*j[0]))
        P2dash_value.append((S2_value[i,0]*j[1]))
        P3dash_value.append((S3_value[i,0]*j[2]))

    P1dash_value=np.array(P1dash_value)
    P2dash_value=np.array(P2dash_value)
    P3dash_value=np.array(P3dash_value)

    Pc_3d_external=np.vstack((P1dash_value,P2dash_value,P3dash_value))

    Pc_3d=np.zeros((2,3,3))

    min_error = 0
    R_final = np.eye(3)
    t_final = np.ones((3,))

    for i in range(Vs_value.shape[0]):

        Pc_3d[i]= Pc_3d_external[i::2]  # Taking each value of Pc_3d and find R and t for all

        R, t = Procrustes(Pc_3d[i],Pw[0:3,:])

        #Finding world corrdinates with the derived R and t and then comparing with input Pw
        Pw_ = K[0][0]*np.dot(np.linalg.inv(K),np.array([Pc[-1,0], Pc[-1,1], 1]).T)

        Pw_ = np.dot(R,Pw_)+t

        #Finding Error
        error = np.linalg.norm((Pw[-1,:] - Pw_))

        if i==0:
            min_error = error
            R_final = R
            t_final = t
        else:
            if error<min_error:
                error = min_error
                R_final = R
                t_final = t
        i=i+1

        R = R_final
        t = t_final

    return R, t

def Procrustes(X, Y):
    """
    Solve Procrustes: Y-A = RX-B + t

    Input:
        X: Nx3 numpy array of N points in camera coordinate (returned by your P3P)
        Y: Nx3 numpy array of N points in world coordinate
    Returns:
        R: 3x3 numpy array describing camera orientation in the world (R_wc)
        t: (3,) numpy array describing camera translation in the world (t_wc)

    """
    ##### STUDENT CODE START #####

    X_mean= np.mean(X, axis=0)              # centroid of points
    Y_mean = np.mean(Y, axis=0)
    X_centered= X - X_mean                  # subtracting centroid points
    X_centered=np.transpose(X_centered)
    Y_centered = Y - Y_mean
    Y_centered=np.transpose(Y_centered)     


    bat= np.dot(X_centered,np.transpose(Y_centered))        # doing BAT --> SVD.
    U, S ,VT= np.linalg.svd(bat, full_matrices=False)       

    V= np.transpose(VT)
    UT= np.transpose(U)
    det_check=np.eye(3)                                    
    det_check[-1,-1] = np.linalg.det(np.dot(V,UT))  

    R=np.dot(V,np.dot(det_check,UT))                        # Finding R following the slides

    t= Y_mean - np.dot(R,X_mean)                            #t = A mean - R.Bmean


    ##### STUDENT CODE END #####

    return R, t



