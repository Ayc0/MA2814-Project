# TL;DR

Project for MA2814 - Introduction to Random Modeling

# Requirements

- `pipenv`
- `pyenv`

# Install

- `pipenv install`

# Commands

- `pipenv run import <filename> [-o, --override]` <br>
  Parse `sources/<filename>.txt` and compute its related markov chain, then stores it in `.cache` folder.<br><br>
  if `<filename>` is already cached, and `override` isn't specified, it just sets this markov chain as the current one

- `pipenv run display` <br>
  Create transition matrix image in /docs/images

# Bibliography

[Notre-Dame de Paris](https://fr.wikisource.org/wiki/Notre-Dame_de_Paris)
