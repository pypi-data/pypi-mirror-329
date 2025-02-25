import numpy as np
from typing import Dict

from pyoche.sample import Sample
from .normalize import Scaler

class MlSample(Sample):

    def normalize(self, scaler_dict: Dict[str, Scaler], _raise_missing=True) -> 'MlSample':
        if _raise_missing:
            keys = set(scaler_dict.keys())
        else:
            keys = set(self.keys()).intersection(scaler_dict.keys())

        features = {key: self[key][np.newaxis] for key in keys} # type: ignore

        normalized_flat_dict = {
            key: scaler_dict[key].transform(features[key]).reshape(self[key].shape) # type: ignore
            for key in keys
        }
        return self.__class__.from_dict(normalized_flat_dict) # type: ignore

    def inverse(self, scaler_dict):
        features = {key: self[key][np.newaxis] for key in scaler_dict.keys()}
        inverted_flat_dict = {
            key: value.inverse(features[key]).reshape(self[key].shape)
            for key, value in scaler_dict.items()
        }
        return self.__class__.from_dict(inverted_flat_dict)



