import matplotlib
matplotlib.use('Agg')

import os

import matplotlib.pyplot as plt
import numpy as np

from load import load

images_dir = os.path.join(os.path.dirname(__file__), '../docs/images')

if __name__ == "__main__":
    # execute only if run as a script
    markov_chain = load()

    filename = '{}.png'.format(markov_chain.name)
    filepath = os.path.join(images_dir, filename)

    matrix = np.nan_to_num(markov_chain.transition_matrix / np.amax(markov_chain.transition_matrix, axis=1))
    plt.imshow(matrix, cmap="viridis")

    # Display letters in ticks
    plt.xticks(np.arange(len(markov_chain.letters_list)), markov_chain.letters_list)
    plt.yticks(np.arange(len(markov_chain.letters_list)), markov_chain.letters_list)
    
    # Set x tick to top
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

    plt.savefig(filepath)
    print('"{}" has been added in "/docs/images/"'.format(filename))
