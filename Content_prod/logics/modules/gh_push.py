# отправка файла в репозиторий GitHub
def gh_push(main_mod, file_dir, file_name, file_content):
# main_mod = имя файла запуска задачи
# file_dir = каталог размещения файла в репо
# file_name = имя файла с расширением (пр: example.txt)
# file_content = содержание файла ИЛИ 'rename:NEWNAME' (без расширения) при переименовании файла
# в file_dir досаточно указать папку, в которую надо сохранить файл: функция определит весь путь
# при отправке в bug_files указать file_name = bug_file: функция составит имя из даты и main_mod
    
    try:

        # определение каталога сохранения файла
        if file_dir == 'bug_files':             path = 'Content_prod/bug_files/'
        if file_dir == 'answers':               path = 'Content_prod/cache/answers/'
        if file_dir == 'standings':             path = 'Content_prod/cache/answers/standings/'
        if file_dir == 'fixtures':              path = 'Content_prod/cache/answers/fixtures/'
        if file_dir == 'sub_results':           path = 'Content_prod/cache/sub_results/'
        if file_dir == 'club_sets':             path = 'Content_prod/cache/sub_results/club_sets/'
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

        # определение содержимого каталога выгрузки
        dir_contents = repo.get_contents(path[:-1])     # последний слэш не нужен
        
        import json
        # только для каталога content_commits: переписать файл, если содержание изменилось в сравнении с тем же типом последней версии
        # если содержание прежнее (хотя дата в имени другая) - не переписывать файл
        if (file_dir == 'content_commits') and (file_name[:-24] in str(dir_contents)):   # если в /content_commits есть файл такого типа
            # список файлов в /content_commits
            dir_content_commits = os.listdir((os.path.abspath(__file__))[:-26]+'/cache/content_commits')
            last_file = file_name[:-24]     # инициализация имени последнего коммита для цикла
            for file in dir_content_commits:
                # если в /content_commits есть файл однотипный выгружаемому И это последний из выгруженных по дате
                if file[:-24] == file_name[:-24] and file > last_file:
                    last_file = file   # сохраняем последний выгруженный однотипный файл в переменную
            with open((os.path.abspath(__file__))[:-26]+'/cache/content_commits/'+last_file, 'r') as f:
                if f.read() != file_content:    # если содержание меняется
                    repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")
        # для остальных каталогов
        elif file_content[:6] == 'rename':      # если требуется переименовать файл
            new_name = file_content[7:] # новое имя файла
            # извлечь его содержимое, удалить текущий и создать с новым именем
            if file_name[-3:] == 'txt':
                with open((os.path.abspath(__file__))[:-38]+path+file_name, 'r') as f:
                    file_content = f.read()
                contents = repo.get_contents(path+file_name, ref="master")
                repo.delete_file(contents.path, "remove "+file_name, contents.sha, branch="master")
                repo.create_file(path+new_name+'.txt', "add "+new_name+'.txt', file_content, branch="master")
            elif file_name[-4:] == 'json':
                with open((os.path.abspath(__file__))[:-38]+path+file_name, 'r') as j:
                    file_content = json.load(j)
                contents = repo.get_contents(path+file_name, ref="master")
                repo.delete_file(contents.path, "remove "+file_name, contents.sha, branch="master")
                repo.create_file(path+new_name+'.json', "add "+new_name+'.json', \
                    json.dumps(file_content, skipkeys=True, ensure_ascii=False, indent=2), branch="master")
        elif file_name in str(dir_contents):       
            # если в каталоге есть этот файл - сделать его update
            # GH не переписывает файл, если имя и содеражние не изменились
            contents = repo.get_contents(path+file_name, ref="master")
            if file_name[-3:] == 'txt':
                repo.update_file(contents.path, "update "+file_name, file_content, contents.sha, branch="master")
            elif file_name[-4:] == 'json':
                repo.update_file(contents.path, "update "+file_name, \
                    json.dumps(file_content, skipkeys=True, ensure_ascii=False, indent=2), contents.sha, branch="master")
        else:   # иначе создать файл
            if file_name[-3:] == 'txt':
                repo.create_file(path+file_name, "add "+file_name, file_content, branch="master")
            elif file_name[-4:] == 'json':
                repo.create_file(path+file_name, "add "+file_name, \
                    json.dumps(file_content, skipkeys=True, ensure_ascii=False, indent=2), branch="master")

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
