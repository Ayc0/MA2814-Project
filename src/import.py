import os
import sys

from settings import SPACE
from markov_chain import MarkovChain

source_dir = os.path.join(os.path.dirname(__file__), 'sources')

if len(sys.argv) < 2:
    raise Exception('Must give a filename')

filename = "{}.txt".format(sys.argv[1])

available_files = os.listdir(source_dir)

if filename not in available_files:
    raise Exception('{} isn\'t a valid file'.format(sys.argv[1]))

source_filename = os.path.join(source_dir, filename)

markov_chain = MarkovChain()

with open(source_filename, 'r') as f:
    word = f.readline()
    while word:
        previous_char = SPACE
        for char in word.rstrip():
            markov_chain.add(previous_char, char)
            previous_char = char
        markov_chain.add(previous_char, SPACE)
        word = f.readline()

markov_chain.build_array()
