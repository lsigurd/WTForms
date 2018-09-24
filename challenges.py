#import statements go here 
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"
    
#create class to represent WTForm that inherits flask form

class iTunesForm(FlaskForm):
	artist= StringField('Enter an artist name?', validators=[Required()])
	email = StringField('Enter your email', validators=[Required(), Email()])
	results = StringField('Enter number of results', validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    simpleForm = iTunesForm()
    return render_template('itunes-form.html', form=simpleForm) 

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = iTunesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
    	artist = form.artist.data
    	results = form.results.data
    	params = {}
    	params['term'] = artist
    	params['limit'] = results
    	response = requests.get("https://itunes.apple.com/search?", params = params)
    	response_py = json.loads(response.text)['results']
    flash('All fields are required!')
    return render_template('itunes-results.html', result_html = response_py) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
