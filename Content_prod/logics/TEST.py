file_dir = 'fixtures'
file_name = 'ESP Cup 22-23 prev.json'
path = 'Content_prod/cache/answers/fixtures/'

# настройка выгрузки в репо
from github import Github
from github import Auth     # Authentication is defined via github.Auth
import os
token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
repo_name = os.getenv('repository')
auth = Auth.Token(token)    # using an access token
g = Github(auth=auth)   # Public Web Github
repo = g.get_repo(repo_name)

# определение содержимого каталога выгрузки
dir_contents = repo.get_contents(path[:-1])     # последний слэш не нужен

import json
with open((os.path.abspath(__file__))[:-27]+path+file_name, 'r') as j:
    file_content = json.load(j)

print(file_content)
