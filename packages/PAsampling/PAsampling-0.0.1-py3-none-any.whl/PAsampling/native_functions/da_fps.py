from tqdm import tqdm
import numpy as np
from scipy.spatial.distance import cdist
import os

def da_fps_np(X, initialization, b, d = None, distance_func=None, precomputed_distances=False, weights=None, verbose = False):
    """
    This function implements the Density Aware Farthest Point Sampling (DAFPS) algorithm using the numpy library.
    DAFPS selects a subset of points from a dataset by iteratively choosing the point that is farthest from the current set of selected points,
    while also considering the density of points in the neighborhood of each selected point.

    Parameters:
    -----------
    X : numpy.ndarray (n_samples, n_features)
        Input points, representing a set of data points. 
    initialization : list
        List of indices (rows of the input points matrix) representing the initial set of selected elements.
    b : int
        The desired number of points to select.
    d : numpy.ndarray (n_samples, knn), optional (default=None)
        Distance matrix or array of distances between points. If None, it is computed using the Euclidean distance.
    distance_func : callable, optional (default=None)
        A function to compute pairwise distances. If None, Euclidean distance is used.
    precomputed_distances : bool, optional (default=False)
        If True, the input X is assumed to be a precomputed distance matrix.
    weights : numpy.ndarray (n_samples, ), optional (default=None)
        Array of weights for each point. If provided, these weights are used to adjust the selection process.
    verbose : bool, optional (default=False)
        If True, progress messages are printed.

    Returns:
    --------
    centers : list
        List of indices representing the selected points using the DA-FPS algorithm.
    """
    if b > len(X):
        print('Error: number of points to select larger than the number of available points')
        return
    if len(initialization) >= b:            
        print('Error: initial subset already contains the desired number of points or more.')
        return
    centers = [i for i in initialization]
    if precomputed_distances is True:
        distances = X[:, centers].min(axis=1)
    else:
        if distance_func is None:
            distances = np.min(cdist(X, X[centers]), axis=1)
        else:
            distances = np.min(np.asarray([distance_func(X[c], X) for c in centers]), axis = 0)   
    if weights is not None:
        dweights = weights

    # Iterate to select additional points until reaching the desired number
    for n in tqdm(range(b - len(initialization)), disable=not verbose):
        # Find the points in the neighborhood of all current centers
        if weights is None:
            dweights = np.sum((d <= distances[:, np.newaxis]), axis=1)
        # Calculate distances weights based on the number of neighbors
        distances_weights = distances * dweights
        # Find the point farthest from all current centers
        farthest_point = np.argmax(distances_weights)
        # Add it as a new center
        centers.append(farthest_point)
        # Recalculate distances from all points to the new center
        if precomputed_distances is True:
            new_distances = np.minimum(X[:, farthest_point], distances)
        else:
            if distance_func is None:
                new_distances =  np.minimum(np.linalg.norm(X - X[farthest_point], axis=1), distances)
            else:
                new_distances = np.minimum(distance_func(X[farthest_point], X), distances)
        distances = new_distances
    # Return the final set of selected centers
    return centers
