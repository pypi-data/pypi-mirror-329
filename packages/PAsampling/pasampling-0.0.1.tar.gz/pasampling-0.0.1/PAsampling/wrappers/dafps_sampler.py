from ..native_functions import *
from scipy.spatial import cKDTree
import numpy as np

class DAFPS:
    """
    Implements the Density-Aware Farthest Point Sampling (DA-FPS) algorithm.

    This class provides a wrapper around the da_fps_np function, allowing for the selection
    of a subset of samples from a dataset based on the DA-FPS strategy. The selection can be 
    performed using different distance functions and can handle precomputed distance matrices.

    Attributes:
    -----------
    X : numpy.ndarray (n_samples, n_features)
        Input points, representing a set of data points.
    d : numpy.ndarray (n_samples, knn), optional (default=None)
        knn distance matrix between points. The i-th row contains the sorted distances between the i-th point and its k nearest neighbors.
    knn : int, optional (default=100)
        The number of nearest neighbors to consider when computing the knn distance matrix.
    weights : numpy.ndarray (n_samples, ), optional (default=None)
        Array of weights for each point. If provided, these weights are used to adjust the selection process.
    precomputed_distances : bool, optional (default=False)
        If True, the input X is assumed to be a precomputed distance matrix.
                
    """
    
    def __init__(self, X, d=None, knn=100, weights=None, precomputed_distances=False):
        self.knn = knn
        self.X = X
        self.precomputed_distances = precomputed_distances
        self.weights = weights
        self.d = d
        if self.precomputed_distances is False:
            if self.weights is None:
                if self.d is None:
                    # If also knn is not provided, raise an error
                    if self.knn is None:
                        raise ValueError("At least one among the following input values must be provided: weights, d (knn matrix) and knn.")
                    else:
                        # Compute knn distance matrix using cKDTree
                        tree = cKDTree(X)
                        self.d, _ = tree.query(X, knn, workers=-1)
            # If weights are provided, knn distance matrix not needed
            else: 
                self.d = None
        else:
            # If precomputed distances are provided and weights are not provided
            if self.weights is None:
                # If also knn is not provided, raise an error
                if self.knn is None:
                    raise ValueError("At least one among the following input values must be provided: weights, d (knn matrix) and knn.")
                else:
                    # Compute knn distance matrix from precomputed distances using argsort
                    nearest_indices = np.argsort(X, axis=1)[:, :self.knn]
                    self.d = np.take_along_axis(X, nearest_indices, axis=1)
            # If weights are provided, knn distance matrix not needed
            else:
                self.d = None
                    
    def fit(self, initial_subset, b_samples, mu=0, distance_func=None, verbose=False):
        """Fits the model to the data X and returns the indices of the selected samples. 
          
        Parameters:
        -----------
        initial_subset : list
            List of indices (rows of the input points matrix) representing the initial set of selected elements.
        b_samples : int
            The desired number of points to select.
        mu : int, optional (default=0)
            The number of initial points to select using FPS before applying the DA-FPS algorithm.
            mu is expressed as a percentage of the total number of samples in the dataset. Default is 0%.
        distance_func : callable, optional (default=None)
            A function to compute pairwise distances. If None, Euclidean distance is used.
        verbose : bool, optional (default=False)
            If True, progress messages are printed.

        Returns:
        --------
        samples : list
            List of indices representing the selected points using the DAFPS algorithm.
        """ 
        if int(self.X.shape[0]/100*mu)>= b_samples:
            raise ValueError("Choose mu smaller. The value of mu exceeds or equals the labeling budget.")
        if mu == 0:      
            return da_fps_np(self.X, initial_subset, b_samples, self.d, distance_func, self.precomputed_distances, self.weights, verbose)
        elif mu > 0:
            initial_subset_fps = fps_np(self.X, initial_subset, int((len(self.X) / 100) * mu))
            return da_fps_np(self.X, initial_subset_fps, b_samples, self.d, distance_func, self.precomputed_distances,  self.weights, verbose)
        else:
            raise ValueError("Invalid mu value. Choose a positive integer.")

