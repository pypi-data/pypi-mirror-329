from setuptools import setup, find_packages

setup(
    name='PAsampling',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'numpy<2.0.0',
        'ipywidgets',
        'tqdm',
        'scipy',
        'scikit-learn',
        'h5py',
        'apricot-select==0.6.0',
        'scikit-learn-extra==0.2.0',
        'matplotlib',
        'seaborn',
        'pandas',
        'twinning',
        'requests'
    ],

    author='Paolo Climaco',
    author_email='climaco@ins.uni-bonn.de',
    description='A library for passive data sampling implementing existing and novel algorithms',
    url='https://github.com/PaClimaco/PAsampling',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License", 
        'Operating System :: OS Independent',
    ],
    license_files=['LICENSE']
)
