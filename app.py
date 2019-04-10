import os
import random
from flask import Flask, session, redirect, url_for, request, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
#app.config['SESSION_TYPE'] = 'filesystem'

winning_words = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
max_tries = 5

@app.route('/')
def index():
    return redirect(url_for('username'))

@app.route('/username')
def username():
    if 'username' in request.args:
        username = request.args['username']
        session['username'] = username
        return redirect(url_for('hangman'))
    return render_template('username.html')


@app.route('/hangman')
def hangman():
    if 'winning_word' not in session:
        session['winning_word'] = random.choice(winning_words)
    if 'guesses' not in session:
        session['guesses'] = []
    guesses = session['guesses']
    if 'guess' in request.args:
        guess = request.args['guess']
        if guess not in guesses:
            guesses.append(guess)

    display_word = ''
    for letter in session['winning_word']:
        if letter in guesses:
            display_word += letter
        else:
            display_word += '_'
        display_word += ' '
    session['guesses'] = guesses
    try_number = len(guesses)
    if try_number == max_tries:
        return redirect(url_for('lose'), display_word=display_word)
    return render_template('hangman.html',
            display_word=display_word,
            try_number=try_number)

@app.route('/lose')
def lose():
    session.pop(session['session_key'])
    render_template('lose.html')

@app.route('/win')
def win():
    try:
        username = session['username']
    except KeyError:
        redirect(url_for('lose'), display_word='Nice Try')
    if username in backend['high_scores']:
        num_guesses = len(session['guesses'])
        is_high_score = session['high_scores'][username] < num_guesses
        render_template('win.html',
                try_number=session['try_number'], high_score=True)

if __name__ == '__main__':
    app.run()
