# отправка файла в репозиторий GitHub

def gh_push(file_dir, file_name, content):
    
    # настройка выгрузки в репо
    from github import Github
    from github import Auth     # Authentication is defined via github.Auth
    import os
    token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
    repo_name = os.getenv('repository')
    auth = Auth.Token(token)    # using an access token
    g = Github(auth=auth)   # Public Web Github
    repo = g.get_repo(repo_name)

    # определение каталога сохранения файла

import traceback    # модуль трассировки для отслеживания ошибок
import datetime     # модуль для определния текущей даты для формирования имени bug_file
DateNowExc = str(datetime.datetime.utcnow())[:19].replace(":", "-")    # текущая дата по UTC, отформатированная под строку для имени файла
