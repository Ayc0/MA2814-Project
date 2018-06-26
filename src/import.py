import os
import sys

from settings import SPACE

source_dir = os.path.join(os.path.dirname(__file__), 'sources')

if len(sys.argv) < 2:
    raise Exception('Must give a filename')

filename = "{}.txt".format(sys.argv[1])

available_files = os.listdir(source_dir)

if filename not in available_files:
    raise Exception('{} isn\'t a valid file'.format(sys.argv[1]))

source_filename = os.path.join(source_dir, filename)

# TODO: remplace print by a valid function
add_letter = print

with open(source_filename, 'r') as f:
    word = f.readline()
    while word:
        previous_char = SPACE
        for char in word.rstrip():
            add_letter(previous_char, char, end="|")
            previous_char = char
        add_letter(previous_char, SPACE)
        word = f.readline()