from abc import ABC, abstractmethod
import numpy as np
from functools import wraps
from typing import Union, Tuple, TypeVar, Type, Callable, Any, cast, Optional, List, Iterable

S = TypeVar('S', bound='Scaler')
F = TypeVar('F', bound=Callable[..., Any])

class Scaler(ABC):
    SCALING_ATTRS: Union[Tuple[str, ...], Tuple[()]] = ()
    SCALER_NAME: str = "Default class scaler"

    def __init__(self) -> None:
        self.is_fitted: bool = False
        for attr in self.SCALING_ATTRS:
            setattr(self, attr, None) 
        
    def __repr__(self) -> str:
        return f"{self.SCALER_NAME} with " + ", ".join(
            (f"{attr}: {getattr(self, attr)}" for attr in self.SCALING_ATTRS)
        )

    @classmethod
    def from_attrs(cls: Type[S], **attrs: Union[int, float, np.ndarray]) -> S:
        instance = cls()
        for attr, value in attrs.items():
            if attr in cls.SCALING_ATTRS:
                setattr(instance, attr, value)
            else:
                raise ValueError(
                    f"{attr} is not a settable attribute of the "
                    f"specified scaler: {value}"
                )
        instance.is_fitted = True
        return instance


    def check_fit(func: F) -> F: # type: ignore # cannot set decorator as staticmethod
        @wraps(func)
        def wrapper(self: "Scaler", *args: Any, **kwargs: Any) -> Any:
            if not self.is_fitted:
                raise ValueError("The normalizer must be fitted to data first.")
            return func(self, *args, **kwargs)

        return cast(F, wrapper)

    def _reshape_for_fit(self, X: np.ndarray) -> np.ndarray:
        """
        Whether the data is a structured grid with multiple channels in the form
        (N, C, H, W), an unstructured point cloud (N, F, Np), a vector (N, F) or 
        a scalar (N), the data can be reshaped to ([CF], N*Np*H*W). This way, 
        the normalization is conducted along the second axis: the channels/
        features are normalized independently.

        N: number of samples
        C, F: number of channels/features
        H, W: height/width
        Np: number of points in point cloud 
        """

        # first reshaping X to feature 3 dimensions regardless of the initial
        # shape: -> (N, F, Np)
        # atleast_2d transposed is to account for scalars (N)
        self._os = X.shape
        X = X.reshape(*np.atleast_2d(X.T).T.shape[:2], -1)
        self._os3D = X.shape

        # transposing F to be the first axis and flattening the last two
        # last .T to enable clearer implementations of the transform and fit
        return X.transpose((1, 0, 2)).reshape(X.shape[1], -1).T
    
    def _inverse_reshape(self, X: np.ndarray) -> np.ndarray:
        N, F, Np = self._os3D
        X = X.T.reshape(F, N, Np).transpose(1, 0, 2)
        return X.reshape(self._os)

    def fit(self: S, X: np.ndarray, exclude_channels: Optional[Union[list, np.ndarray]]=None) -> S:
        X = self._reshape_for_fit(X)
        self._fit(X, exclude_channels)
        self.is_fitted = True
        return self

    @abstractmethod
    def _fit(self, X: np.ndarray, exclude_channels: Optional[Union[list, np.ndarray]]=None) -> None:
        raise NotImplementedError(
            "`_fit` method must be implemented for child object to be valid."
        )

    @check_fit
    def transform(self, X: np.ndarray) -> np.ndarray:
        X = self._reshape_for_fit(X)
        return self._inverse_reshape(self._transform(X))

    def fit_transform(self, X: np.ndarray, exclude_channels: Optional[Union[list, np.ndarray]]=None):
        X = self._reshape_for_fit(X)

        self._fit(X, exclude_channels)
        self.is_fitted = True

        return self._inverse_reshape(self._transform(X))

    @abstractmethod
    def _transform(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            "`_transform` method must be implemented for child object to be valid."
        )

    # @check_dim
    @check_fit
    def inverse(self, X: np.ndarray) -> np.ndarray:
        X = self._reshape_for_fit(X)
        return self._inverse(self._inverse_reshape(X))

    @abstractmethod
    def _inverse(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            "`_inverse` method must be implemented for child object to be valid."
        )

    def concat(self, *others: 'Scaler'):
        others_lst: Iterable[Scaler] = list(others)
        for i, other in enumerate(others_lst):
            if not type(self) == type(other):
                others_lst[i] = other.to(type(self))
        
        return self.__class__.from_attrs(
            **{attr: np.hstack([
                getattr(scaler, attr) 
                for scaler in [self]+others_lst]) 
            for attr in self.SCALING_ATTRS})
    
    def to(self, type_other: Type[S]) -> S:
        if isinstance(self, type_other):
            return self
        else:
            raise NotImplementedError(
                f'Casting to {type_other} not implemented '
                'or not possible')


