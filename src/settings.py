import sys
import numpy as np

SPACE = ' '

def stop(message, error=True):
    if error:
        sys.stderr.write('Error: {} '.format(message))
        sys.exit(1)
    print(message)
    sys.exit(0)

def formatRow(array):
    return np.array(array).reshape(array.size)