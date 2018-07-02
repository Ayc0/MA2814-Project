import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from load import load
from settings import SPACE, formatRow
import mean

mc = load()
mc_pure = mc.copy(pure=True)

mu_0 = mc.rowOfLetters(SPACE)
indexOfSpace = mc.letters_list.index(SPACE)

mu_1 = np.delete(formatRow(mu_0 * mc.transition_matrix), indexOfSpace)
mu_n = np.delete(formatRow(mu_0 * mc.transition_matrix.I), indexOfSpace)
print(mu_n)
print(mu_n * mc_pure.transition_matrix)


M = mc_pure.transition_matrix
Ms = [np.matrix(np.eye(len(mc.letters) - 1)), M]
def powM(i):
    global Ms
    n = len(Ms)
    if i < n:
        return Ms[i]
    while i >= n:
        Ms.append(Ms[-1] * M)
        n += 1
    return Ms[i]

I = mc_pure.transition_matrix.I
Is = [np.matrix(np.eye(len(mc.letters) - 1)), I]
def powI(i):
    global Is
    n = len(Is)
    if i < n:
        return Is[i]
    while i >= n:
        # Is.append(powM(n).I)
        Is.append(Is[-1] * I)
        n += 1
    return Is[i]



length = 8
letters = []
for i in range(length):
    distrib = mean.geometric(mu_1 * powM(i), mu_n * powI(length - 1 - i))
    letters.append(formatRow(distrib))



