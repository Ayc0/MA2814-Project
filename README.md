# TL;DR

Project for MA2814 - Introduction to Random Modeling

# Requirements

- `pipenv`
- `pyenv`

# Install

The packages used are numpy and matplotlib and the current python version is the v3.5. If you don't have this version of python, install `pyenv` to install any version of python, and `pipenv` to install every package.

- `pipenv install` <br>
  To install every package with the right version

# Commands

As the project uses pipenv, you should use it to run the files:

- `pipenv run import <filename> [-o, --override]` <br>
  Parse `sources/<filename>.txt` and compute its related markov chain, then stores it in `.cache` folder.<br><br>
  if `<filename>` is already cached, and `override` isn't specified, it just sets this markov chain as the current one

- `pipenv run display` <br>
  Create transition matrix image in /docs/images

- `pipenv run generate [method] -n [number]` <br>
  Generate (depending on the method) a text / words using the current markov chain's transition matrix <br>
  Allowed methods: `text` (for now)<br>

- `pipenv run compare` <br>
  Compare the `current` markov chain with `it`, `fr` and `en` to determine the language of `current`

# Sources

- [Notre-Dame de Paris](https://fr.wikisource.org/wiki/Notre-Dame_de_Paris) (full)
- [The Hunchback of Notre-Dame](https://en.wikisource.org/wiki/The_Hunchback_of_Notre_Dame) (full)
- [Un capriccio del dottor Ox](https://it.wikisource.org/wiki/Un_capriccio_del_dottor_Ox) (only 3 first chapters)
- [https://fr.wikipedia.org/wiki/Guadeloupe](Wikipedia's page on Guadeloupe)
