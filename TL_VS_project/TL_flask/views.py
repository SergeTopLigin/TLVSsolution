from TL_flask import app
from datetime import datetime
from flask import render_template    # функция для вызова шаблонов по адресу \templates

@app.route('/')
@app.route('/home/')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title = "TopLiga",
        message = "TopLiga soon",
        content = ", now is " + formatted_now)

@app.route('/about/')
def about():
    return render_template(
        "about.html",
        title = "About TopLiga",
        content = "About")
