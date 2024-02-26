# формирование словаря из запроса
# поиск и выдача необходимой информации из запроса
# функции модуля принимают в качестве параметра ответ на api запрос в формате строки

def CupIsFinished(answer):    # функция определяет закончен ли сезон в кубке
# сезон закончен, если есть round: Final и его status: short: FT / AET / PEN / CANC / AWD / WO
# параметр: ответ на апи запрос fixtures в формате строки
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        import json     # модуль формирование словаря из строки
        answer_dict = json.loads(answer)
        completion_status = ["FT", "AET", "PEN", "CANC", "AWD", "WO"]   # список статусов, обозначающих завершение матча
        # сезон закончен, если есть round: Final и его status: short: FT / AET / PEN / CANC / AWD / WO
        if answer_dict["response"][-1]["league"]["round"] == "Final" and \
            answer_dict["response"][-1]["fixture"]["status"]["short"] in completion_status:
            return("finished")
        else:
            return("in_progress")
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
        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этого кубка


def CupLast(answer):    # функция определяет дату последнего известного матча кубка
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        import datetime
        import json     # модуль формирование словаря из строки
        answer_dict = json.loads(answer)
        last_date = datetime.datetime(2000, 1, 1)
        for fixture in answer_dict["response"]:
            fixt_date = fixture["fixture"]["date"]
            fixt_date = datetime.datetime(int(fixt_date[:4]), int(fixt_date[5:7]), int(fixt_date[8:10]))
            if fixt_date > last_date:
                last_date = fixt_date
        return(last_date)
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
        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этого кубка


def CupFirst(answer):    # функция определяет дату первого матча кубка
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        import datetime
        import json     # модуль формирование словаря из строки
        answer_dict = json.loads(answer)
        first_date = datetime.datetime(2100, 1, 1)
        for fixture in answer_dict["response"]:
            fixt_date = fixture["fixture"]["date"]
            fixt_date = datetime.datetime(int(fixt_date[:4]), int(fixt_date[5:7]), int(fixt_date[8:10]))
            if fixt_date < first_date:
                first_date = fixt_date
        return(first_date)
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
        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этого кубка


def PrevCupInfluence(answer):    # функция определяет дату окончания влияния предыдущего сезона кубка: финал + 150 дней
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        import datetime
        import json     # модуль формирование словаря из строки
        answer_dict = json.loads(answer)
        LastInf_date = str([answer_dict['response'][answer_dict['response'].index(elem)]['fixture']['date'] \
            for elem in answer_dict['response'] if 'Final' in elem['league']['round']])[2:-2]
        LastInf_date = datetime.datetime(int(LastInf_date[:4]), int(LastInf_date[5:7]), int(LastInf_date[8:10]))
        LastInf_date += datetime.timedelta(days=150)
        return(LastInf_date)
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
        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этого кубка