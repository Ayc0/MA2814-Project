import os
import pickle

from markov_chain import MarkovChain

cache_dir = os.path.join(os.path.dirname(__file__), '../.cache')
cache_filename = os.path.join(cache_dir, "current.pkl")

def load():
    [nb_char, letters, letters_table] = pickle.load(open(cache_filename, 'rb'))
    markov_chain = MarkovChain(nb_char, letters, letters_table)
    markov_chain.build()
    return markov_chain

if __name__ == "__main__":
    # execute only if run as a script
    markov_chain = load()
    print(markov_chain.letters)
    print(markov_chain.letters_table)
    print(markov_chain.transition_array)
    print(markov_chain.transition_matrix)

