import numpy as np

from settings import SPACE, randomDistrib

def set_to_list(s):
    array = [x for x in s]
    array.sort()
    return array

def copyNotNone(value):
    if value is None:
        return None
    return value.copy()

class MarkovChain:
    def __init__(self, name, nb_char=1, letters={ SPACE }, letters_table=dict(), transition_array=None, transition_matrix=None, reversion_array=None):
        self.name = name
        self.nb_char = nb_char
        self.letters = letters.copy()
        self.letters_table = letters_table.copy()
        self.transition_array = copyNotNone(transition_array)
        self.transition_matrix = copyNotNone(transition_matrix)
        self.reversion_array = copyNotNone(reversion_array)

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
        if len(letters):
            return array / len(letters)
        return array

    def nextProba(self, rowOfLetters, order=1):
        return rowOfLetters * (self.transition_matrix ** order)

    def nextLetter(self, letter):
        rowOfLetters = self.rowOfLetters([letter])
        rowOfLetters = self.nextProba(rowOfLetters)
        index = randomDistrib(rowOfLetters)
        if index == -1:
            message = '"{}" don\'t have any followers'.format(letter)
            raise ValueError(message)
        return self.letters_list[index]

    def build(self, pure=False):
        is_space_in_letters = SPACE in self.letters
        if pure:
            self.letters = self.letters - set(SPACE)
        letters_list = self.letters_list
        table = []
        for letterA in letters_list:
            row = []
            for letterB in letters_list:
                row.append(self.get(letterA, letterB))
            table.append(row)
        self.transition_array = np.array(table)
        transition_array = np.nan_to_num(self.transition_array / self.transition_array.sum(axis=1)[:,None])
        self.transition_matrix = np.matrix(transition_array)
        reversion_array = np.transpose(self.transition_array)
        reversion_array = np.nan_to_num(reversion_array / reversion_array.sum(axis=1)[:,None])
        self.reversion_matrix = np.matrix(reversion_array)
        # if pure and is_space_in_letters:
            # self.letters = self.letters |  set(SPACE)

    def copy(self, name=None, build=True, pure=False):
        if name is None:
            name = self.name
        if build:
            transition_array = None
            transition_matrix = None
            reversion_array = None
        else:
            transition_array = self.transition_array
            transition_matrix = self.transition_matrix
            reversion_array = self.reversion_array
        copied = MarkovChain(name, self.nb_char, self.letters, self.letters_table, transition_array, transition_matrix, reversion_array)
        if build:
            copied.build(pure)
        return copied



