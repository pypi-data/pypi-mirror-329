# Passive Sampling (PAsampling)
This is a project funded  by the [Rhine-Ruhr Center for Scientific Data Literacy](https://www.dkz2r.de/) (DKZ.2R),which is one the eleven Data Literacy Centers in Germany. The goal of DKZ.2R reduce data-related hurdles in research, train and support researchers in methodological data literacy in a holistic way, and promote data-competent scientists. 

## Overview
Passive Sampling (PAsampling) is a repository designed to provide easy and fast access to existing and novel tools and resources for data sampling. This project aims to facilitate the implementation of data sampling techniques and provide insights on key aspects of data selection in machine learning, with a particular focus on training data selection for optimizing regression model performance. The term "Passive" refers to the fact that the library mainly focuses on selection approaches that rely solely on data feature representations and do not involve any active learning procedures, which require iterative learning of one or several models. Additionally, the library provides tools for creating machine learning experiment pipelines.

## Documentation

Here is a link to PAsampling's [documentation](https://pasampling.readthedocs.io/en/latest/index.html)

## Features

- PAsampling includes several data sampling methods
    - [Density Aware Farthest Point (DAFPS)](./PAsampling/native_functions/da_fps.py) 
    - [FacilityLocation](./PAsampling/wrappers/facility_location_sampler.py)
    - [Farthest Point Sampling (FPS)](./PAsampling/native_functions/fps.py) 
    - [FPS_plus](./PAsampling/wrappers/modified_samplers.py)
    - [k-medoids++](./PAsampling/wrappers/kmedoids_sampler.py)
    - [Twin](./PAsampling/wrappers/twin_sampler.py)
    
- ML pipeline tools
    - [DataLoader](./PAsampling/utils/data_loader.py)
    - [DataSelector](./PAsampling/utils/data_selection.py)

## Installation

To install the PAsampling package, you can either install it via PyPI or clone the repository and install the required dependencies:

### Install via PyPI
```bash
pip install PAsampling
```

### Install via Git
```bash
git clone https://github.com/PaClimaco/PAsampling.git
cd PAsampling
pip install .
```

## Usage

Here is a basic example of how to use PAsampling:

```python
from PAsampling import *
# Example usage (Farthest Point Sampling on QM dataset)

datasets =  DataLoader('./data') # data_loader function
x, labels = datasets.QM7_dataset()
fps_sampler = FPS() # FPS sampler class
fps_indices = fps_sampler.fit(x, initial_subset=[0], b_samples= 100) # Fit FPS to data matrix
```

## Tutorials
Explore the tutorials to learn how to use the PAsampling library tools and gain key insights into data sampling in machine learning.\
    -[Basic key concepts](./PAsampling/Tutorials/basic_concepts.ipynb)\
    -[Training data selection for regression model performance optimization](./PAsampling/Tutorials/Training_data_selection.ipynb)


## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) to get started. All contributors will be acknowledged and credited.


## Contact

For any questions or inquiries, please contact us at [climaco@ins.uni-bonn.de](mailto:climaco@ins.uni-bonn.de).

## Dependencies
Some of the functions implement in PAsampling are wraps of functions from the following existing libraries:

[Apricot](https://github.com/jmschrei/apricot) MIT License\
[twinning](https://github.com/avkl/twinning) Apache 2.0 License
    



