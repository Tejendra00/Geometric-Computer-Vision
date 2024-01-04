import numpy as np

def pose_candidates_from_E(E):
  transform_candidates = []
  ##Note: each candidate in the above list should be a dictionary with keys "T", "R"
  """ YOUR CODE HERE
  """
  U, _, VT = np.linalg.svd(E)

  t= U[:,-1]

  Y= np.array([[0,-1,0],[1,0,0],[0,0,1]])

  R1= U @ Y.T @ VT
  R2= U @ Y @ VT
  
  if np.linalg.det(R1)<0 or np.linalg.det(R2) <0:
    R1=-R1
    R2=-R2
    t=-t

  transform_candidates = [
        {"T": t, "R": R1},
        {"T": t, "R": R2},
        {"T": -t, "R": R1},
        {"T": -t, "R": R2}
    ]

  """ END YOUR CODE
  """
  return transform_candidates