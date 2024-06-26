from TL_flask import app
from datetime import datetime
from flask import render_template    # функция для вызова шаблонов по адресу \templates
from flask import send_from_directory
import os

import TL_flask   # функция для вызова файлов

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

@app.route('/standings/')
def standings():
    with open((os.path.abspath(__file__))[:-8]+'static/content/standings.txt', 'r', newline='\n') as f:
        standings = '<pre>' + f.read() + '</pre>'   # тэг <pre> передает содержимое без изменений (переносы строк, доп пробелы итд)
    return render_template(
        "standings.html",
        title = "Standings",
        content = standings)

@app.route('/associations/')
def associations():
    with open((os.path.abspath(__file__))[:-8]+'static/content/associations.txt', 'r', newline='\n') as f:
        associations = '<pre>' + f.read() + '</pre>'   # тэг <pre> передает содержимое без изменений (переносы строк, доп пробелы итд)
    return render_template(
        "associations.html",
        title = "Associations",
        content = associations)

@app.route('/tournaments/')
def tournaments():
    with open((os.path.abspath(__file__))[:-8]+'static/content/tournaments.txt', 'r', newline='\n') as f:
        tournaments = '<pre>' + f.read() + '</pre>'   # тэг <pre> передает содержимое без изменений (переносы строк, доп пробелы итд)
    return render_template(
        "tournaments.html",
        title = "Tournaments",
        content = tournaments)

@app.route('/participants/')
def participants():
    with open((os.path.abspath(__file__))[:-8]+'static/content/participants.txt', 'r', newline='\n') as f:
        participants = '<pre>' + f.read() + '</pre>'   # тэг <pre> передает содержимое без изменений (переносы строк, доп пробелы итд)
    return render_template(
        "participants.html",
        title = "Participants",
        content = participants)

@app.route('/games/')
def games():
    with open((os.path.abspath(__file__))[:-8]+'static/content/games.txt', 'r', newline='\n') as f:
        games = '<pre>' + f.read() + '</pre>'   # тэг <pre> передает содержимое без изменений (переносы строк, доп пробелы итд)
    return render_template(
        "games.html",
        title = "Games",
        content = games)

@app.route('/robots.txt/')  # по этому адресу будет показан robots.txt из каталога static
def robots():
    # return app.send_static_file('robots.txt')     # опасный вариант
    return send_from_directory('static', 'robots.txt')    # работает, но после Frozen - криво
    # return "<p>User-agent: *<br>Disallow: /<br>User-agent: AdsBot-Google<br>Disallow: /</p>"    # html вместо txt

# @app.errorhandler(404)  # оформление страницы с кодом 404 (страница не найдена) - только для динамо версии
# def pageNotFound(error):
#     return render_template(
#         'page404.html', 
#         title = "Page not found",
#         content = "Page not found"
#         ), 404  # возвращение сервером кода 404
#