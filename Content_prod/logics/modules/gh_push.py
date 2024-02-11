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

        # дата в имени файла
        import datetime     # модуль для определния текущей даты для формирования имени bug_file
        CreateDate = str(datetime.datetime.utcnow())[:19].replace(":", "-").replace(' ','_')    # текущая дата по UTC, отформатированная под строку
        if file_name == 'bug_file':
            file_name = CreateDate+' '+str(main_mod)+".txt"
        if file_dir == 'content_commits':
            file_name = file_name[:-4]+' '+CreateDate+".txt"

        # настройка выгрузки в репо
        from github import Github
        from github import Auth     # Authentication is defined via github.Auth
        import os
        token = os.getenv('GH_token')   # обращение к переменной среды (секрету), установленной в .yml 
        repo_name = os.getenv('repository')
        auth = Auth.Token(token)    # using an access token
        g = Github(auth=auth)   # Public Web Github
        repo = g.get_repo(repo_name)

        # определение содержимого каталога выгружамеого файла
        dir_contents = repo.get_contents(str(os.path.dirname(os.path.abspath(__file__))[:-20])+path)
        if file_name in str(dir_contents):       # если в каталоге есть этот файл - сделать его update
            contents = repo.get_contents(str(os.path.dirname(os.path.abspath(__file__))[:-20])+path+file_name, ref="master")
            repo.update_file(contents.path, file_name+" update", file_content, contents.sha, branch="master")
        else:   # иначе создать файл
            repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")

        # if file_name in str(dir_contents) or\       # если в репозитории есть этот файл
        # (file_dir == 'content_commits' and file_name[:-24] in str(dir_contents)):   # или в /content_commits есть файл такого типа
        #     # достать его содержимое
        #     contents = repo.get_contents(str(os.path.dirname(os.path.abspath(__file__))[:-20])+path+file_name, ref="master")
        #     # если 
        #     repo.update_file(contents.path, "TL standings from current UEFA ranking without >1/365>", TL_standings_str, contents.sha, branch="main")
        # else:   # иначе создать файл
        #     repo.create_file("TLstandings_fromUEFAcoef.txt", "TL standings from current UEFA ranking without >1/365>", TL_standings_str, branch="main")

        # # отправка файла в репо
        # repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")

        g.close()

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
        from modules.bug_mail import bug_mail
        bug_mail(str(mod_name), 'не удалось отправить файл в репозиторий GitHub\n'+str(bug_info))
