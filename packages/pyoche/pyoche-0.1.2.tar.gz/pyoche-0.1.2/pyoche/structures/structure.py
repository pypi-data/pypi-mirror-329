from abc import ABC, abstractmethod
from pyoche.array import Array
import numpy as np
import numpy.typing as npt
from h5py import Group # type: ignore # no typing module in h5py

from typing import Dict, Tuple, TypeVar, Type, Optional, Union, List

Struct = TypeVar('Struct', bound='Structure')

class Structure(ABC):
    GROUP_NAME: str = ''
    REQUIRED: Union[Tuple[str], Tuple[()]] = ()

    def __init__(self) -> None:
        self._elements: Dict[str, Array] = {}
        if self.GROUP_NAME == '':
            raise NotImplementedError('The group name of the'
                                      ' structure must be defined')

    def __getitem__(self, name: str) -> Array:
        if name not in self._elements:
            raise KeyError(f'Element "{name}" not found in the structure')
        return self._elements[name]

    def __setitem__(self, name: str, value: npt.ArrayLike) -> None:
        try:
            self._elements[name] = Array(value)
        except ValueError:
            raise ValueError(f'Cannot convert value to Array for element "{name}"')

    def __delitem__(self, name: str) -> None:
        del self._elements[name]
    
    def __iter__(self):
        return iter(self._elements.items())

    @classmethod
    def from_elements(cls: Type[Struct], **elements: npt.ArrayLike) -> Struct:
        self = cls()
        for key, value in elements.items():
            self[key] = value
        return self

    @classmethod
    def from_h5group(cls: Type[Struct], instance: Group, *groups) -> Struct:
        if groups:
            return cls.from_elements(
                **{name: instance[name][()] for name in groups} # type: ignore
            )
        
        return cls.from_elements(
            **{name: instance[name][()] for name in instance} # type: ignore
        )

    @property
    @abstractmethod
    def shape(self):
        ...


class PointCloudField(Structure):
    GROUP_NAME: str = 'point_cloud_field'

    @property
    def shape(self):
        c_shape = self._elements[list(self._elements.keys())[0]].shape
        n_features = sum(
            [value.shape[0] for value in self._elements.values()]
        )
        return (n_features, *c_shape[1:])
    
    # def to_array(self, keys: Optional[List[str]]=None):
    #     if keys is None:
    #         keys = list(self._elements.keys())
    #     arrays = [self._elements[key] for key in keys]
    #     if not all(a.shape[1] == arrays[0].shape[1] for a in arrays):
    #         raise ValueError('All arrays must have the same number of columns for stacking')
    #     return np.vstack(arrays) 


class Scalar(Structure):
    GROUP_NAME: str='scalars'

    @property
    def shape(self):
        return (len(self._elements),)

class Mesh(Structure):
    GROUP_NAME: str = 'mesh'

    def __init__(self):
        super().__init__()

    @classmethod
    def from_elements(cls, *args, **kwargs):
        self = super().from_elements(*args, **kwargs)
        try:
            self['edges']
            self['points']
        except KeyError:
            raise KeyError(
                'To be defined, a mesh should contain \'edges\' and \'points\''
            )
        return self

    @property
    def shape(self):
        c_shape = self._elements[list(self._elements.keys())[0]].shape
        n_features = sum(
            [value.shape[0] for value in self._elements.values()]
        )
        return (n_features, *c_shape[1:])
    
    @property
    def edges(self):
        return self['edges'] 

    @property
    def points(self):
        return self['points'] 

    @property
    def n_cells(self):
        return self.edges.shape[0] # type: ignore

    

STRUCTURES: Dict[str, Type[Structure]]= {
    'point_cloud_field': PointCloudField,
    'scalars': Scalar,
    'mesh': Mesh
}