from flask import Flask
from TL_flask import app

@app.route('/')
@app.route('/home')
def home():
    return "Hello Flask!"