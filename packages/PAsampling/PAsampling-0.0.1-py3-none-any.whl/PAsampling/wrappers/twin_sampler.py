from twinning import twin
import numpy as np

class Twin:
    """
    This class implements the twin function from the Twinning library https://github.com/avkl/twinning.

    Attributes:
    -----------
    r : float
        The ratio parameter for the twin function.
    u1 : int
        The initial point index for the twin function.
        
    """
    
    def __init__(self, ratio, idx_initial_point):
        self.r = ratio
        self.u1 = idx_initial_point

    def fit(self, X):
        """ Fits the twin function to the data X, with shape (n_sample, n_features) and returns the result as a list.
        
        Parameters:
        -----------     
        X : numpy.ndarray
            Input data matrix, representing a set of data points with shape (n_samples, n_features).
        
        Returns:
        --------
        Samples : list
            List of indices representing the selected points using the Twin algorithm.
        """
        X = np.asarray(X, dtype=np.float64)
        return twin(X, r=self.r, u1=self.u1).tolist()