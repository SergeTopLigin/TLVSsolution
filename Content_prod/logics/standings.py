try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # пока игры не обрабатываются: просто копировать sub_results/init_standings.json > sub_results/standings.json
    # декодирование из файла
    import json
    import os
    with open((os.path.abspath(__file__))[:-20]+'/cache/sub_results/init_standings.json', 'r') as j:
        TL_standings = json.load(j)
    # формирование .json из словаря TL-standings
    # и выгрузка standings.json в репо: /sub_results
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    print('enter 1')
    gh_push(str(mod_name), 'sub_results', 'standings.json', \
        json.dumps(TL_standings, skipkeys=True, ensure_ascii=False, indent=2))

    # формирование строки из словаря в читабельном виде
    TL_standings_str = ''   # github принимает только str для записи в файл
    rank = 1
    for club in TL_standings:
        TL_standings_str += "{3:>2}  {0:20}   {2:3.0f}   {1:5.2f}".\
        format(club, TL_standings[club][0], TL_standings[club][1], str(rank)) + '\n'
        rank += 1

    # выгрузка standings.txt в репо: /content и /content_commits
    import os
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    print('enter 2')
    gh_push(str(mod_name), 'content', 'standings.txt', TL_standings_str)
    print('enter 3')
    gh_push(str(mod_name), 'content_commits', 'standings.txt', TL_standings_str)
    print('enter 4')
except: 

    # запись ошибки/исключения в переменную через временный файл
    import traceback
    with open("bug_file.txt", 'w+') as f:
        traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
        f.seek(0)                       # установка курсора в начало временного файла
        bug_info = f.read()

    # отправка bug_file в репозиторий GitHub и на почту
    import os
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'bug_files', 'bug_file', bug_info)
    from modules.bug_mail import bug_mail
    bug_mail(str(mod_name), bug_info)
