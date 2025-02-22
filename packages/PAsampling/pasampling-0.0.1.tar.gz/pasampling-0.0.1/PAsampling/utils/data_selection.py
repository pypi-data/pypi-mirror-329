import numpy as np
import h5py
from tqdm import tqdm
import random
from scipy.spatial import cKDTree
from ..wrappers.kmedoids_sampler import Kmedoids
from ..wrappers.facility_location_sampler import FacilityLocation
from ..wrappers.twin_sampler import Twin
from ..wrappers.fps_sampler import FPS
from ..wrappers.dafps_sampler import DAFPS
from ..wrappers.fps_plus_sampler import FPS_plus
np.random.seed(123)

def save_indices_to_h5py(group_train, group_test, trainig_set_sizes, indices, idx_test):
    for n in trainig_set_sizes:
        idx_train = indices[:n]
        idx_test_selected = list(set(idx_test).difference(set(idx_train)))
        group_train.create_dataset(f'selected_{n}', data=idx_train)
        group_test.create_dataset(f'selected_{n}', data=idx_test_selected)


def DataSelector(X, save_path, strategies=None, trainig_set_sizes=None, initial_conditions=None, knn=100, mu=3, ratios= None, gamma_FacLocG=1):
    """
    Selects data subsets based on various strategies and saves the indices to an HDF5 file.
    
    Parameters:
    -----------
    X : numpy.ndarray
        The input data array (n_points, n_features).
    save_path : str
        The path where the HDF5 file will be saved.
    strategies : list of str, optional
        List of strategies to use for data selection. Possible values include 'DAFPS', 'FPS', 'RDM', 'k-medoids++', 
        'FacilityLocation', 'Twinning', 'FPS-k-medoids++', 'FPS-FacLoc', 'FPS-RDM', 'FacLoc-G'.
    trainig_set_sizes : list of int, optional
        List of training set sizes to be used for each strategy.
    initial_conditions : list, optional
        List of initial conditions for the data selection strategies.
    knn : int, optional
        Number of nearest neighbors to consider for the DAFPS strategy. Default is 100.
    mu : int, optional
        Hyperparameter for the DAFPS and FPS-(mehtod) strategies. Default is 3.
    ratios : list of float, optional
        List of ratios for the Twinning strategy.
    gamma_FacLocG : float, optional
        Gamma parameter for the FacilityLocation strategy with Gaussian metric. Default is 1.
        
    Returns:
    --------
    None
    """
    f = h5py.File(save_path, "w") 
    #if 'DAFPS' in strategies:
    # print('DA-FPS hyperparameters are u={} and k={}'.format(knn, mu))                                                                                                                                                                                                                                       
    if 'DAFPS' in strategies:
        print('DAFPS ')  
        grp = f.create_group(f'DAFPS')
        dafps_sampler = DAFPS(X, knn=knn)
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
                subgrup_train = grp.create_group(f'train_Initialize_{count}')
                subgrup_test = grp.create_group(f'test_Initialize_{count}')
                dafps_indices = dafps_sampler.fit(initial_subset=[initial_sub], b_samples=max(trainig_set_sizes), mu=mu)
                idx_test = list(np.arange(X.shape[0]))
                save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes, dafps_indices, idx_test)  
                                                                                               
    if 'FPS' in strategies:
        print('FPS')
        grp = f.create_group(f'FPS')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            fps_sampler = FPS(precomputed_distances=False)
            fps_indices = fps_sampler.fit(X, initial_subset=[initial_sub], b_samples=max(trainig_set_sizes))
            idx_test = list(np.arange(X.shape[0]))
            save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes, fps_indices, idx_test)    

    if 'RDM' in strategies:
        print('RDM')
        grp = f.create_group(f'RDM')
        for i in tqdm(range(len(initial_conditions))):
                random.seed(i)
                j = i+1
                subgrup_train = grp.create_group(f'train_Initialize_{j}')
                subgrup_test = grp.create_group(f'test_Initialize_{j}')
                idx_test = list(np.arange(X.shape[0]))
                random_indices = random.sample(idx_test, max(trainig_set_sizes))
                save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes, random_indices, idx_test)    

    if 'k-medoids++' in strategies:
        print('k-medoids++') 
        grp = f.create_group(f'k-medoids++')
        for count, _ in  tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            idx_test = list(np.arange(X.shape[0]))
            for n in trainig_set_sizes:
                kmedoids_sampler = Kmedoids(b_samples=n, init='k-medoids++', metric='euclidean', random_state=count)
                kmedoids_indices = kmedoids_sampler.fit(X)
                idx_train = kmedoids_indices
                idx_test_selected=  list(set(idx_test).difference(idx_train)) 
                subgrup_train.create_dataset(f'selected_{n}', data = idx_train) 
                subgrup_test.create_dataset(f'selected_{n}', data = idx_test_selected)

    if 'FacilityLocation' in strategies:
        print('FacilityLocation')
        grp = f.create_group(f'FacilityLocation')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')   
            facility_location_sampler = FacilityLocation(initial_subset=[initial_sub], b_samples=max(trainig_set_sizes), metric='euclidean', verbose=False, n_jobs=-1)
            facility_location_indices = facility_location_sampler.fit(X)
            idx_test = list(np.arange(X.shape[0]))
            save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes,  facility_location_indices, idx_test)    

    if 'Twinning' in strategies:
        print('Twinning')
        grp = f.create_group(f'Twinning')
        for count, initial_sub in  tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            idx_test = list(np.arange(X.shape[0]))
            for n, ratio in zip(trainig_set_sizes, ratios):
                twin_sampler = Twin(ratio=ratio, idx_initial_point=initial_sub)
                idx_train = twin_sampler.fit(X)
                idx_test=  list(set(idx_test).difference(idx_train)) 
                subgrup_train.create_dataset(f'selected_{n}', data = idx_train) 
                subgrup_test.create_dataset(f'selected_{n}', data = idx_test)
                
    if 'FPS-k-medoids++' in strategies and mu!=0:
        print('FPS-k-medoids++')
        grp = f.create_group(f'FPS-k-medoids++')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            idx_test = list(np.arange(X.shape[0]))
            for n in  trainig_set_sizes:
                modified_sampler = FPS_plus(method='kmedoids', mu=mu)
                idx_train = modified_sampler.fit(X, initial_subset=[initial_sub], b_samples=n, random_state=count)
                idx_test=  list(set(idx_test).difference(idx_train)) 
                subgrup_train.create_dataset(f'selected_{n}', data = idx_train) 
                subgrup_test.create_dataset(f'selected_{n}', data = idx_test)
                
    if 'FPS-FacLoc' in strategies  and mu!=0:
        print('FPS-FacLoc')
        grp = f.create_group(f'FPS-FacLoc')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            modified_sampler = FPS_plus(method='facility_location', mu=mu)
            modified_indices = modified_sampler.fit(X, initial_subset=[initial_sub], b_samples=max(trainig_set_sizes))
            idx_test = list(np.arange(X.shape[0]))
            save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes,  modified_indices, idx_test) 

    if 'FPS-RDM' in strategies  and mu!=0:
        print('FPS-random splits')
        grp = f.create_group(f'FPS-RDM')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')
            modified_sampler = FPS_plus(method='random', mu=mu)
            modified_indices = modified_sampler.fit(X, initial_subset=[initial_sub], b_samples=max(trainig_set_sizes), random_state=count-1)
            idx_test = list(np.arange(X.shape[0]))
            save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes,  modified_indices, idx_test)     

    if 'FacLoc-G' in strategies:
        print('FacLoc-G')
        grp = f.create_group(f'FacLoc-G')
        for count, initial_sub in tqdm(enumerate(initial_conditions, 1)):
            subgrup_train = grp.create_group(f'train_Initialize_{count}')
            subgrup_test = grp.create_group(f'test_Initialize_{count}')   
            facility_location_sampler = FacilityLocation(initial_subset=[initial_sub], b_samples=max(trainig_set_sizes), metric='Gaussian', verbose=False, n_jobs=-1)
            facility_location_indices = facility_location_sampler.fit(X, gamma=gamma_FacLocG)
            idx_test = list(np.arange(X.shape[0]))
            save_indices_to_h5py(subgrup_train, subgrup_test, trainig_set_sizes,  facility_location_indices, idx_test)    

    f.close()