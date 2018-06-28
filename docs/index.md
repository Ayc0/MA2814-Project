---
title: Random word generator
tagline: Markov chain based word generator
permalink: /
---

{% include images.md %}

## How to determine the signature markov chain of a language

### Initializing

The first approach was to create a markov chain that represents the chance to pass from one possible character to another one.

To do this, we initially download a text file, then we format it in lowercase, remove every punctuation, every numbers, etc. (all those files are in `/sources/`) (to remove every punctuation, etc. we wrote a JavaScript script `/format.js` that uses the package [sluggr](https://www.npmjs.com/package/sluggr)).

Then we parse this text file and we count in a `MarkovChain` class which character follows which other character. At the end of the parsing, this pseudo markov chain has a label, the set of characters included in it and this map of followers.

As the parsing can take some time, we don't want to recompute it each time we run a script. And so we store them in a `/.cache/` folder.

In addition to the label, the set of characters and the map, if we run the `build()` method of a markov chain, we can have its transition matrix (and the map represented with `numpy.array` object). Those two variables are only computed after the build phase because once they're done, you cannot easily add a new character in the markov chain.

### Input file

One question we faced was: which file should we use to train our model? As we couldn't find a right response without any tests, we tried our algorithm on two different files: `"words.txt"` and `"Notre_Dame_de_Paris_full.txt"` (renamed afterwards `"fr_full.txt"`). `"words.txt"` is the list of almost every words in french, and `"Notre_Dame_de_Paris.txt"` is the full text of [Notre-Dame de Paris](https://fr.wikisource.org/wiki/Notre-Dame_de_Paris).

In order to have a visual representation of what we were doing, we wrote a function that uses `matplotlib` to display the transition matrix of markov chains (with the colormap mode).

The graphic represents the probability for any possible character (on the left) to reach any other character (on the bottom). To make the graphic clearer, every row were scaled up to have the highest probability equal to one (simple multiplication on the entire row).

The last column is frequency of letters (the highest frequency is also set to 1).

| ![Notre-Dame de Paris][fr_full] | ![French words][words] |
| :-----------------------------: | :--------------------: |
|       Notre-Dame de Paris       |      French words      |

We chose to use `"Notre_Dame_de_Paris_full.txt"` instead of `"words.txt"` because it is a real use of the french language and is more realistic that the other one (even if it doesn't match the [theoretical frequency](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia_en_fran%C3%A7ais)).

And if we had a even larger sample, we'll have a better markov chain.

Those graphs are the signature of a language: the markov_chain and the frequency of letters.

## Determine the language of a given text

| ![Notre-Dame de Paris][fr_full] | ![Notre-Dame de Paris english][en] | ![Un capriccio del dottor Ox][it_full] |
| :-----------------------------: | :--------------------------------: | :------------------------------------: |
|       Notre-Dame de Paris       |   Notre-Dame de Paris in english   |       Un capriccio del dottor Ox       |

The same method as previously was done on two other texts: [the english translation of Notre-Dame de Paris](https://en.wikisource.org/wiki/The_Hunchback_of_Notre_Dame) and [Un capriccio del dottor Ox](https://it.wikisource.org/wiki/Un_capriccio_del_dottor_Ox). And we've also took a paragraph written in one of those three languages and computed it's markov chain:

| ![Guadeloupe][guadeloupe] |
| :-----------------------: |
|     Unknown language      |

One way to determine the original language is to attribute a score to each language and to select the language with the lowest score.

<!-- prettier-ignore-start -->
In order to compute this score, we use this formula: $\dfrac{\sum_i\sum_j norm(| U_{ij} - L_{k,ij} |)}{n^2}$ (with $L_k$ the k-language (fr/it/en/etc.) and $U$ the unknown paragraph and $n$ the size of the matrix).
<!-- prettier-ignore-end -->

The score is divided by `n²` to make it independent to the size of the matrix and if there're more letters, the score won't be affected and so we can compare (with the same score function) every transition matrix.

The `norm` function should be best determined in order to have the best results.

### Determination of the norm

We chose a norm with the shape: $x \rightarrow x^y, y > 0$. If `y = 1`, every differences in coefficient are as meaningful as any others. If `y > 1`, the differences will be flatten, specially around 0. On the opposite, if `y < 1`, there will be exacerbated.

As it is pretty common to have a few errors, as long as they're under a certain limit, it's acceptable (having 0.6 instead of 0.5 is okay). But we want to prevent huge gaps (we don't want a 0.9 instead of a 0.2).

In order to have the right norm function, we have to determine this limit.

### Cutoff limit

First, with $norm = x \rightarrow x^y, y > 0$, the "cutoff" value is when the function starts to raise pretty quickly, which is when the value of its derivative is 1.

$ norm(x) = x^y \Rightarrow norm'(x) = y . x^{y-1} $

$ norm'(x) = 1 \Leftrightarrow x = \sqrt[y-1]{\dfrac{1}{y}} $

With geogebra, we plot the function $y \rightarrow \sqrt[y-1]{\dfrac{1}{y}}$ and we looked at its intersections with the function $x = k$, for various value of k (interesting cutoff values).

This is what we got:

| x    | y    |
| ---- | ---- |
| 0.33 | 0.81 |
| 0.4  | 1.19 |
| 0.5  | 2    |
| 0.6  | 3.39 |
| 0.66 | 4.94 |
| 0.75 | 8.4  |

Then we compared those cutoff values with the data we had to see which one was the best:

#### n = 0.81, x = 0.33

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 4.651e-2 |         0% |
| en   | 5.888e-2 |        26% |
| it   | 5.491e-2 |        18% |

#### n = 1.19, x = 0.4

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 2.022e-2 |         0% |
| en   | 2.714e-2 |        34% |
| it   | 2.686e-2 |        32% |

#### n = 2, x = 0.5

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 5.361e-3 |         0% |
| en   | 7.987e-3 |        48% |
| it   | 8.563e-3 |        59% |

#### n = 4.94, x = 0.666

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 3.166e-4 |         0% |
| en   | 5.390e-4 |        70% |
| it   | 8.479e-4 |       167% |

#### n = 8.4, x = 75

| lang |  score   | percentage |
| :--- | :------: | ---------: |
| fr   | 3.237e-5 |         0% |
| en   | 4.763e-5 |        47% |
| it   | 14.94e-5 |       361% |

### Conclusion

`(n, x) := (4.94, 0.666)` is chosen because its maximized at the same time the percentage of differences with en and it.

Having a rather large cutoff value can be explained because we are only interested in the location of the biggest percentages in the markov chains: knowing that the sequence "xw" is rare in a language and that it is also rare in another language has less value than it is rare in one but important in another one. Same thing is "xw" is really common in one language and common in another one.
