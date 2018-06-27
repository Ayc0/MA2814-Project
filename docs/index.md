---
title: Random word generator
tagline: Markov chain based word generator
---

## How to determine the signature markov chain of a language

### Initializing

The first approach was to create a markov chain that represents the chance to pass from one possible character to another one.

To do this, we initially download a text file, then we format it in lowercase, remove every punctuation, every numbers, etc. (all those files are in `/sources/`) (to remove every punctuation, etc. we wrote a JavaScript script `/format.js` that uses the package [sluggr](https://www.npmjs.com/package/sluggr)).

Then we parse this text file and we count in a `MarkovChain` class which character follows which other character. At the end of the parsing, this pseudo markov chain has a label, the set of characters included in it and this map of followers.

As the parsing can take some time, we don't want to recompute it each time we run a script. And so we store them in a `.cache` folder.

In addition to the label, the set of characters and the map, if we run the `build` method of a markov chain, we can have its transition matrix (and the map represented with `numpy.array` object). Those two variables are only computed after the build phase because once they're done, you cannot easily add a new character in the markov chain.

## Score power

$ f(x) = x^n \Rightarrow f'(x) = n . x^{n-1} $

$ f'(x) = 1 \Leftrightarrow x = \sqrt[n-1]{\dfrac{1}{n}} $

| n    | x    |
| ---- | ---- |
| 0.81 | 0.33 |
| 1.19 | 0.4  |
| 2    | 0.5  |
| 3.39 | 0.6  |
| 4.94 | 0.66 |
| 8.4  | 0.75 |

### n = 0.81, x = 0.33

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 4.651e-2 |         0% |
| en   | 5.888e-2 |        26% |
| it   | 5.491e-2 |        18% |

### n = 1.19, x = 0.4

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 2.022e-2 |         0% |
| en   | 2.714e-2 |        34% |
| it   | 2.686e-2 |        32% |

### n = 2, x = 0.5

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 5.361e-3 |         0% |
| en   | 7.987e-3 |        48% |
| it   | 8.563e-3 |        59% |

### n = 4.94, x = 0.666

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 3.166e-4 |         0% |
| en   | 5.390e-4 |        70% |
| it   | 8.479e-4 |       167% |

### n = 8.4, x = 75

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 3.237e-5 |         0% |
| en   | 4.763e-5 |        47% |
| it   | 14.94e-5 |       361% |

### Conclusion

`n=4.94` is chosen because gap of `66%`
