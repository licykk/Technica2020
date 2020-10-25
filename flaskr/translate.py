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

import nltk
import sys
def translate_legalese(data):
	result = data
	data = data.lower().strip().translate(str.maketrans('', '', string.punctuation))
	for phrase in legal_dictionary:
		if data.find(phrase) > -1:
			print(phrase, legal_dictionary[phrase][0])
			result = result.replace(phrase, legal_dictionary[phrase][0])


	# for line in data.split("\n"):
	# 	for word in line.split(" "):
	# 		try:
	# 			new_word = word.lower().strip().translate(str.maketrans('', '', string.punctuation))
	# 			result += legal_dictionary[new_word][0]
	# 			#print(legal_dictionary[new_word][0], file=sys.stdout)
	# 		except:
	# 			result += word
	# 		result += " "
	# 	for sentence in line.split(". "):
	# 		print(sentence, file=sys.stdout)
	# 		word_tokens = nltk.word_tokenize(sentence)
	# 		word_tags = nltk.pos_tag(word_tokens)
	# 		fragment_chunks = nltk.chunk.ne_chunk(word_tags)
	# 		for chunk_word in fragment_chunks:
	# 			# if the chunk is a tree type
	# 			if(type(chunk_word) == nltk.tree.Tree):
	# 				# get node label)
	# 				chunk_word_label = chunk_word.label()
	# 				print(chunk_word_label, file=sys.stdout)
	# 				# if the word is labeled person OR if the word before it was
	# 				#if(chunk_word_label == 'PERSON'):
	# 	result += "\n"
	
		
	return result

# def check_grammar():
#     url = "https://jspell-checker.p.rapidapi.com/check"

#     payload = "{t"language": "enUS",t"fieldvalues": "thiss is intresting",t"config": {tt"forceUpperCase": false,tt"ignoreIrregularCaps": false,tt"ignoreFirstCaps": true,tt"ignoreNumbers": true,tt"ignoreUpper": false,tt"ignoreDouble": false,tt"ignoreWordsWithNumbers": truet}}"
#     headers = {
#         'x-rapidapi-host': "jspell-checker.p.rapidapi.com",
#         'x-rapidapi-key': "291656ee30msh18e8c9fae5f9512p192f82jsn5f47800ab86e",
#         'content-type': "application/json",
#         'accept': "application/json"
#         }
#     response = requests.request("POST", url, data=payload, headers=headers)

#     print(response.text)

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