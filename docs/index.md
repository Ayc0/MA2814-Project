---
title: Random word generator
tagline: Markov chain based word generator
permalink: /
---

{% include images.md %}

## How to determine the signature markov chain of a language

### Initializing

The first approach was to create a markov chain that represents the chances to pass from one possible character to another.

To do this, we initially download a text file, we format it in lowercase, remove every punctuation, every numbers, etc. (all those files are in `/sources/`) (to remove every punctuation, etc. we wrote a JavaScript script `/format.js` that uses the package [sluggr](https://www.npmjs.com/package/sluggr)).

Then we parse this text file and we count which character follows which character in a `MarkovChain` class. At the end of the parsing, the computed pseudo markov chain has a label, a set of characters included in it and the map of followers.

As the parsing can take some time, we don't want to recompute it each time we run the script so we store the results in a `/.cache/` folder.

In addition to the label, the set of characters and the map, running the `build()` method of a markov chain returns its transition matrix (and the map represented with `numpy.array` object). Those two variables are only computed after the build phase because once they're done, you cannot easily add a new character in the markov chain.

### Input file

One question we faced was: which file should we use to train our model? As we couldn't find an answer without running any test, we tried our algorithm on two different files: `"words.txt"` and `"Notre_Dame_de_Paris_full.txt"` (renamed afterwards `"fr_full.txt"`). `"words.txt"` is the list of almost every words in french, and `"Notre_Dame_de_Paris.txt"` is the full text of [Notre-Dame de Paris](https://fr.wikisource.org/wiki/Notre-Dame_de_Paris).

In order to have a visual representation of what we were doing, we wrote a function that uses `matplotlib` to display the transition matrix of markov chains (with the colormap mode).

The graphic represents the probability for any possible character (on the left) to be followed by any other character (on the bottom). To make the graphic clearer, each row was scaled up to have the highest probability equal to one (simple multiplication on the entire row).

The last column is frequency of letters (the highest frequency is also set to 1).

| ![Notre-Dame de Paris][fr_full] | ![French words][words] |
| :-----------------------------: | :--------------------: |
|       Notre-Dame de Paris       |      French words      |

We chose to use `"Notre_Dame_de_Paris_full.txt"` instead of `"words.txt"` because it is a real use of the french language and is more realistic that the other one (even if it doesn't match the [theoretical frequency](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia_en_fran%C3%A7ais)).

And if we had an even larger sample, we would have a better markov chain.

Those graphs are the signature of a language: the markov_chain and the frequency of letters.

## Determine the language of a given text

| ![Notre-Dame de Paris][fr_full] | ![Notre-Dame de Paris english][en] | ![Un capriccio del dottor Ox][it_full] |
| :-----------------------------: | :--------------------------------: | :------------------------------------: |
|       Notre-Dame de Paris       |   Notre-Dame de Paris in english   |       Un capriccio del dottor Ox       |

The same method as previously have been applied on two other texts: [the english translation of Notre-Dame de Paris](https://en.wikisource.org/wiki/The_Hunchback_of_Notre_Dame) and [Un capriccio del dottor Ox](https://it.wikisource.org/wiki/Un_capriccio_del_dottor_Ox). And we've also taken a paragraph written in one of those three languages and computed it's markov chain:

| ![Guadeloupe][guadeloupe] |
| :-----------------------: |
|     Unknown language      |

One way to determine the original language is to give a score to each language and then select the language with the lowest score.

<!-- prettier-ignore-start -->
In order to compute this score, we use this formula: $\dfrac{\sum_i\sum_j norm(| U_{ij} - L_{k,ij} |)}{n^2}$ (with $L_k$ the k-language (fr/it/en/etc.) and $U$ the unknown paragraph and $n$ the size of the matrix).
<!-- prettier-ignore-end -->

The score is divided by `n²` to make it independent of the size of the matrix so we can compare with the same score function every transition matrices.

The `norm` function should be best determined in order to have the best results.

### Determination of the norm

We chose a norm with the shape: $x \rightarrow x^y, y > 0$. If `y = 1`, every differences in coefficients are as meaningful as any others. If `y > 1`, the differences will be flatten, specially around 0. On the opposite, if `y < 1`, there will be exacerbated.

As it is pretty common to have a few errors, as long as they're not too big, it's acceptable (having 0.6 instead of 0.5 is okay). But we want to prevent huge gaps (we don't want a 0.9 instead of a 0.2).

In order to have the right norm function, we have to determine this limit.

### Cutoff limit

First, with $norm = x \rightarrow x^y, y > 0$, the "cutoff" value is when the function starts to raise pretty quickly, which is when the value of its derivative is 1.

$ norm(x) = x^y \Rightarrow norm'(x) = y . x^{y-1} $

$ norm'(x) = 1 \Leftrightarrow x = \sqrt[y-1]{\dfrac{1}{y}} $

With geogebra, we plot the function $y \rightarrow \sqrt[y-1]{\dfrac{1}{y}}$ and we looked at its intersections with the function $x = k$, for various values of k (interesting cutoff values).

This is what we got:

| x    | y    |
| ---- | ---- |
| 0.33 | 0.81 |
| 0.4  | 1.19 |
| 0.5  | 2    |
| 0.6  | 3.39 |
| 0.66 | 4.94 |
| 0.75 | 8.4  |

Then we compared those cutoff values with the data we had to see which one is the best:

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

`(n, x) := (4.94, 0.666)` is chosen because it maximizes at the same time the percentage of differences with en and it.

Having a rather large cutoff value can be explained because we are only interested in the location of the biggest percentages in the markov chains: knowing that the sequence "xw" is rare in a language and that it is also rare in another language has less value than it is rare in one but important in another one.

## How to generate words

### First algorithm

We initially did a naive algorithm: you start with the whitespace, then you take the row associated to this character in the transition matrix and you have discrete distribution of followers, and you take one random letter according to this distribution. And you start again from this letter. An example of a text generated by this algorithm can be find [here]({{base_url}}results.html#chunks-of-1-letter).

But this method has a strong limitation: there is no memory of past letters. For instance, in french you often have two "m"s in a row but **never** three "m"s. But if you apply this algorithm there is a high probability when you reach a "m" to continue on another "m" and so on (in the example, you can find a similar issue with the letter "l").

### Bigger chunks

One way have some kind of memory **and** still have a word generator using markov chain is to create a map of chunks (go from "ag" to "gl")instead of creating a map of letters (go from letter "a" to letter "b"). The only condition is that every chunks should form a sort of chain: the chunk "xy" can only be followed "yz" (or "wxy" by "xyz", etc.). But this has a huge drawback: the size of the transition matrix. For a transition matrix of 3 letters chunks, the matrix has a size of (3581x3581). And the more letters you have in a chunk, the bigger the matrix is.

But the improvement is noticeable: for the [2 letters chunks]({{base_url}}results.html#chunks-of-2-letters) and for the [3 letters chunks]({{base_url}}results.html#chunks-of-3-letters), the more letters you have in a chunk, the "frenchier" the words are.

And the following table represents the score of each languages according to the previous method of computing scores.

| lang | 1 letter | 2 letters | 3 letters |
| :--- | :------: | :-------: | :-------: |
| fr   | 1.471e-6 | 3.483e-6  | 1.809e-6  |
| en   | 8.414e-4 | 8.793e-4  | 7.766e-4  |
| it   | 6.572e-4 | 9.002e-4  | 8.490e-4  |

According to the scores, the way the word generator works still produces "french" texts even with chunks of 2-3 letters.

(We're using the same model for the training and for the validation).

As the chunks of 2 letters produces a fairly good generator and as it's less greedy in term of matrix sizes, we're going to use this type of generator afterwards and we generated a [french text but with accents]({base_url}}results.html#french-real-text-with-accents) (é, à, etc.), an [italian text with accents]({{base_url}}results.html#italian-with-accents) and an [english text]({{base_url}}results.html#english-real-text).

## How to generate words with specific length

WIP

## Conclusion

What we succeeded to do:

- A way to parse text and generate a signature,
- A way to compare signatures to determine the language of a text,
- A way to generate texts using this signature.

What we can improve:

- Bigger input sample,
- Train model and verify it on 2 different data sets,
- Verify scores on multiple texts of various lengths,
- Find a better way to create a score (the 1-letter chunk produces the same score as 3-letters chunk even if the 3-letters chunks' generated text feels much more french)
