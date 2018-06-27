from load import load
from settings import SPACE

mc = load()

word = []

letter = SPACE
for i in range(5000):
    letter = mc.nextLetter(letter)
    if letter != SPACE or mc.nb_char == 1:
        word.append(letter[0])
print(''.join(word))