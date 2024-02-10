from github import Github
from github import Auth     # Authentication is defined via github.Auth
import os
token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
repo_name = os.getenv('repository')
auth = Auth.Token(token)    # using an access token
g = Github(auth=auth)   # Public Web Github
repo = g.get_repo(repo_name)

# # отправка файла в репо
# repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")

all_contents = repo.get_contents('Content_prod/cache/answers/standings/')
print(all_contents)

g.close()
