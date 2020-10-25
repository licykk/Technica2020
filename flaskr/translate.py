import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('translate', __name__, url_prefix='/translate')

@bp.route('/')
def options():
    return render_template('translate/translate.html')

@bp.route('/translate', methods=('GET', 'POST'))
def translate():
    if request.method == 'POST':
        data = request.form['legalese']

        result = translate_legalese(data)

    return render_template('translate/result.html', result=result)

# @bp.route('/upload', methods=('GET', 'POST'))
# def upload():
#     if request.method == 'POST':
#         data = request.form['legalese']

#     return render_template('translate/result.html', result=result)

#@bp.route('/picupload', methods=('GET', 'POST'))
# def picupload():
#     if request.method == 'POST':
#         data = request.form['legalese']
    
#     result = translate_legalese(data)

#     return render_template('translate/result.html', result=result)

# function that does the hardcore work
# data is input text
def translate_legalese(data):
    b = get_db()
    result = "Put result here"

    
    return "hi"

# find and replace
def translate_legalese_planB(data):
    return "hi"
    
