import numpy as np

from settings import SPACE

def set_to_list(s):
    array = [x for x in s]
    array.sort()
    return array



class MarkovChain:
    def __init__(self):
        self.markov_chain_dict = dict()
        self.markov_chain_array = None
        self.markov_chain_matrix = None
        self.letters = { SPACE }

    def add(self, prev, new):
        self.letters.add(prev)
        if ((prev, new) in self.markov_chain_dict):
            self.markov_chain_dict[(prev, new)] += 1
        else:
            self.markov_chain_dict[(prev, new)] = 1
    
    def get(self, prev, new):
        if self.markov_chain_dict.get((prev, new)) is not None:
            return self.markov_chain_dict[(prev, new)]
        return 0
    
    @property
    def letters_list(self):
        return set_to_list(self.letters)

    def build_array(self):
        letters_list = self.letters_list
        table = []
        for letterA in letters_list:
            row = []
            for letterB in letters_list:
                row.append(self.get(letterA, letterB))
            table.append(row)
        self.markov_chain_array = np.array(table)


