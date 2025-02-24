import numpy as np


def values(x):
    if x is not None:
        return x.values


def get(x, arg):
    try:
        return x[arg]
    except:
        if hasattr(x, '__dict__') and arg in x.__dict__:
            return x[arg]
        else:
            return getattr(x, arg, None)

def from_obj(obj, *args, f=lambda x: x):
    return tuple([f(get(obj, arg)) for arg in args])


def nvl(*args):
    for e in args:
        if e is not None:
            return e


def length(x):
    if hasattr(x, '__len__'):
        return len(x)
    else:
        return 1


def array(x, shape=None):
    if isinstance(x, np.ndarray):
        return x
    else:
        return np.full(shape, x) if shape is not None else np.array([x])
