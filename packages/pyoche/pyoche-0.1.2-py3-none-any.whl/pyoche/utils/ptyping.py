from typing import NewType, MutableMapping
import numpy.typing as npt

NestedName = NewType('NestedName', str)
FlatDict = MutableMapping[NestedName, npt.ArrayLike]
NestedDict = MutableMapping[str, MutableMapping[str, npt.ArrayLike]]