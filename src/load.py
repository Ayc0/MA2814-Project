import os
import pickle

from markov_chain import MarkovChain
from settings import stop

cache_dir = os.path.join(os.path.dirname(__file__), '../.cache')
cache_filename = os.path.join(cache_dir, "current.pkl")

def filename(file):
    cache_filename = os.path.join(cache_dir, "{}.pkl".format(file))
    if not(os.path.exists(cache_filename)):
        stop('Cached "{}" doesn\'t exists, you should import it before')
    return cache_filename

def load(file="current", build=True):
    [file, nb_char, letters, letters_table] = pickle.load(open(filename(file), 'rb'))
    markov_chain = MarkovChain(file, nb_char, letters, letters_table)
    if build:
        markov_chain.build()
    return markov_chain

if __name__ == "__main__":
    # execute only if run as a script
    markov_chain = load()
    print(markov_chain.letters)
    print(markov_chain.letters_table)
    print(markov_chain.transition_array)
    print(markov_chain.transition_matrix)

