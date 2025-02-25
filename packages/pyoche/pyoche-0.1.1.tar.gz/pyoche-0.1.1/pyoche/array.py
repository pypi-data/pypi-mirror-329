import numpy as np

class Array(np.ndarray):
    def __new__(cls, input_array, *args, **kwargs):
        return np.asarray(input_array, **kwargs).view(cls)

    @property
    def d(self):
        """not strict"""
        if self.ndim == 1:
            return self
        elif self.ndim == 0:
            return self[np.newaxis]
        else:
            if (tmp := np.squeeze(self)).ndim == 1:
                return tmp
            return self
            

    @property
    def dd(self):
        """not strict"""
        if self.ndim == 1:
            return self[:, np.newaxis]
        elif self.ndim == 0:
            return self[np.newaxis, np.newaxis]
        else:
            return self

    @property
    def D(self):
        """strict"""
        if self.ndim == 1:
            return self
        elif self.ndim == 0:
            return self[np.newaxis]
        else:
            if (tmp := np.squeeze(self)).ndim == 1:
                return tmp
            else:
                raise TypeError(f"Truly nD array cannot be squeezed into 1D array.")

    @property
    def DD(self):
        """strict"""
        if self.ndim == 1:
            return self[:, np.newaxis]
        elif self.ndim == 0:
            return self[np.newaxis, np.newaxis]
        elif self.ndim == 2:
            return self
        else:
            raise TypeError(f"array must be of dim 1 or 2 to use DD. Got {self.ndim}")
