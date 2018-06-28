import numpy as np

from load import load
from settings import SPACE
from markov_chain import MarkovChain

languages = ["fr", "en", "it"]
mystery_file = "current"

# Load markov chains without building them
unknown_markov_chain = load(mystery_file, False)
markov_chains = []
for language in languages:
    markov_chain = load(language, False)
    markov_chains.append(markov_chain)


# Guess common letters
letters = unknown_markov_chain.letters
for markov_chain in markov_chains:
    letters &= markov_chain.letters

print(letters)

# Set common letters
unknown_markov_chain.letters = letters
for markov_chain in markov_chains:
    markov_chain.letters = letters

# Build markov chains
unknown_markov_chain.build()
for markov_chain in markov_chains:
    markov_chain.build()

nb_cells = unknown_markov_chain.transition_matrix.size

# Determine closest matrix
norm = lambda matrix: np.power(np.abs(matrix), 4.94)
scores = [np.sum(norm(markov_chain.transition_matrix - unknown_markov_chain.transition_matrix)) / nb_cells for markov_chain in markov_chains]
min_score = min(scores)
winner_index = scores.index(min_score)
winner_language = languages[winner_index]

for (index, score) in enumerate(scores):
    print("{}: {} ({}%)".format(languages[index], score, int((score - min_score)/min_score * 100)))
