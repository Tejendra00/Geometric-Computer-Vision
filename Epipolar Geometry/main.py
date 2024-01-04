import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from matplotlib.patches import Rectangle

from compute_grad import compute_Ix, compute_Iy, compute_It
from compute_flow import flow_lk
from vis_flow import plot_flow
from depth import depth
from epipole import epipole


# DO NOT CHANGE THIS DEFINITION
K = np.array([
    [1118, 0, 357],
    [0, 1121, 268],
    [0, 0, 1]
])

if __name__ == "__main__":

    # TODO: Edit this parameter to see different results.
    threshmin = 2

    # load images
    data_folder = "data"
    images = [
        mpimg.imread(os.path.join(data_folder, "insight{}.png".format(i))) * 255
        for i in range(20, 27)
    ]
    images = np.stack(images, axis=-1)
    print(f'Loaded images with shape: {images.shape}')

    # find gradients
    Ix = compute_Ix(images)
    Iy = compute_Iy(images)
    It = compute_It(images)
    
    print(f'Computed gradients with shape: {Ix.shape}, {Iy.shape}, {It.shape}')

    # only take the image in the middle for flow computations
    valid_idx = 3
    flow, confidence = flow_lk(Ix[..., valid_idx], Iy[..., valid_idx], It[..., valid_idx])
    
    print(f'Computed LK flow with shape: {flow.shape}, {confidence.shape}')

    # visualize flow
    plt.figure()
    plot_flow(images[..., valid_idx], flow, confidence, threshmin=threshmin)
    plt.title(f'LK optical flow for threshold: {threshmin}')
    plt.savefig(f"flow_{threshmin}.png")
    plt.show()

    # compute and visualize epipole
    print('Computing epipole - this may take a while...')
    
    plt.figure()
    ep = epipole(flow[..., 0], flow[..., 1], confidence, threshmin, num_iterations=1000)
    ep = ep / ep[2]

    # define projective coordinates of all pixels
    x = np.array([i for i in range(images.shape[0])])
    y = np.array([i for i in range(images.shape[1])])
    xv, yv = np.meshgrid(x, y)
    xp = np.stack([xv.flatten(),yv.flatten(),np.ones(images.shape[:2]).flatten()]).T # shape: (512**2, 3)

    # visualize flow and epipole
    plot_flow(images[..., valid_idx], flow, confidence, threshmin=threshmin)
    plt.scatter(ep[0] + flow.shape[0]//2, ep[1] + flow.shape[1]//2, c='g', s=20, marker='*')
    # plt.scatter(xp[:, 0], xp[:, 1], c='b', s=0.1)
    plt.title(f'Epipole for threshold: {threshmin}')
    plt.savefig(f"epipole_{threshmin}.png")
    plt.show()

    depth_map = depth(flow, confidence, ep, K, thres=threshmin)
    sns.heatmap(depth_map, square=True, cmap='mako')
    plt.title(f'Depth map for threshold: {threshmin}')
    plt.savefig(f"depthmap_{threshmin}.png")
    plt.show()







