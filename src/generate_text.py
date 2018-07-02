import sys

from load import load
from settings import SPACE

def generate(length):
    mc = load()
    word = []
    letter = SPACE
    for i in range(length):
        letter = mc.nextLetter(letter)
        if letter != SPACE or mc.nb_char == 1:
            word.append(letter[0])
    return ''.join(word)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        stop('Must give a length')
    length = int(sys.argv[1])
    print(generate(length))
    