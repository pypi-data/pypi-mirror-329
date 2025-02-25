from typing import Union
from .ptyping import FlatDict, NestedDict

def unflat(flat_dict: FlatDict) -> NestedDict:
    nested_dict: NestedDict = {}
    for key, value in flat_dict.items():
        main_key, sub_key = key.split('/')

        try:
            nested_dict[main_key][sub_key] = value
        except KeyError:
            nested_dict[main_key] = {sub_key: value}
    
    return nested_dict

def unflat_keys(flat_keys):
    nested_keys = {}
    for key in flat_keys:
        main_key, sub_key = key.split('/')

        try:
            nested_keys[main_key].append(sub_key)
        except KeyError:
            nested_keys[main_key] = [sub_key]
    
    return nested_keys

def is_nested(dictionary: Union[FlatDict, NestedDict]) -> bool:
    return any(isinstance(value, dict) for value in dictionary.values())
