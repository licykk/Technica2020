import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
import requests


bp = Blueprint('translate', __name__, url_prefix='/translate')

# @bp.route('/')
# def options():
#     return render_template('translate/translate.html')


@bp.route('/translate', methods=('GET', 'POST'))
def translate():
    if g.user is None:
            return redirect(url_for('auth.login'))
    if request.method == 'POST':
        title = request.form['legalese-title']
        data = request.form['legalese']
        error = None
        result = translate_legalese(data)
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO documents (title, body, author_id)'
                    ' VALUES (?, ?, ?)',
                    (title, result, g.user['id'])
                )
            db.commit()
            return render_template('translate/result.html', result=result, title=title)

    return render_template('translate/translate.html')

# @bp.route('/upload', methods=('GET', 'POST'))
# def upload():
#     if request.method == 'POST':
#         data = request.form['legalese']

#     return render_template('translate/result.html', result=result)

@bp.route('/picupload', methods=('GET', 'POST'))
def picupload():
    if request.method == 'POST':
        data = request.form['legalese']
    
    result = translate_legalese(data)

    return render_template('translate/result.html', result=result)

# function that does the hardcore work
# data is input text
# find and replace
import csv
import string

#get data from csv TrainingData.csv
legal_dictionary = {}
with open('TrainingData.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        legal_dictionary[row[0]] = row[1:]

def translate_legalese(data):
    result = ""
    for line in data.split("\n"):
        for word in line.split(" "):
            try:
                new_word = word.lower().strip().translate(str.maketrans('', '', string.punctuation))
                result += legal_dictionary[new_word][0]
            except:
                result += word
            result += " "
        result += "\n"
    
        
    return result



# grammar checker
def auto_correct_text(text):
    r = requests.post("https://grammarbot.p.rapidapi.com/check",
        data = {'text': text, 'language': 'en-US'},
        headers={
        'x-rapidapi-host': "grammarbot.p.rapidapi.com",
        'x-rapidapi-key': config.grammar_api,
        'content-type': "application/x-www-form-urlencoded"
    })
    j = r.json()
    new_text = ''
    cursor = 0
    print(j)
    for match in j["matches"]:
        offset = match["offset"]
        length = match["length"]
        if cursor > offset:
            continue
        # build new_text from cursor to current offset
        new_text += text[cursor:offset]
        # next add first replacement
        repls = match["replacements"]
        if repls and len(repls) > 0:
            new_text += repls[0]["value"]
        # update cursor
        cursor = offset + length
    
    # if cursor < text length, then add remaining text to new_text
    if cursor < len(text):
        new_text += text[cursor:]
 
    return new_text