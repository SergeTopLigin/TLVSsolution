# настройка выгрузки в репо
from github import Github
from github import Auth     # Authentication is defined via github.Auth
import os
token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
repo_name = os.getenv('repository')
auth = Auth.Token(token)    # using an access token
g = Github(auth=auth)   # Public Web Github
repo = g.get_repo(repo_name)

path = "Content_prod/cache/content_commits/"

# определение содержимого каталога выгрузки
dir_contents = repo.get_contents(path)
# if file_name in str(dir_contents):       # если в каталоге есть этот файл - сделать его update
#     contents = repo.get_contents(str(os.path.dirname(os.path.abspath(__file__))[:-20])+path+file_name, ref="master")
#     repo.update_file(contents.path, file_name+" update", file_content, contents.sha, branch="master")
# else:   # иначе создать файл
#     repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")

print(dir_contents)