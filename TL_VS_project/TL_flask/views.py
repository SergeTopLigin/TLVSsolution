from TL_flask import app
from datetime import datetime
from flask import render_template    # функция для вызова шаблонов по адресу \templates
# from flask import send_from_directory   # функция для вызова файлов

@app.route('/')
# @app.route('/home/')      # для Frozen-Flask нельзя использовать одну функцию на несколько адресов
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
        content = "About TopLiga")

@app.route('/robots.txt/')  # по этому адресу будет показан robots.txt из каталога static
def robots():
    # return app.send_static_file('robots.txt')     # опасный вариант
    # return send_from_directory('static', 'robots.txt')    # работает, но после Frozen - криво
    return "<p>User-agent: *<br>Disallow: /<br>User-agent: AdsBot-Google<br>Disallow: /</p>"    # html вместо txt