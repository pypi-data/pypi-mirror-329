import numpy as np

def none_harmonizer():
    def fn(arg):
        return arg
    return fn

def to_spc(grid_shape):
    """Converts a scalar, vector or unstructured point cloud (upc) to a
    structured point cloud (spc): (N, C, H, W)"""
    def fn(arg):
        if arg.ndim == 3:
            if grid_shape[0]*grid_shape[1] != arg.shape[-1]:
                raise ValueError('Shape mismatch')
            return arg.reshape((*arg.shape[:2], *grid_shape))
        if arg.ndim >= 4:
            if grid_shape != arg.shape[2:]:
                raise ValueError('Shape mismatch')
            return arg

        return np.ones((
            *arg.DD.shape, 
            *grid_shape
        ))*arg.DD[..., np.newaxis, np.newaxis]
    return fn

def to_upc(num_points=None):
    """
    Converts a structured point cloud (spc), scalars and vectors into an 
    unstructured point cloud (upc): (N, F, Np). 
    """
    def fn(arg: np.ndarray):
        if arg.ndim == 2:
            if num_points is None:
                raise TypeError('num_points arg must be provided as '
                                'scalars/vectors are processed.')
            return np.ones((*arg.shape, num_points))*arg[..., np.newaxis]

        elif arg.ndim == 3:
            if num_points is not None and num_points != arg.shape[-1]:
                raise ValueError('Shape mismatch')
            return arg

        elif arg.ndim >= 4:
            if num_points is not None and num_points != np.prod(arg.shape[2:]):
                raise ValueError('Shape mismatch')
            return arg.reshape(*arg.shape[:2], -1)

        else:
            raise NotImplementedError

    return fn
            
def to_fupc():
    """
    Converts element to flat unstructured point cloud (fupc): (NxNp, F)
    """
    def fn(arg):
        if arg.ndim == 2:
            return arg

        elif arg.ndim == 3:
            pass

        elif arg.ndim >= 4:
            arg = arg.reshape(*arg.shape[:2], -1)

        else:
            raise NotImplementedError

        return arg.transpose((0, 2, 1)).reshape(-1, arg.shape[1])
    return fn

def forced_to_fupc(num_points):
    """
    Converts element to flat unstructured point cloud (fupc): (NxNp, F), 
    ensuring that the length of the first axis NxNp == num_points.
    """
    def fn(arg):
        if arg.ndim == 1:
            return np.ones((num_points, arg.shape[0])) * arg
        
        elif arg.ndim == 2:
            if arg.shape[0] != num_points:
                raise ValueError('Shape mismatch')
            return arg

        elif arg.ndim == 3:
            pass

        elif arg.ndim >= 4:
            arg = arg.reshape(*arg.shape[:2], -1)

        else:
            raise NotImplementedError

        arg = arg.transpose((0, 2, 1)).reshape(-1, arg.shape[1])

        if arg.shape[0] != num_points:
            raise ValueError('Shape mismatch')

        return arg
    return fn
