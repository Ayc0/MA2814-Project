import numpy as np
from random import random

from settings import SPACE

def set_to_list(s):
    array = [x for x in s]
    array.sort()
    return array


class MarkovChain:
    def __init__(self, letters={ SPACE }, letters_table=dict(), transition_array=None, transition_matrix=None):
        self.letters = letters
        self.letters_table = letters_table
        self.transition_array = transition_array
        self.transition_matrix = transition_matrix

    def add(self, prev, new):
        self.letters.add(prev)
        self.letters.add(new)
        if ((prev, new) in self.letters_table):
            self.letters_table[(prev, new)] += 1
        else:
            self.letters_table[(prev, new)] = 1
    
    def get(self, prev, new):
        if self.letters_table.get((prev, new)) is not None:
            return self.letters_table[(prev, new)]
        return 0
    
    @property
    def letters_list(self):
        return set_to_list(self.letters)
    
    @property
    def letters_array(self):
        return np.array(self.letters_list)
    
    def sanitize(self, letters):
        return set(letters) & self.letters

    def rowOfLetters(self, letters):
        letters = list(self.sanitize(letters))
        array = np.zeros(self.letters_array.shape)
        for letter in letters:
            array += self.letters_array == letter
        return array / len(letters)

    def nextProba(self, rowOfLetters, order=1):
        return rowOfLetters * (self.transition_matrix ** order)

    def nextLetter(self, letter):
        rowOfLetters = self.rowOfLetters(letter)
        rowOfLetters = self.nextProba(rowOfLetters)
        rand = random()
        cumulative_sum = 0
        for (index, letter) in enumerate(self.letters_list):
            cumulative_sum += rowOfLetters[0, index]
            if cumulative_sum > rand:
                return letter

    def build(self):
        letters_list = self.letters_list
        table = []
        for letterA in letters_list:
            row = []
            for letterB in letters_list:
                row.append(self.get(letterA, letterB))
            table.append(row)
        self.transition_array = np.array(table)
        transition_array = self.transition_array / self.transition_array.sum(axis=1)[:,None]
        self.transition_matrix = np.matrix(transition_array)


