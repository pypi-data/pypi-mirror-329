from typing import Tuple, Optional, Dict, Type, Mapping, TypeVar, Literal
import numpy as np

from pyoche.dataset import Dataset
from .ml_sample import MlSample
from .normalize import Scaler

D = TypeVar('D', bound='MlDataset')

class MlDataset(Dataset[MlSample]):
    SAMPLE_OBJECT: Type[MlSample] = MlSample

    def split(self, 
              train_ratio: float=0.8, 
              val_ratio: Optional[float]=None, 
              seed: Optional[int]=None) -> Tuple[Dataset, ...]:
        if train_ratio <= 0 or train_ratio >= 1:
            raise ValueError('Train ratio must be between 0 and 1')
        if val_ratio is None:
            val_ratio = 1-train_ratio
        if train_ratio + val_ratio > 1:
            raise ValueError(
                'The sum of train and validation ratios must be <= one:'
                f'{train_ratio=}, {val_ratio=}'
            )

        test_ratio = (1-(train_ratio+val_ratio) 
                      if train_ratio + val_ratio < 1 else None)
        
        if seed is not None:
            np.random.seed(seed)
        
        indices = np.arange(len(self))
        np.random.shuffle(indices)
        indices = list(indices)

        train_cut = int(train_ratio*len(self))

        if test_ratio is not None:
            val_cut = train_cut + int(val_ratio*len(self))

            return (self[indices[:train_cut]], 
                    self[indices[train_cut:val_cut]], 
                    self[indices[val_cut:]])
        else:
            return (self[indices[:train_cut]], 
                    self[indices[train_cut:]])

    def split_with(self, mode: Literal['union','intersect']="union", **feature_filters):
        """
        Splits the dataset based on the provided feature filters.
        Parameters:
            mode (str): The mode of splitting, either 'union' or 'intersect'. 
                        'union' returns samples that match any of the filters.
                        'intersect' returns samples that match all of the filters.
                        Default is 'union'.
            feature_filters (dict): A dictionary where keys are feature names (with '__' instead of '/') 
                                    and values are lists of values to filter by.

        Returns:
            tuple: A tuple containing two datasets:
                - The first dataset contains samples that do not match the filters.
                - The second dataset contains samples that match the filters.

        Raises:
            NotImplementedError: If any feature name does not start with 'scalars'.
            NotImplementedError: If the number of feature filters does not match the shape of the values array.

        Examples:
            **the feature names should be passed with '__' instead of '/'**
            >>> dset.split_with('scalars__geometry_number'=[30])
            >>> dset.split_with(
            >>>     'scalars__geometry_number'=[30, 65],
            >>>     'scalars__rotation_speed'=[15000, 12000]
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

        values = self.to_array(*feature_filters.keys()) # type: ignore
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
        
        non_matching_samples = list(np.array(self.samples)[~bool_array])
        matching_samples = list(np.array(self.samples)[bool_array])

        return (
            self.__class__(non_matching_samples), # type: ignore
            self.__class__(matching_samples) # type: ignore
        )

    def fit(self, scaler_dict: Mapping[str, Scaler]) -> Dict[str, Scaler]:
        features = {key: self.to_array(key) # type: ignore
                    for key in scaler_dict.keys()}
        return {
            key: value.fit(features[key])
            for key, value in scaler_dict.items()
        }

    def fit_normalize(self, scaler_dict: Dict[str, Scaler]) -> 'MlDataset':
        features = {key: self.to_array(key)  # type: ignore
                    for key in scaler_dict.keys()}

        for key, value in scaler_dict.items():
            value.fit(features[key])
        
        return self.normalize(scaler_dict)
        
    def normalize(self, scaler_dict: Dict[str, Scaler]) -> 'MlDataset':
        normalized_sample_list = []
        for sample in self:
            normalized_sample_list.append(sample.normalize(scaler_dict))
        
        return MlDataset(normalized_sample_list)
