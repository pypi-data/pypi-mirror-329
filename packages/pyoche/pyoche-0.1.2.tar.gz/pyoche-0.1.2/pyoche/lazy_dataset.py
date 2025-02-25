from typing import List, Optional, Union, Iterable, TypeVar, Type, overload, Iterator, Generic
from pathlib import Path
from tqdm import tqdm
import numpy as np
from concurrent.futures import ThreadPoolExecutor
# from functools import lru_cache

from .sample import Sample
from .array import Array
from .utils.harmonizers import none_harmonizer
from .utils.ptyping import NestedName

S = TypeVar('S', bound=Sample)
D = TypeVar('D', bound='LazyDataset')

class LazyDataset(Generic[S]):
    SAMPLE_OBJECT: Type[S] = Sample # type: ignore

    def __init__(self, samples: Optional[List[Union[str, Path]]] = None) -> None:
        self.samples: List[Path] = []

        if samples is not None:
            self.add_samples(samples)

    @overload
    def __getitem__(self, idx: np.integer) -> S: ...
    @overload
    def __getitem__(self, idx: NestedName) -> Array: ...
    @overload
    def __getitem__(self: D, idx: Union[slice, Iterable[int]]) -> D: ...
    def __getitem__(self: D, idx: Union[int, slice, Iterable[int], NestedName]) -> Union[S, D, Array]: # type: ignore
        if isinstance(idx, slice):
            return self.__class__(self.samples[idx]) # type: ignore
        elif isinstance(idx, str):
            return self.to_array(idx)
        elif isinstance(idx, (np.integer, int)):
            return self.load_sample(int(idx))
        elif isinstance(idx, Iterable):
            selected_samples = [self.samples[i] for i in idx] # type: ignore
            return self.__class__(selected_samples) # type: ignore
        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    # @lru_cache
    def load_sample(self, idx: int, *groups) -> S:
        sample_path = self.samples[idx]
        return self.SAMPLE_OBJECT.from_file(sample_path, *groups)

    # @lru_cache
    def load_samples(self, indices: Iterable[int], *groups) -> List[S]:
        sample_paths = [self.samples[idx] for idx in indices]
        
        def mk_sample(path):
            return self.SAMPLE_OBJECT.from_file(path, *groups)
        
        samples = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_results = executor.map(mk_sample, sample_paths)
            for result in tqdm(future_results, total=len(sample_paths), desc="Loading samples"):
                samples.append(result)
        return samples

    def __len__(self) -> int:
        return len(self.samples)

    def __iter__(self) -> Iterator[S]:
        for idx in range(len(self)):
            yield self.load_sample(idx)

    def __contains__(self, item: S) -> bool:
        return any(item == self.load_sample(idx) for idx in range(len(self)))

    @classmethod
    def from_folder(
        cls: Type[D],
        folder: Union[str, Path],
        load_subset: Optional[Union[int, tuple]] = None
    ) -> D:
        instance = cls()
        folder_path = Path(folder)

        files = [file for file in folder_path.iterdir() if file.suffix == ".h5"]
        files.sort(key=lambda f: f.name)
        if load_subset is not None:
            if isinstance(load_subset, tuple):
                files = files[slice(*load_subset)] # type: ignore
            else:
                files = files[:load_subset]

        instance.add_samples(files) # type: ignore
        return instance

    def to_array(self, *feature_names: str, harmonizer=none_harmonizer()) -> Array:
        feature_arrays = {feature_name: [] for feature_name in feature_names}
        
        indices = range(len(self.samples))
        
        samples = self.load_samples(indices, *feature_names)
        
        for sample in samples:
            for feature_name in feature_names:
                feature_arrays[feature_name].append(sample[feature_name])
        
        arrays = []
        for feature_name in feature_names:
            concatenated_array = harmonizer(Array(feature_arrays[feature_name]).dd)
            arrays.append(concatenated_array)
        
        combined_array = np.hstack(arrays)
        return Array(combined_array)

    def get_shape(self, *feature_names: NestedName) -> tuple:
        total_samples = len(self)
        if total_samples == 0:
            return (0, 0)
        sample = self.load_sample(0)
        feature_dims = sum(sample[feature].shape[0] for feature in feature_names)
        return (total_samples, feature_dims)

    def add_samples(self, samples: List[Union[str, Path]]) -> None:
        if not isinstance(samples, list):
            raise TypeError("`samples` should be of type `list`")

        for sample in samples:
            if isinstance(sample, str):
                sample = Path(sample)
            if not isinstance(sample, Path):
                raise TypeError("Samples should be of type `str` or `Path`")
            if not sample.is_file():
                raise FileNotFoundError(f"File not found: {sample}")
            if sample.suffix != ".h5":
                raise TypeError(f"Invalid file extension for file: {sample}")
            self.samples.append(sample.resolve())

    def remove_samples(self, indices: List[int]) -> None:
        for i in sorted(indices, reverse=True):
            del self.samples[i]

    def save_h5file(self, folder_path: Union[str, Path]) -> None:
        p = Path(folder_path)
        p.mkdir(exist_ok=True, parents=False)

        for idx in tqdm(range(len(self.samples)), desc="Saving samples"):
            sample = self.load_sample(idx)
            sample.save_h5file(p.joinpath(sample.name))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(num_samples={len(self)})"

    def update(self, samples):
        """trick method to create a new dataset in place. Useful if
        processing samples and adding new elements on the fly while 
        not being able to return/pass new dataset. (used in callbacks)
        """
        self.__init__(samples)
