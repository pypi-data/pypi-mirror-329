from sklearn_extra.cluster import KMedoids

class Kmedoids:
    """
    Implements the KMedoids function from the sklearn_extra library (https://scikit-learn-extra.readthedocs.io/en/stable/generated/sklearn_extra.cluster.KMedoids.html).

    This class provides a wrapper around the KMedoids function, allowing for the selection
    of a subset of samples from a dataset based on the k-medoids clustering strategy. The selection
    can be performed using different initialization methods and distance metrics.

    Attributes:
    -----------
    b_samples : int
        The number of samples to select (i.e., the number of clusters).
    init : str, optional (default='k-medoids++')
        The method for initialization. Options are  are 'random', 'heuristic', 'k-medoids++', and 'build'.
    metric : str, optional (default='euclidean')
        What distance metric to use. See sklearn.metrics.pairwise_distances metrics. Metric can be 'precomputed', the user must then feed the fit method with a precomputed kernel matrix and not the design matrix X.
    random_state : int, optional (default=None)
        The seed used by the random number generator.
    """
    
    def __init__(self, b_samples, init='k-medoids++', metric='euclidean', random_state=None,  max_iter=300):
        self.b_samples =b_samples
        self.init = init
        self.metric = metric
        self.random_state = random_state
        self.max_iter = max_iter

    def fit(self, X,):
        """ Fits the kmedoids function to the data matrix X and returns the indices of the selected samples (medoids).
        
        Parameters:
        -----------
        X : numpy.ndarray
            Input data matrix, representing a set of data points with shape (n_samples, n_features). 
            If metric is precomputed, X is expected to be the matrix of precomputed pairwise distances.
        
        Returns:
        --------
        samples : list
            List of indices representing the selected points using the kmedoids algorithm
        """
        self.kmedoids = KMedoids(
                                n_clusters=self.b_samples,
                                init=self.init,
                                metric=self.metric,
                                random_state=self.random_state,
                                max_iter=self.max_iter
                                )
        self.kmedoids.fit(X)
        return self.kmedoids.medoid_indices_