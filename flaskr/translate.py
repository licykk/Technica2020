import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

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
                word = word.lower().strip().translate(str.maketrans('', '', string.punctuation))
                result += legal_dictionary[word][0]
            except:
                result += word
            result += " "
        result += "\n"
    
        
    return result
