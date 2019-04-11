# 3DHUBS Hangman

This is a hangman game. The user will be prompted to enter a username and given the chance to guess a word--chosen from a predefined list at random--one letter at a time. The user 

## Setup
To start, `clone` the repository, `cd` into it, and (optionally) start up a virtualenv:

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Now install the requirements

`pip install -r requirements.txt`

## Play

To run the game, run the flask app `python app.py` within the virtualenv initialized in the previous section, and open your browser to `localhost:5000`. Enter your desired username, and guess letters or numbers by entering them into the text prompt. You will be allotted 5 incorrect guesses or _lives_. You will be scored according to how many lives you have remaining should you succeed in guessing the word. Your highest score will be recorded.
