try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # определение UEFA rating
    UEFA_rating = 0
    for ID in TL_standings_rate:
        for SetID in UefaClubSetID:
            if ID == SetID:
                UEFA_rating += TL_standings_rate[ID] + 1.2
                break
    UEFA_rating = round(UEFA_rating, 2)


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
