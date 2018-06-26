import os
import sys
import pickle
import shutil

from settings import SPACE
from markov_chain import MarkovChain

source_dir = os.path.join(os.path.dirname(__file__), '../sources')
cache_dir = os.path.join(os.path.dirname(__file__), '../.cache')

def stop(message, error=True):
    if error:
        print('Error:', end=" ")
    print(message)
    sys.exit(1)

# Setup input

override = False

if '--override' in sys.argv or '-o' in sys.argv:
    override = True
    argv = [x for x in sys.argv if x != '-o' and x != '--override']
else:
    argv = sys.argv

if len(argv) < 2:
    stop('Must give a filename')

file = argv[1]
filename = "{}.txt".format(file)

if file == "current":
    stop('"current" isn\'t a valid filename')

available_files = os.listdir(source_dir)

if filename not in available_files:
    stop('{} isn\'t a valid file'.format(file))

source_filename = os.path.join(source_dir, filename)

# Detect whether or not the MC should be computed

# Create cache folder if doesn't exists
cache_folder_exists = os.path.isdir(cache_dir)
if not(cache_folder_exists):
    print("Create cache folder")
    os.makedirs(cache_dir)

cache_filename = os.path.join(cache_dir, "{}.pkl".format(file))
cache_current = os.path.join(cache_dir, "current.pkl")
cache_file_exists = os.path.exists(cache_filename)

if not(override) and cache_file_exists:
    shutil.copy(cache_filename, cache_current)
    stop('Swap current markov chain to "{}"'.format(file), error=False)

# Compute MC

markov_chain = MarkovChain()

print('Parsing file "{}"...'.format(file))

with open(source_filename, 'r') as f:
    word = f.readline()
    while word:
        previous_char = SPACE
        for char in word.rstrip():
            markov_chain.add(previous_char, char)
            previous_char = char
        markov_chain.add(previous_char, SPACE)
        word = f.readline()

# markov_chain.build()

# Store MC
pickle.dump([markov_chain.letters, markov_chain.letters_table], open(cache_filename, 'wb'))

shutil.copy(cache_filename, cache_current)

print("Parsing done.")
print('Set "{}" as current markov chain'.format(file))
