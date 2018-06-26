from load import load
from settings import SPACE

mc = load()

word = []

letter = SPACE
for i in range(20000):
    letter = mc.nextLetter(letter)
    word.append(letter)
print(''.join(word))