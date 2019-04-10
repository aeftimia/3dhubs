import os
import flask
import random

from base64 import b64encode
from flask import Flask, session, redirect, url_for, request, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
#app.config['SESSION_TYPE'] = 'filesystem'

winning_words = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
num_lives = 5

@app.route('/')
def index():
    if app.config['SECRET_KEY'] not in session:
        session[app.config['SECRET_KEY']] = {'high_scores': {}}

    if request.cookies.get('session_key'):
        session_key = request.cookies.get('session_key')
    else:
        session_key = b64encode(os.urandom(24)).decode('utf-8')

    session[session_key] = {}
    resp = flask.make_response(redirect(url_for('username')))
    resp.set_cookie('session_key', session_key)
    return resp

@app.route('/username')
def username():
    session_key = request.cookies.get('session_key')
    if not session_key in session:
        return redirect(url_for('index'))

    if 'username' in request.args:
        d = session[session_key]
        d['username'] = request.args['username']
        session[session_key] = d
        resp = redirect(url_for('hangman'))
        resp.set_cookie('session_key', session_key)
        return resp
    return render_template('username.html')

@app.route('/hangman')
def hangman():
    session_key = request.cookies.get('session_key')
    if not session_key in session:
        return redirect(url_for('index'))

    if 'winning_word' not in session[session_key]:
        d = session[session_key]
        d['winning_word'] = random.choice(winning_words)
        session[session_key] = d
    if 'guesses' not in session[session_key]:
        d = session[session_key]
        d['guesses'] = []
        session[session_key] = d
    guesses = session[session_key]['guesses']
    if 'guess' in request.args:
        guess = request.args['guess']
        if guess not in guesses:
            guesses.append(guess)
    d = session[session_key]
    d['guesses'] = guesses
    session[session_key] = d

    display_word = ''
    winning_word = session[session_key]['winning_word']
    for letter in winning_word:
        if letter in guesses:
            display_word += letter
        else:
            display_word += '_'
        display_word += ' '

    winning_letters = frozenset([letter for letter in winning_word])
    guessed_set = frozenset(guesses)
    num_lives_left = num_lives - len(guessed_set - winning_letters)
    session[session_key]['num_lives_left'] = num_lives_left
    if num_lives_left == 0:
        return redirect(url_for('lose'))
    if len(winning_letters - guessed_set) == 0:
        return redirect(url_for('win'))
    return render_template('hangman.html',
            display_word=display_word,
            num_lives_left=num_lives_left)

@app.route('/lose')
def lose():
    session_key = request.cookies.get('session_key')
    if not session_key in session:
        return redirect(url_for('index'))
    session.pop(session_key)
    return render_template('lose.html')

@app.route('/win')
def win():
    session_key = request.cookies.get('session_key')
    if not session_key in session:
        return redirect(url_for('index'))
    username = session[session_key]['username']
    num_lives_left = session[session_key]['num_lives_left']
    high_scores = session[app.config['SECRET_KEY']]['high_scores']
    if username in high_scores:
        is_high_score = high_scores[username] < num_lives_left
        if is_high_score:
            high_scores[username] = num_lives_left
    else:
        is_high_score = True
        d = session[app.config['SECRET_KEY']]
        d['high_scores'][username] = num_lives_left
        session[app.config['SECRET_KEY']] = d
    session.pop(session_key)
    return render_template('win.html',
            num_lives_left=num_lives_left,
            high_score=is_high_score)

if __name__ == '__main__':
    app.run()
