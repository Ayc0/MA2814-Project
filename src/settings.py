import sys
import numpy as np
from random import random

SPACE = ' '

def stop(message, error=True):
    if error:
        sys.stderr.write('Error: {} '.format(message))
        sys.exit(1)
    print(message)
    sys.exit(0)

def formatRow(array):
    return np.array(array).reshape(array.size)

def randomDistrib(array):
    array = formatRow(array)
    rand = random()
    cumulative_sum = 0
    for (index, percent) in enumerate(array):
        cumulative_sum += percent
        if cumulative_sum > rand:
            return index
    return -1