class IdScaler(Scaler):
    """
    Identity scaler
    """

    SCALING_ATTRS = ()
    SCALER_NAME = "Identity scaler"
    def __init__(self) -> None:
        super().__init__()
        self.is_fitted = True

    def _fit(self, X, exclude_channels = None):
        pass

    def _transform(self, X):
        return X

    def _inverse(self, X):
        return X
    
    def to(self, type_other: Type[S]) -> S:
        if isinstance(self, type_other):
            return self
        elif type_other==StdScaler:
            return type_other.from_attrs(mean=0, scale=1)
        else:
            raise NotImplementedError(
                f'Casting to {type_other} not implemented '
                'or not possible')

class StdScaler(Scaler):
    """
    Mean-standard scaler: (x - mean) / std_deviation
    """

    SCALING_ATTRS = ("mean", "scale")
    SCALER_NAME = "Mean-Standard scaler"

    def _fit(self, X: np.ndarray, exclude_channels: Optional[Union[list, np.ndarray]]=None):
        if exclude_channels is None:
            exclude_channels = []

        self.mean = np.mean(X, axis=0)
        self.scale = np.sqrt(np.var(X, axis=0))

        self.mean[self.scale == 0] = 0
        self.scale[self.scale == 0] = 1

        self.mean[exclude_channels] = 0
        self.scale[exclude_channels] = 1

    def _transform(self, X: np.ndarray) -> np.ndarray:
        return (X - self.mean) / self.scale

    def _inverse(self, X: np.ndarray) -> np.ndarray:
        return X * self.scale + self.mean



class MinMaxScaler(Scaler):
    """
    Min-max scaler:
    """

    SCALING_ATTRS = ("min", "max")
    SCALER_NAME = "Min-max scaler"

    def _fit(self, X, exclude_channels=None):
        if exclude_channels is None:
            exclude_channels = []

        self.min = np.min(X, axis=0)
        self.max = np.max(X, axis=0)

        self.min[self.min == self.max] = 0
        self.max[0 == self.max] = 1

        self.min[exclude_channels] = 0
        self.max[exclude_channels] = 1

        return self

    def _transform(self, X):
        return (X - self.min) / (self.max - self.min)

    def _inverse(self, X):
        return X * (self.max - self.min) + self.min

class CenteredMinMaxScaler(MinMaxScaler):
    """
    Min-max scaler centered around 0 and ranging from -1 to 1:
    """

    SCALING_ATTRS = ("min", "max")
    SCALER_NAME = "Centered min-max scaler"

    def _fit(self, X, exclude_channels=None):
        if exclude_channels is None:
            exclude_channels = []

        self.min = np.min(X, axis=0)
        self.max = np.max(X, axis=0)

        self.min[(self.max - self.min) == 1], self.max[(self.max - self.min) == 1] = (
            0,
            3,
        )

        self.min[exclude_channels] = 0
        self.max[exclude_channels] = 3

        return self

    def _transform(self, X):
        return 2 * (X - self.min) / (self.max - self.min) - 1

    def _inverse(self, X):
        return (X + 1) * (self.max - self.min) / 2 + self.min

def scaler_from_keys(scaler_dict, *keys):
    if len(keys[0]) == 0:
        raise ValueError('Missing keys, at least one must be provided')
    try:
        return scaler_dict[keys[0]].concat(
            *[scaler_dict[key] for key in keys[1:]]
        )
    except IndexError:
        return scaler_dict[keys[0]]