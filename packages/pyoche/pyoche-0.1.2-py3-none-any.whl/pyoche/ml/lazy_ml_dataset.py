from typing import Tuple, Optional, Dict, List, Union, Type, Iterable, Mapping, TypeVar
import numpy as np
from pathlib import Path
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from .ml_sample import MlSample
from .normalize import Scaler
from pyoche.lazy_dataset import LazyDataset

S = TypeVar('S', bound=MlSample)
D = TypeVar('D', bound='LazyMlDataset')

class LazyMlDataset(LazyDataset[MlSample]):
    SAMPLE_OBJECT: Type[MlSample] = MlSample

    def __init__(
        self,
        samples: Optional[List[Union[str, Path]]] = None,
        scaler_dict: Optional[Dict[str, Scaler]] = None
    ) -> None:
        super().__init__(samples)
        self.scaler_dict = scaler_dict
        
    def load_sample(self, idx: int, *groups) -> MlSample:
        if self.scaler_dict:
            if groups:
                groups = set(self.scaler_dict.keys()).intersection(*groups)
            else:
                groups = self.scaler_dict.keys()
                
        sample = super().load_sample(idx, *groups)

        if self.scaler_dict:
            sample = sample.normalize(self.scaler_dict)
        return sample

    def load_samples(self, indices: Iterable[int], *groups) -> List[MlSample]:
        indices = list(indices)

        def mk_sample(idx, groups):
            if self.scaler_dict:
                if groups:
                    groups = set(self.scaler_dict.keys()).intersection(groups)
                else:
                    groups = self.scaler_dict.keys()

            sample = super(LazyMlDataset, self).load_sample(idx, *groups)

            if self.scaler_dict:
                sample = sample.normalize(self.scaler_dict, _raise_missing=False)
            return sample
        
        _mk_sample = partial(mk_sample, groups = groups)

        samples = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_results = executor.map(_mk_sample, indices)
            for result in tqdm(future_results, total=len(indices), desc="Loading samples"):
                samples.append(result)
        return samples
        
    def split(
        self,
        train_ratio: float = 0.8,
        val_ratio: Optional[float] = None,
        seed: Optional[int] = None
    ) -> Tuple[LazyDataset, ...]:
        if train_ratio <= 0 or train_ratio >= 1:
            raise ValueError('Train ratio must be between 0 and 1')
        if val_ratio is None:
            val_ratio = 1 - train_ratio
        if train_ratio + val_ratio > 1:
            raise ValueError(
                'The sum of train and validation ratios must be <= 1: '
                f'{train_ratio=}, {val_ratio=}'
            )

        test_ratio = (1 - (train_ratio + val_ratio) 
                      if (train_ratio + val_ratio) < 1 else None)

        if seed is not None:
            np.random.seed(seed)

        indices = np.arange(len(self))
        np.random.shuffle(indices)
        indices = list(indices)

        train_cut = int(train_ratio * len(self))

        if test_ratio is not None:
            val_cut = train_cut + int(val_ratio * len(self))

            return (
                self[indices[:train_cut]], # type: ignore
                self[indices[train_cut:val_cut]],
                self[indices[val_cut:]]
            )
        else:
            return (
                self[indices[:train_cut]], # type: ignore
                self[indices[train_cut:]]
            )

    
    def split_with(self, mode="union", **feature_filters):
        """
        the feature names should be passed with __ instead of /
        >>> dset.split_with(scalars__geometry_number=[30])
        >>> dset.split_with(
        >>>     scalars__geometry_number=[30, 65],
        >>>     scalars__rotation_speed=[15000, 12000]
        >>> )
        """
        feature_filters = {
            key.replace('__', '/'): value 
            for key, value in feature_filters.items()
        }
        if not all([key.startswith('scalars') 
                    for key in feature_filters.keys()]):
            raise NotImplementedError(
                'Only works with scalar filters for now')

        values = self.to_array(*feature_filters.keys())
        if len(feature_filters) != values.shape[1]:
            raise NotImplementedError(
                'Need to implement using nD scalars (vectors) for filtering'
            )

        bool_array = np.empty(values.shape)
        for i, value in enumerate(feature_filters.values()):
            bool_array[:, i] = np.isin(values[:, i], value)

        if mode == 'union':
            bool_array = bool_array.any(axis=1)
        elif mode == 'intersect':
            bool_array = bool_array.all(axis=1)
        else:
            raise ValueError('mode can be either `union` or `intersect`')
        
        non_matching_samples = list(np.array(self.samples)[~bool_array])
        matching_samples = list(np.array(self.samples)[bool_array])

        return (
            self.__class__(non_matching_samples), # type: ignore
            self.__class__(matching_samples) # type: ignore
        )

    def fit(self, scaler_dict: Mapping[str, Scaler]) -> Dict[str, Scaler]:
        features = {key: self.to_array(key) for key in scaler_dict.keys()}
        return {
            key: scaler.fit(features[key])
            for key, scaler in scaler_dict.items()
        }

    def fit_normalize(self, scaler_dict: Dict[str, Scaler]) -> 'LazyMlDataset':
        self.fit(scaler_dict)
        return self.normalize(scaler_dict)

    def normalize(self, scaler_dict: Dict[str, Scaler]) -> 'LazyMlDataset':
        return self.__class__(self.samples, scaler_dict=scaler_dict) #type: ignore


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(num_samples={len(self)})"
