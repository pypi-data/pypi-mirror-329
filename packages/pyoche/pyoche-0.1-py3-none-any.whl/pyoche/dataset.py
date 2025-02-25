"""
Module for dataset handling and operations.

This module defines the Dataset class that encapsulates a collection of samples,
providing methods to index, iterate, filter, load from folders, and save samples
as HDF5 files.
"""

from pathlib import Path
from typing import Iterable, List, Optional, Union, TypeVar, Type, Generic, overload
from concurrent.futures import ThreadPoolExecutor
import numpy as np 

from tqdm import tqdm

from .sample import Sample
from .array import Array
from .utils.harmonizers import none_harmonizer
from .utils.ptyping import NestedName

S = TypeVar('S', bound=Sample)
D = TypeVar('D', bound='Dataset')

class Dataset(Generic[S]):
    """
    Class representing a collection of samples.
    
    This dataset supports conventional Python sequence operations and also provides
    specialized methods for converting feature sets into combined numpy arrays, updating
    samples in place, and saving sample data to disk.
    
    Attributes:
        samples (List[S]): The list containing sample instances.
        is_constant_len (dict): Mapping indicating whether each feature is of a constant length 
                                across all samples.
    """
    SAMPLE_OBJECT: Type[S] = Sample  # type: ignore

    def __init__(self, samples: Optional[Iterable[S]] = None) -> None:
        """
        Initialize the Dataset with an optional iterable of samples.
        
        Args:
            samples (Optional[Iterable[S]]): An iterable of sample objects. Each sample is
                                             expected to be an instance of SAMPLE_OBJECT.
        """
        self.samples: List[S] = []
        self.is_constant_len = {}

        if samples is not None:
            self.add_samples(samples)
    
    @overload
    def __getitem__(self, idx: int) -> S: ...
    @overload
    def __getitem__(self, idx: NestedName) -> Array: ...
    @overload
    def __getitem__(self: D, idx: Union[slice, Iterable[int], Iterable[bool]]) -> D: ...
    def __getitem__(self: D, idx: Union[slice, Iterable, int, NestedName]) -> Union[S, D, Array]:
        """
        Retrieve one or more samples or feature data from the dataset.
        
        Depending on the type of idx:
          - An integer returns the sample at that index.
          - A slice or iterable returns a new Dataset with selected samples.
          - A string (or NestedName) returns an Array of feature data from all samples.
        
        Args:
            idx (Union[int, slice, Iterable, NestedName]): An index, slice, iterable of indices/booleans,
                       or feature name to select data.
        
        Returns:
            S, D, or Array: A single sample, a new Dataset instance, or a feature Array.
        
        Raises:
            TypeError: If the index type is not recognized.
        """
        if isinstance(idx, slice):
            return self.__class__(self.samples[idx])
        elif isinstance(idx, str):
            return self.to_array(idx) # type: ignore
        elif isinstance(idx, Iterable):
            if all(isinstance(i, (bool, np.bool_)) for i in idx):
                return self.__class__([s for s, b in zip(self.samples, idx) if b])
            return self.__class__(list(map(self.samples.__getitem__, idx)))
        elif isinstance(idx, int):
            return self.samples[idx]
        else:
            raise TypeError(f"Invalid index type: {type(idx)}")
    
    def __iter__(self: D) -> D:
        """
        Return an iterator over the dataset samples.
        """
        self._iterator = 0
        return self
    
    def __next__(self) -> S:
        """
        Return the next sample in the dataset during iteration.
        
        Returns:
            The next sample.
        """
        try:
            self._iterator += 1
            return self[self._iterator-1]
        except IndexError:
            raise StopIteration

    def __contains__(self, element: S) -> bool:
        """
        Check if a sample is in the dataset.
        
        Args:
            element (S): A sample object.
        
        Returns:
            bool: True if present, False otherwise.
        """
        return element in self.samples

    def __len__(self) -> int:
        """
        Return the number of samples in the dataset.
        
        Returns:
            int: The number of samples.
        """
        return len(self.samples)

    @classmethod
    def from_folder(
        cls: Type[D], 
        folder: Union[str, Path], 
        load_subset: Optional[Union[int, tuple]] = None
    ) -> D:
        """
        Create a dataset from HDF5 files in a folder.
        
        Args:
            folder (Union[str, Path]): The folder path.
            load_subset (Optional[Union[int, tuple]]): Option to load a subset of files. 
                                                        If an integer is provided, the first N files
                                                        will be loaded. If a tuple is provided, the
                                                        slice will be used to load files.
        
        Returns:
            Dataset: A new dataset instance.
        """
        instance = cls()
        samples: Optional[List[S]] = list()

        files = [file for file in (Path(folder)).iterdir() if file.suffix == ".h5"]
        files.sort(key=lambda f: f.name)
        files = (
            files[slice(*load_subset)] #type: ignore
            if isinstance(load_subset, tuple) 
            else files[slice(load_subset)]
        )

        def mk_sample(fname: Path):
            return cls.SAMPLE_OBJECT.from_file(fname.resolve())

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_results = executor.map(mk_sample, files)

            for result in tqdm(
                future_results, 
                total=len(files), 
                desc="Opening files in folder"
            ):
                samples.append(result)

        instance.add_samples(samples)

        return instance

    def to_array(self, *feature_names: NestedName, harmonizer=none_harmonizer()) -> Array:
        """
        Convert the dataset features to a combined array.
        
        Args:
            feature_names: Names of features to include.
            harmonizer: Function to harmonize the feature arrays. 
                        This function will help in reshaping the feature arrays 
                        before combining them.
        
        Returns:
            Array: A numpy array of combined features.
        """
        def _to_array(feature_name: NestedName, samples) -> Array:
            return Array(list(map(lambda x: x[feature_name], samples))).dd

        def _vlen_to_array(feature_name, samples):
            return Array(np.vstack(list(map(
                lambda x: x[feature_name].reshape(x[feature_name].shape[0], -1).T,
                samples
            ))))

        if any([not self.is_constant_len[key] for key in feature_names]):
            _fn = _vlen_to_array
        else:
            _fn = _to_array
        
        harmonizer = none_harmonizer() if harmonizer is None else harmonizer

        return Array(np.hstack([
            harmonizer(_fn(feature_name, self.samples))
            for feature_name in feature_names
        ]))
    
    def get_shape(self, *feature_names: NestedName):
        """
        Get the shape of the dataset for the given features.
        
        Args:
            feature_names: Names of features.
        
        Returns:
            tuple: A tuple representing the dataset shape.
        """
        return len(self), sum([self[0][feature].shape[0] 
                               for feature in feature_names])

    def add_samples(self, samples: Iterable[S]) -> None:
        """
        Add samples to the dataset.
        
        Args:
            samples (Iterable[S]): An iterable of samples to add.
        """
        if not isinstance(samples, list):
            raise TypeError("`samples` should be of type `list`")

        if not all(isinstance(x, self.SAMPLE_OBJECT) for x in samples):
            raise TypeError(
                "At least one sample from the list is not of the right type"
            )
        
        if samples:  # update constant length only if there is at least one sample
            if not self.is_constant_len:
                for key in samples[0].keys():
                    self.is_constant_len[key] = True

            for key, value in self.is_constant_len.items():
                if value:
                    try:
                        os = self.samples[0][key].shape
                    except IndexError:
                        os = samples[0][key].shape
                    for sample in samples:
                        if sample[key].shape != os:
                            self.is_constant_len[key] = False
                            break

        self.samples.extend(samples)

    def update(self, samples):
        """
        Update the dataset samples in place.
        
        This method is useful when processing samples on the fly.
        
        Args:
            samples: New list of sample objects.
        """
        self.__init__(samples)

    def save_h5file(self, folder_path: Union[str, Path]) -> None:
        """
        Save each sample of the dataset as individual HDF5 files.
        
        Creates the target folder if it does not exist. Writes each sample into a separate
        HDF5 file using the sample's name as the filename. The HDF5 file structure mirrors the 
        sample's internal structure with groups and datasets.
        
        Args:
            folder_path (Union[str, Path]): Path to the folder where HDF5 files will be saved.
        
        Raises:
            IOError: If there is an issue creating the folder or writing files.
        """
        p = Path(folder_path)
        p.mkdir(exist_ok=True, parents=True)
        
        for sample in self.samples:
            sample.save_h5file(
                p.joinpath(Path(sample.name).name)
            )
