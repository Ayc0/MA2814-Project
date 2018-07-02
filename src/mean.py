import numpy as np

from settings import stop

def verify_shape(a, b):
    if a.shape != b.shape:
        stop("The two shapes are different: {} {}".format(a.shape, b.shape))

def geometric(a, b):
    verify_shape(a, b)
    c = np.sqrt(np.array(a)*np.array(b))
    return np.nan_to_num(c / np.sum(c))

def arithmetic(a, b):
    verify_shape(a, b)
    return (a + b) / 2