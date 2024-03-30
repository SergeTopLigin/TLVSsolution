# определение участников от нац кубка
# возвращает список участников = [{club: , id: }, ...]

def participants_nat_cup(tourn, tourn_id, season, quota, prev):
    # tourn = tournaments.json[nat]['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json[nat]['tournaments'][tourn]['id']
    # season = tournaments.json[nat]['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json[nat]['tournaments'][tourn]['quota']
    # prev = список участников от cup PREV season = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        import os
        import json
        import random




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
        
        return([])
