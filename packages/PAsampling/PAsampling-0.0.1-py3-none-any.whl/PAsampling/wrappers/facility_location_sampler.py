from apricot import FacilityLocationSelection
import numpy as np
from sklearn.metrics import pairwise_distances

class FacilityLocation:
    """
    Implements the FacilityLocationSelection function from the Apricot library (https://apricot-select.readthedocs.io/en/).

    This class provides a wrapper around the FacilityLocationSelection function, allowing for the selection
    of a subset of samples from a dataset based on the facility location strategy. The selection can be 
    performed using different metrics, including 'euclidean', 'Gaussian', and 'precomputed'.

    Attributes:
    -----------
    b_samples : int
        The number of samples to select.
    metric : str, optional (default='euclidean')
        The metric to use for computing distances. Options are 'euclidean', 'Gaussian', and 'precomputed'.
    initial_subset : list, optional (default=None)
        A list of initial indices to include in the subset.
    verbose : bool, optional (default=False)
        Whether to print progress messages.
    n_jobs : int, optional (default=-1)
        The number of parallel jobs to run. -1 means using all processors.

    """
    
    def __init__(self, b_samples, metric='euclidean',initial_subset=None, verbose=False, n_jobs=-1):
        self.b_samples = b_samples
        self.metric = metric
        self.initial_subset = initial_subset
        self.verbose = verbose
        self.n_jobs = n_jobs

    def fit(self, X, gamma = 0.1):
        """ 
        Fits the function to the data X, with shape (n_samples, n_features), and returns the indices of the selected samples.
        If the metric is 'Gaussian', the gamma parameter is used to compute the RBF kernel matrix.
        If the metric is 'precomputed', the input X is assumed to be a precomputed distance matrix.
        
        Parameters:
        -----------
        X : numpy.ndarray
            Input data matrix, representing a set of data points.
            If metric is 'precomputed', X is expected to be the matrix of precomputed pairwise distances.
        gamma : float, optional (default=0.1)
            The gamma parameter for the RBF kernel matrix. Used if metric is 'Gaussian'.
        
        Returns:
        --------
        Samples : list
            List of indices representing the selected points using the FacilityLocation algorithm.
        
        """
        if self.metric == 'euclidean':
            self.selector = FacilityLocationSelection(
                                                    self.b_samples, 
                                                    self.metric,
                                                    initial_subset=self.initial_subset,
                                                    verbose=self.verbose,
                                                    n_jobs=self.n_jobs
                                                    )
            self.selector.fit(X)
            return self.selector.ranking
        elif self.metric == 'Gaussian':
            sq_dist = pairwise_distances(X, metric = 'sqeuclidean', n_jobs = -1)
                # Compute the RBF kernel matrix
            K = np.exp(-gamma * sq_dist)
            selector = FacilityLocationSelection(
                                                self.b_samples, 
                                                metric = 'precomputed',
                                                initial_subset=self.initial_subset,
                                                verbose=self.verbose,
                                                n_jobs=self.n_jobs
                                                )
            selector.fit(K)
            return self.selector.ranking
        elif self.metric == 'precomputed':
            selector = FacilityLocationSelection(
                                                self.b_samples, 
                                                metric = 'precomputed',
                                                initial_subset=self.initial_subset,
                                                verbose=self.verbose,
                                                n_jobs=self.n_jobs
                                                )
            selector.fit(X)
            return self.selector.ranking