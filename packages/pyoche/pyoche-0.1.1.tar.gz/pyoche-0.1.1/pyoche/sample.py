"""
Module for sample handling.

This module defines the Sample class that encapsulates one or more structures, 
enabling loading from HDF5 files, dictionary-based input, or constructing samples 
from predefined structure objects.
"""

from h5py._hl.files import File
from typing import Optional, Union, Dict, Type, TypeVar, overload, cast
from pathlib import Path
import numpy.typing as npt

from .structures.structure import STRUCTURES, Structure
from .array import Array
from .utils.ptyping import NestedName, FlatDict, NestedDict
from .utils.funcs import unflat, is_nested, unflat_keys

S = TypeVar('S', bound='Sample')

class Sample:
    """
    Represents a sample composed of one or more Structures instances.
    
    The sample organizes structures in a dictionary where each key corresponds
    to a structure name (or a nested key) and each value is an instance of a 
    Structure subclass. Structures can be loaded from file or constructed programmatically.
    
    Attributes:
        _structures (Dict[str, Structure]): Internal mapping from structure names
                                             to their corresponding structure objects.
        name (str): Identifier for the sample, often set as the source filename.
    """
    def __init__(self):
        """
        Initialize a Sample instance.
        
        Ensures that the internal dictionary for storing structures and the sample
        name are properly initialized.
        """
        if not hasattr(self, "_structures"):
            self._structures: Dict[str, Structure] = {}
        if not hasattr(self, "name"):
            self.name: str = ''

    @overload
    def __getitem__(self, name: NestedName) -> Array: ...
    @overload
    def __getitem__(self, name: str) -> Structure: ...
    def __getitem__(self, name: Union[NestedName, str]) -> Union[Array, Structure]:
        """
        Retrieve a structure or corresponding data array using a key.
        
        The key may be a simple string or a nested name (e.g., "group/subgroup").
        Nested keys access specific elements within complex structures.
        
        Args:
            name (Union[NestedName, str]): The identifier for the structure or sub-structure.
        
        Returns:
            Array or Structure: The requested data container.
            
        Note:
            If a nested key is used, the method returns a subset (Array) of the structure.
        """
        if len(subnames := name.split("/")) == 2:
            return self._structures[subnames[0]][subnames[1]]
        return self._structures[name]
    
    @overload
    def __setitem__(self, name: NestedName, value: npt.ArrayLike) -> None: ...
    @overload
    def __setitem__(self, name: str, value: Structure) -> None: ...
    def __setitem__(self, name: Union[NestedName, str], value: Union[npt.ArrayLike, Structure]) -> None:
        """
        Set a structure or array in the sample.
        
        Args:
            name (Union[NestedName, str]): The key or nested name.
            value (Union[npt.ArrayLike, Structure]): The value to set. Must be a Structure for non-nested keys.
        
        Raises:
            KeyError: If the structure is not found.
            TypeError: If the type of value is not appropriate.
        """
        if len(subnames := name.split("/")) == 2:
            if subnames[0] in self._structures:
                self._structures[subnames[0]][subnames[1]] = value # type: ignore
            else:
                raise KeyError(f'Structure "{subnames[0]}" not found in Sample')
        else:
            if isinstance(value, Structure):
                self._structures[name] = value
            else:
                raise TypeError("For a non-nested string key, the value must be an instance of Structure")

    def __iter__(self):
        for struct_name, structure in self._structures.items():
            for element_name, element in structure:
                yield f'{struct_name}/{element_name}', element
    
    def keys(self):
        for struct_name, structure in self._structures.items():
            for element_name, _ in structure:
                yield f'{struct_name}/{element_name}'

    @classmethod
    def from_file(cls: Type[S], fname: Union[str, Path], *groups) -> S:
        data = File(fname, mode="r")
        return cls.from_h5file(data, *groups)

    @classmethod
    def from_h5file(cls: Type[S], instance: File, *groups, _close: bool=True) -> S:
        self = cls()
        self.name = instance.filename

        if groups: 
            selected_groups = set(groups) 
        else: 
            selected_groups = [
                f'{key}/{subkey}' 
                for key in instance.keys() 
                for subkey in instance[key].keys() # type: ignore
            ]

        for group in selected_groups:
            if group not in instance:
                raise KeyError(f"Group '{group}' not found in the HDF5 file.")

        nested_groups = unflat_keys(selected_groups)
        for group, subgroups in nested_groups.items():

            struct_type = "_".join(group.split("_")) # type: ignore
            try:
                self._structures[group] = STRUCTURES[struct_type].from_h5group(
                    instance[group], *subgroups # type: ignore
                )
            except TypeError:
                raise NotImplementedError(
                    'The "from_h5group" classmethod must'
                    " be implemented to use the "
                    f"<{struct_type}> structure"
                )
        if _close:
            instance.close()
        return self

    @classmethod
    def from_dict(cls: Type[S], dictionary: Union[NestedDict, FlatDict]):
        self = cls()
        if is_nested(dictionary):
            dictionary = cast(NestedDict, dictionary)
        else:
            dictionary = unflat(cast(FlatDict, dictionary))

        for group in dictionary:
            struct_type = "_".join(group.split("_"))

            self._structures[group] = STRUCTURES[struct_type].from_elements(
                **dictionary[group]
            )

        return self

    @classmethod
    def from_structure(cls: Type[S], *structures: Structure) -> S:
        self = cls()
        for struct in structures:
            self._structures[struct.GROUP_NAME] = struct

        return self

    def save_h5file(self, fname: Union[str, Path]) -> None:
        """
        Save the sample's structures to an HDF5 file.
        
        This method iterates over all stored structures and writes each one as a group
        in an HDF5 file. Each structure's elements become datasets within their respective group.
        
        Args:
            fname (Union[str, Path]): The filepath for the HDF5 file to write.
        """
        h5f = File(fname, mode="w-")

        for struct_name, struct in self._structures.items():
            tmp = h5f.create_group(struct_name)

            for key, value in struct._elements.items():
                tmp.create_dataset(key, data=value)
    
    def __repr__(self) -> str:
        """
        Generate a string representation of the sample.
        
        Provides a summary of contained fields along with their dimensions.
        
        Returns:
            str: A formatted string with sample details.
        """
        features_shape = [f'\t{key}: {value.shape}\n' for key, value in self]
        return f"{self.__class__.__name__}:\n{''.join(features_shape)}"
