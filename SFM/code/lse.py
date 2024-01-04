import numpy as np

def least_squares_estimation(X1, X2):
  """ YOUR CODE HERE
  """

  Aa=[]
  # reshaping X2_T*E*X1 = 0 to 
  # Af=0 where A= x1 x x2 from Kronecker Product
  for i in range(X1.shape[0]):
    A=np.kron(X2[i,:],X1[i,:])
    Aa.append(A)
  Aa=np.vstack(Aa)
  U,D,VT=np.linalg.svd(Aa)
  Ea= VT[-1,:]
  Ea=np.reshape(Ea, (3,3))
  
  Ua,Da,VaT= np.linalg.svd(Ea)
  Da = np.diag([1, 1, 0])

  E = Ua @ Da @ VaT

  """ END YOUR CODE
  """
  return E
