from load import load
from settings import SPACE

mc = load()

word = []

letter = SPACE
for i in range(5000):
    letter = mc.nextLetter(letter)
    if letter != SPACE:
        word.append(letter[0])
print(''.join(word))