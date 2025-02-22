import numpy as np
from ..native_functions import  fps_np
from .kmedoids_sampler import Kmedoids
from .facility_location_sampler import FacilityLocation
from .twin_sampler import Twin
import random

class FPS_plus:
    """
    Implements a modified version of the Farthest Point Sampling (FPS) algorithm.

    This class provides a wrapper around the fps_np function and integrates it with various sampling strategies.
    It allows for the selection of a subset of samples from a dataset based on the FPS strategy, followed by 
    additional selection using different methods such as k-medoids, facility location, random sampling, and twinning.

    Attributes:
    -----------
    method : str, optional (default='kmedoids')
        The sampling method to use after the initial FPS selection. Options are 'kmedoids', 
        'facility_location', 'random', and 'twin'.

    mu : int, optional (default=3)
        The number of initial points to select using FPS before applying the respective strategy.
        mu is expressed as a percentage of the total number of samples in the dataset. Default is 3%.
    
    """
    
    def __init__(self, method='kmedoids', mu=3):
        self.method = method
        self.mu = mu
        
    def fit(self, X, initial_subset, b_samples, metric='euclidean', ratio = 5, idx_initial_point = 0, init_kmedoids = 'k-medoids++', random_state=None):
        """Fits the model to the data X and returns the indices of the selected samples.
        
        Parameters:
        -----------
        X : numpy.ndarray (n_samples, n_features)
            Input points, representing a set of data points.
        initial_subset : list
            List of indices (rows of the input points matrix) representing the initial set of selected elements.
        b_samples : int
            The desired number of points to select.
        metric : str, optional (default='euclidean')
            The metric to use for computing distances. Options are 'euclidean', 'manhattan', etc.
        ratio : int, optional (default=5)
            The ratio parameter for the twinning method.
        idx_initial_point : int, optional (default=0)
            The initial point index for the twinning method.
        init_kmedoids : str, optional (default='k-medoids++')
            The method for initialization in k-medoids. Options are 'random', 'heuristic', 'k-medoids++', and 'build'.
        random_state : int, optional (default=None)
            The seed used by the random number generator.

        Returns:
        --------
        samples : list
            List of indices representing the selected points using the modified FPS algorithm.
    
        """
        if self.method == 'kmedoids':
            return self.fps_kmedoids(X, initial_subset,  b_samples, metric, init_kmedoids, random_state)
        elif self.method == 'facility_location':
            return self.fps_facility_location(X, initial_subset, b_samples, metric)
        elif self.method == 'random':
            return self.fps_random(X, initial_subset,  b_samples, random_state=random_state)
        elif self.method == 'twin':
            return self.fps_twinning(self, X, initial_subset, ratio, idx_initial_point)
        else:
            raise ValueError("Invalid method. Choose 'kmedoids', 'facility_location', 'random', or 'twin'.")

    def fps_kmedoids(self, X, initial_subset,  b_samples, metric, init_kmedoids = 'k-medoids++', random_state=0):
        idx = fps_np(X, initial_subset, int((len(X) / 100) * self.mu))
        idx_test = list(np.arange(X.shape[0]))
        idx_test_selected = list(set(idx_test).difference(set(idx)))
        if random_state is None:
            random_state = random.randint(0, 1000) 
        b = b_samples - len(idx)
        kmedoids_sampler = Kmedoids(b_samples= b,  metric=metric, init=init_kmedoids, random_state = random_state)
        kmedoids_indices = kmedoids_sampler.fit(X[idx_test_selected])
        idx_train = list(idx) + list(np.asarray(idx_test_selected)[np.asarray(kmedoids_indices)])
        return idx_train

    def fps_facility_location(self, X, initial_subset,  b_samples , metric='euclidean'):
        idx = fps_np(X, initial_subset, int((len(X) / 100) * self.mu))
        b = b_samples - len(idx)
        facility_location_sampler = FacilityLocation(initial_subset = list(idx), b_samples=b, metric= metric)
        facility_location_indices = facility_location_sampler.fit(X)
        idx_slctd = list(idx) + list(facility_location_indices)
        return idx_slctd

    def fps_random(self, X, initial_subset, b_samples, random_state=None):
        idx_fps = fps_np(X, initial_subset, int((len(X) / 100) * self.mu))
        if random_state is not None:
            random.seed(random_state)   
        idx_test = list(set(list(np.arange(X.shape[0]))).difference(idx_fps))
        idx_selected = idx_fps
        idx_selected += random.sample(idx_test, b_samples - len(idx_fps))
        return idx_selected
    
    def fps_twinning(self, X, initial_subset, ratio, idx_initial_point):
        idx_fps = fps_np(X, initial_subset, int((len(X) / 100) * self.mu))
        idx_test = list(set(list(np.arange(X.shape[0]))).difference(idx_fps))
        twin_sampler = Twin(ratio=ratio, u1=idx_test[idx_initial_point])
        twin_indices = twin_sampler.fit(X[idx_test])
        idx_train = list(idx_fps) + list(np.asarray(idx_test)[np.asarray(twin_indices)])
        return idx_train

