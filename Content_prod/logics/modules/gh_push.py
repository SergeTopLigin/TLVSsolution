# отправка файла в репозиторий GitHub
def gh_push(main_mod, file_dir, file_name, file_content):
# main_mod = имя файла запуска задачи
# file_dir = каталог размещения файла в репо
# file_name = имя файла
# file_content = содержание файла
# в file_dir досаточно указать папку, в которую надо сохранить файл: функция определит весь путь
# при отправке в bug_files указать file_name = bug_file: функция составит имя из даты и main_mod
    
    try:

        # определение каталога сохранения файла
        if file_dir == 'bug_files':             path = 'Content_prod/bug_files/'
        if file_dir == 'answers':               path = 'Content_prod/cache/answers/'
        if file_dir == 'sub_results':           path = 'Content_prod/cache/sub_results/'
        if file_dir == 'content_commits':       path = 'Content_prod/cache/content_commits/'
        if file_dir == 'content':               path = 'TL_VS_project/TL_flask/static/content/'

        # создание имени bug_file
        if file_name == 'bug_file':
            import datetime     # модуль для определния текущей даты для формирования имени bug_file
            BugDate = str(datetime.datetime.utcnow())[:19].replace(":", "-")    # текущая дата по UTC, отформатированная под строку
            file_name = BugDate+str(main_mod)+".txt"

        q=1/0

        # # настройка выгрузки в репо
        # from github import Github
        # from github import Auth     # Authentication is defined via github.Auth
        # import os
        # token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
        # repo_name = os.getenv('repository')
        # auth = Auth.Token(token)    # using an access token
        # g = Github(auth=auth)   # Public Web Github
        # repo = g.get_repo(repo_name)

        # # отправка файла в репо
        # repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")

        # g.close()

    except:

        # запись ошибки/исключения в переменную через временный файл
        import traceback
        with open("bug_file.txt", 'w+') as f:
            traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
            f.seek(0)                       # установка курсора в начало временного файла
            bug_info = f.read()

        # отправка bug_file на почту
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from .bug_mail import bug_mail
        bug_mail(str(mod_name), 'не удалось отправить файл в репозиторий GitHub\n'+str(bug_info))
