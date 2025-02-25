# Pyoche

Pyoche is a python library to write (CFD/numerical) data in pre-defined structured ways using the HDF5 file format. A number of utils is then provided to use those files as data in a machine/deep learning workflow (normalization, splitting, visualization, etc...)



## Installation guide

### Python 3.8+

### With pip
```
pip install pyoche
```

### Required packages are listed in the ```setup.py``` file:

- ```numpy```
- ```h5py```
- ```pathlib```
- ```mathplotlib```


## Using Pyoche

### Saving data in the pyoche formalism

Data can be saved in the pyoche formalism using the `Sample` class. Here's a minimal example:

```python
from pyoche import Sample
import numpy as np

# Method 1: Using nested dictionaries
# Note: First axis of each field must be the number of features
point_cloud = {
    'coordinates': np.random.rand(3, 1000),  # 3D coordinates (x,y)
    'velocity': np.random.rand(3, 1000),     # 3D velocity field (vx,vy,vz)
}

scalars = {
    'reynolds_number': np.array([1000.0]),   # Global parameters
    'mach_number': np.array([0.3])
}

sample = Sample.from_dict({
    'point_cloud_field': point_cloud,
    'scalars': scalars
})

# Method 2: Using flat dictionary with path-like keys
flat_dict = {
    'scalars/pressure': np.array([101325.0]),
    'scalars/temperature': np.array([300.0]),
    'point_cloud_field/coordinates': np.random.rand(3, 1000),
    'point_cloud_field/velocity': np.random.rand(3, 1000)
}

sample = Sample.from_dict(flat_dict)

# Save the sample
sample.save_h5file('parent/output.h5')
```

This creates an HDF5 file with the proper pyoche structure, which can then be loaded using the methods described below.


### Internal data (HDF5 data which respects one of the specified data structures of pyoche)

A 'sample' ```<name>.h5``` file can be loaded with pyoche using the ```Sample``` object:

```py
sample = Sample.from_file('parent/output.h5')
```

### Manipulating Sample Data

The Sample class provides convenient dictionary-like operations to access and modify data:

```python
# Adding data to a sample
sample['point_cloud_field/new_field'] = np.random.rand(3, 1000)  # Add new field
sample['scalars/new_scalar'] = np.array([42.0])  # Add new scalar

# Accessing data
velocity = sample['point_cloud_field/velocity']  # Get velocity field
pressure = sample['scalars/pressure']  # Get pressure scalar

# Accessing structures
scalars = sample['scalars']  # Get all scalars as a Structures instance
point_cloud = sample['point_cloud_field']  # Get all point cloud data as a Structure

# Creating a new sample from a structure:
s2 = Sample.from_structure(scalars)

# Iterating over fields
for key, value in sample:
    print(f"Field {key} has shape {value.shape}")

# Getting available keys
for key in sample.keys():
    print(f"Available field: {key}")

# Check if a field exists
if 'scalars/pressure' in sample:
    print("Pressure field exists")
```

### Manipulation through the dataset object

Samples can be grouped into a 'dataset':

```python
from pyoche import Dataset

Dataset([sample])
```

Alternatively, they can be loaded directly from the parent folder:
```py
dataset = Dataset.from_folder('parent/')
```

The Dataset class provides multiple ways to access data:

```python
# Accessing a single sample by index
sample = dataset[0]  # Returns the first Sample object

# Iterating through samples
for sample in dataset:
    print(sample.name)
```

Other indexing methods are also available
```py
# making a dataset with more samples
dataset = Dataset([sample]*10)

# Accessing a range of samples
subset = dataset[0:4]  # Returns a new Dataset with the first 4 samples
filtered = dataset[[0, 2, 5]]  # Returns a Dataset with specific samples
# As well as the possibility to filter samples with a boolean mask
masked = dataset[[True]*9+[False]]

# Direct access to features across all samples
velocities = dataset['point_cloud_field/velocity']  # Returns an Array with all velocities

# Converting multiple features to a combined array
combined = dataset.to_array(
    'point_cloud_field/coordinates',
    'point_cloud_field/velocity'
)  # Returns a concatenated Array of features
```

The `to_array` method is particularly useful for machine learning tasks as it combines features from all samples into a single array.
Using "harmonizer" functions, data of different shapes can be combined on the fly.

### Harmonizer functions

Harmonizers help transform data into consistent shapes. A common use case is converting between different data representations:

Convert temperature to match velocity's point cloud structure. Since harmonizers operate on samples, one more dimension is added to the temperature (Shape: (N_sample, N_features))
```python
temperature = np.array([300.0])  # Global temperature (scalar)
temperatures = temperature[np.newaxis]  # Shape: (1, 1)
```
Same for the velocity
```py
velocity = np.random.rand(3, 1000)  # Point cloud velocity field
velocities = velocity[np.newaxis]  # Shape: (1, 3, 1000)
```

Now combining botht with the "to_upc" harmonizer (upc: unstructured point_cloud, with a shape of (N_features, N_points))

```python
from pyoche.utils.harmonizers import to_upc

harmonizer = to_upc(num_points=1000)
temp_upc = harmonizer(temperatures)  # Shape: (1, 1000) - same temperature at all points
```

Equivalent numpy operation for the harmonizer:

```py
temp_upc_numpy = np.ones((1, 1, 1000)) * temperatures[..., np.newaxis]  # Shape: (1, 1, 1000)
```

Both can be combined directly with to_array by passing the harmonizer in the method
```py
combined = dataset.to_array(
    'point_cloud_field/velocity',
    'scalars/temperature',
    harmonizer=harmonizer
)
# combined shape: (N, 4, 1000)
```

Equivalent numpy operation for the combination:
```py
# velocity shape: (N, 3, 1000)
# temp_upc shape: (N, 1, 1000) 
# combined shape: (N, 4, 1000)
combined_numpy = np.concatenate([velocities, temp_upc], axis=1)  # Joins along feature dimension

```

Other harmonizers like `to_spc` (structured point cloud) and `to_fupc` (flat unstructured point cloud) are available for different data transformation needs.





