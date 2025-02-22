import os
import requests
import scipy.io
import pandas as pd
import numpy as np
import tarfile
import zipfile
import tarfile
from sklearn.preprocessing import MinMaxScaler


class DataLoader:
    """
    A class used to load and preprocess various datasets.
    
    Parameters:
    -----------
        save_path (str): The directory where the datasets will be saved. Default is the current working directory.
    
    Attributes:
    -----------  
    unzip_file(file_path, extract_to='.'):
        Unzips a compressed file (zip or tar) to a specified directory.
    download_data(url, save_path):
        Downloads data from a specified URL and saves it to a specified path.
    QM7_dataset(preprocessing=True):
        Downloads and processes the QM7 dataset, with optional preprocessing.
    Power_Grid_dataset(normalize=True):
        Loads and preprocesses the Power Grid dataset, with optional normalization.
        
    """
    
    def __init__(self, save_path=None):
        # Initialize the Dataset class with a specified save_path or the current working directory
        self.save_path = save_path if save_path else os.getcwd()


    def unzip_file(self, file_path, extract_to='./data'):
        """
        Unzip a compressed file (zip or tar) to a specified directory.
        
        :param file_path: Path to the compressed file.
        :param extract_to: Directory to extract the files to.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")
        
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
                print(f"Extracted {file_path} to {extract_to}")
        elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_to)
                print(f"Extracted {file_path} to {extract_to}")
        elif file_path.endswith('.tar.bz2'):
            with tarfile.open(file_path, 'r:bz2') as tar_ref:
                tar_ref.extractall(extract_to)
                print(f"Extracted {file_path} to {extract_to}")
        elif file_path.endswith('.tar'):
            with tarfile.open(file_path, 'r:') as tar_ref:
                tar_ref.extractall(extract_to)
                print(f"Extracted {file_path} to {extract_to}")
        else:
            raise ValueError(f"Unsupported file type: '{file_path}'")


    def download_data(self, url, save_path):
        if os.path.exists(save_path):
            return
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Download successful. Data saved to {save_path}")
        else:
            print(f"Failed to download data. Status code: {response.status_code}")


    def QM7_dataset(self, preprocessing= True):
        """
        Downloads and processes the QM7 dataset.

        Parameters:
        -----------
            preprocessing (bool): If True, extracts the upper triangular entries of each matrix in the dataset.
                                    If False, reshapes the matrices into vectors. Default is True.

        Returns:
        --------
            tuple: A tuple containing:
                - features (np.ndarray): The processed feature matrix.
                - labels (np.ndarray): The labels corresponding to the feature matrix.
        """
        # Download and process QM7 dataset
        qm7_url = 'http://quantum-machine.org/data/qm7.mat'
        self.data_qm7_path = os.path.join(self.save_path, 'data_qm7') 
        os.makedirs(self.data_qm7_path, exist_ok=True)
        self.save_path = os.path.join(self.data_qm7_path, 'qm7.mat')
        self.download_data(qm7_url, self.save_path)
        mat_contents = scipy.io.loadmat(self.save_path)
        variable1 = mat_contents['X']
        variable2 = mat_contents['T']
        if preprocessing:
            upper_triangular_entries_all = []
            # Loop through each matrix in variable1
            for matrix in variable1:
                # Get the indices of the upper triangular part
                indices = np.triu_indices(matrix.shape[0])
                # Extract the upper triangular elements using the indices
                upper_triangular_entries = matrix[indices]
                # Store the upper triangular entries in the list
                upper_triangular_entries_all.append(upper_triangular_entries)
            # Convert the list to a numpy array if needed
            features = np.array(upper_triangular_entries_all)
        else:
            features = variable1.reshape((variable1.shape[0], variable1.shape[1] ** 2))
        labels = variable2.reshape(-1)
        return features, labels
    
    
        
        
    def Power_Grid_dataset(self, normalize = True):
            """
            Loads and preprocesses the Power Grid dataset.
            This function downloads the Power Grid dataset from the UCI repository if it is not already present,
            extracts the data, and loads it into a pandas DataFrame. It then selects specific features and the target label,
            optionally normalizes the features, and returns the feature vectors and labels.
            
            Parameters:
            -----------
            normalize (bool): If True, the feature vectors will be normalized using MinMaxScaler. Default is True.
            
            Returns:
            --------
            tuple: A tuple containing:
                - features (numpy.ndarray): The feature vectors.
                - labels (numpy.ndarray): The target labels.
            """
            
            grid_url = 'https://archive.ics.uci.edu/static/public/471/electrical+grid+stability+simulated+data.zip'
            self.data_grid_path = os.path.join(self.save_path, 'data_grid') 
            self.save_path_zip = os.path.join(self.data_grid_path, 'Pgrid.zip')
            self.save_path_csv = os.path.join(self.data_grid_path, 'Pgrid_data/')
            if not os.path.exists(self.data_grid_path):
                os.makedirs(self.data_grid_path, exist_ok=True)
                self.download_data(grid_url, self.save_path_zip)
                self.unzip_file(self.save_path_zip, extract_to= self.save_path_csv)
                greed_df = pd.read_csv(os.path.join(self.save_path_csv,'Data_for_UCI_named.csv'))
            else:
                greed_df = pd.read_csv(os.path.join(self.save_path_csv,'Data_for_UCI_named.csv'))
            features_df = greed_df[['tau1', 'tau2', 'tau3', 'tau4', 'p1', 'p2', 'p3', 'p4', 'g1', 'g2',
                'g3', 'g4']]
            feature_vectors = features_df.values
            labels = greed_df['stab'].values  
    
            if normalize == True:
                scaler = MinMaxScaler()
                x_not_norm = np.array(feature_vectors)
                features= scaler.fit_transform(x_not_norm)
            else:
                features= feature_vectors
            return features, labels


                
                
            
        
    
