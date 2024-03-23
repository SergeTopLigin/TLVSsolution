# модуль определения стадий нац лиг и их приоритетов
# названия стадий в списке standings_dict['response'][0]['league']['standings'] по ключу 'group'
# формировать club_set в tournaments.py и набирать participants из group с макс приоритетом в nat_league_groups.json
# если появляется новая стадия: 
    # автоматически присвоить новой стадии приоритет '0'
    # отправить на mail уведомление о необходимости расстановки приоритетов вручную
# {league+season: {group: приоритет, ...}}

def nat_league_groups(league, season, standings_dict):
# league должен соответствовать названию турнира в Nat_tournaments.Nat_Tournaments[ass][0]
# Season = YY-YY
# standings_dict = ответ на запрос standings

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        import json

        with open((os.path.abspath(__file__))[:-36]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
            groups_dict = json.load(j)
                
        for group in standings_dict['response'][0]['league']['standings']:
            for rank in group:
                if league+' '+season not in groups_dict:
                    groups_dict[league+' '+season] = {}
                if rank['group'] not in groups_dict[league+' '+season]:
                    groups_dict[league+' '+season][rank['group']] = 0
                    
                    # выгрузка nat_league_groups.json в репо и на runner: /sub_results
                    mod_name = os.path.basename(__file__)[:-3]
                    from modules.gh_push import gh_push
                    gh_push(str(mod_name), 'sub_results', 'nat_league_groups.json', groups_dict)
                    from modules.runner_push import runner_push
                    runner_push(str(mod_name), 'sub_results', 'nat_league_groups.json', groups_dict)

                    # если в groups_dict[league+' '+season] более одного элемента - 
                    if len(groups_dict[league+' '+season]) > 1:
                        # отправить на mail уведомление о необходимости расстановки приоритетов вручную
                        from modules.bug_mail import bug_mail
                        bug_mail(str(mod_name), 'необходимо расставить приоритеты стадий '+league+' '+season+' в /sub_results/nat_league_groups.json: \
                            макс лига[стадия: приоритет] для стадий, определяющих рейтинг турнира и участников от него')

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
