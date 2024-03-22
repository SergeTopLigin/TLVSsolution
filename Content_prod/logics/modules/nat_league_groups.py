# модуль определения стадий нац лиг (в standings ключ group)
# если в запросе standings: в списке standings_dict['response'][0]['league']['standings'] более одного элемента:
    # добавить ассоциацию в sub_results в nat_league_groups.json и 
    # отправить на mail уведомление о необходимости сортировки groups
# формировать club_set в tournaments.py и набирать participants из groups в порядке их сортировки
# результат: json: названия стадий и их порядковые номера в списке standings_dict['response'][0]['league']['standings']
    # в порядке набора участников; club set для определения рейтинга турнира определяется по стадии [0]

def nat_league_groups(league, season, standings_dict):
# league должен соответствовать названию турнира в Nat_tournaments.Nat_Tournaments[ass][0]
# Season = YY-YY
# standings_dict = ответ на запрос standings

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        import json

        with open((os.path.abspath(__file__))[:-22]+'/cache/answers/standings/'+tourn_file, 'r', encoding='utf-8') as j:
            groups_dict = json.load(j)



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
