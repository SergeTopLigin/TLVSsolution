# определение участников group set турнира UEFA
# возвращает список участников = [{club: , id: }, ...]
# best from group stage by
    # 1. PTS/PL (only in group, without qualifing)
    # 2. DIF/PL (only in group, without qualifing)
    # 3. TL standings
    # 4. random
# if tourn N curr.season participant == UCL/UEL/UECL tourn prev.season participant => next tourn N curr.season participant

# определение участников происходит по standings 
# для актуализации standings необходим актуальный fixtures

def participants_uefa_group(tourn, season, quota, prev):
    # tourn = tournaments.json['UEFA']['tournaments'][tourn]['tytle']
    # season = tournaments.json['UEFA']['tournaments'][tourn]['season']
    # quota = tournaments.json['UEFA']['tournaments'][tourn]['quota']
    # prev = список участников турниров УЕФА PREV playoff = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        # если файла нет - определить по TL standings (3 критерий)
        # если для сезона curr турнира есть рейтинг, но он еще не начался (results = 0): определение участников по TL standings (3 критерий)



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
