# определение участников от турниров с квотой
# если для сезона curr турнира есть рейтинг, но он еще не начался (results = 0): определение участников по TL standings (3 критерий)
    # В верхней стадии не обязательно лучшая группа: для нац лиг и групп уефа определять по standings, по верхней в ответе стадии. Если квота больше количества ее участников - добор из следующей
# 4 модуля для определения участников (возвращают списки участников):
    # uefa tourn season group set [quota, prev_list]
    # uefa tourn season playoff set [quota]
    # nat league season [quota, prev_list]
    # nat cup season [quota, prev_list]
# main:
    # вызов модулей, передавая квоту
    # при вызове модуля сезона curr передает еще список участников prev (всех турниров УЕФА или конкретного нац турнира) для исключения дублирования
    # формирует словарь participants.json = tournaments.json + {participants: [{club: , id: }]}

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os
    import json
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/tournaments.json', 'r') as j:
        tournaments = json.load(j)

    from modules.participants_uefa_group import participants_uefa_group
    from modules.participants_uefa_playoff import participants_uefa_playoff
    from modules.participants_nat_league import participants_nat_league
    from modules.participants_nat_cup import participants_nat_cup

    # UEFA participants
    # ОПРЕДЕЛИТЬ PLAYOFF/GROUP SET ПО КАТАЛОГУ CLUB_SETS
    # в tournaments есть 'tytle' и 'season'
    # если в /club_sets есть playoff set с 'tytle' и 'season': участники CURR из uefa tourn season playoff set
    # если в /club_sets есть только group set (нет playoff set) с 'tytle' и 'season': 
        # участники CURR из uefa tourn season group set
        # участники PREV из uefa tourn prev season playoff set, если он есть
    if 'UEFA' in tournaments:
        prev = []   # список участников турниров PREV (участники playoff set всех турниров УЕФА), используется во время групповой стадии следующего сезона
        dir_sets = os.listdir((os.path.abspath(__file__))[:-23]+'/cache/sub_results/club_sets')
        for tourn in tournaments['UEFA']['tournaments']:
            season = tournaments['UEFA']['tournaments'][tourn]['season']
            quota = tournaments['UEFA']['tournaments'][tourn]['quota']
            tourn_id = tournaments['UEFA']['tournaments'][tourn]['id']
            set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
            file_set = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name]
            for file_name in file_set:
                if 'playoff' in file_name:  # турнир CURR на стадии playoff или турнир PREV, его участники CURR/PREV по uefa tourn season playoff set
                    tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_playoff(tourn, tourn_id, season, quota)
                    for club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                        prev.append(club)
        for tourn in tournaments['UEFA']['tournaments']:
            season = tournaments['UEFA']['tournaments'][tourn]['season']
            quota = tournaments['UEFA']['tournaments'][tourn]['quota']
            tourn_id = tournaments['UEFA']['tournaments'][tourn]['id']
            set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
            file_set = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name]
            for file_name in file_set:
                if 'group' in file_name:  # турнир CURR на групповой стадии, его участники CURR по uefa tourn season group set
                    tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_group(tourn, tourn_id, season, quota, prev)
    # if 'UEFA' in tournaments:
    #     dir_sets = os.listdir((os.path.abspath(__file__))[:-23]+'/cache/sub_results/club_sets')
    #     for tourn in tournaments['UEFA']['tournaments']:
    #         season = tournaments['UEFA']['tournaments'][tourn]['season']
    #         quota = tournaments['UEFA']['tournaments'][tourn]['quota']
    #         set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
    #         file_set = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name]
    #         for file_name in file_set:
    #             if 'playoff' in file_name:  # турнир CURR на стадии playoff или турнир PREV, его участники CURR/PREV по uefa tourn season playoff set
    #                 tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_playoff(tourn, season, quota)
    #             else:   # турнир CURR на групповой стадии, его участники CURR по uefa tourn season group set
    #                 # предварительно определить участников из playoff турнира PREV
    #                 prev = []   # список участников турнира PREV
    #                 prev_season = str(int(season[:2])-1) + '-' + str(int(season[3:])-1)
    #                 # если в tournaments есть турнир PREV
    #                 if prev_season in [tournaments['UEFA']['tournaments'][tournP]['season'] for tournP in tournaments['UEFA']['tournaments'] \
    #                 if tournaments['UEFA']['tournaments'][tournP]['tytle'] == tournaments['UEFA']['tournaments'][tourn]['tytle']]:
    #                     prev_quota = [tournaments['UEFA']['tournaments'][tournP]['quota'] for tournP in tournaments['UEFA']['tournaments'] \
    #                         if tournaments['UEFA']['tournaments'][tournP]['tytle'] == tournaments['UEFA']['tournaments'][tourn]['tytle'] \
    #                         and tournaments['UEFA']['tournaments'][tournP]['season'] == prev_season][0]
    #                     prev = participants_uefa_playoff(tourn, prev_season, prev_quota)   # список участников турнира PREV
    #                 tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_group(tourn, season, quota, prev)

    # Nat participants
    from modules.country_codes import country_codes
    country_codes = country_codes()
    for ass in tournaments:
        if ass in [country['fifa'] for country in country_codes if ass == country['fifa']]:
            for tourn in tournaments[ass]['tournaments']:
                season = tournaments[ass]['tournaments'][tourn]['season']
                quota = tournaments[ass]['tournaments'][tourn]['quota']
                tourn_id = tournaments['UEFA']['tournaments'][tourn]['id']
                prev = []   # список участников турнира PREV
                prev_season = str(int(season[:2])-1) + '-' + str(int(season[3:])-1)
                # если в tournaments есть турнир PREV
                if prev_season in [tournaments[ass]['tournaments'][tournP]['season'] for tournP in tournaments[ass]['tournaments'] \
                if tournaments[ass]['tournaments'][tournP]['tytle'] == tournaments[ass]['tournaments'][tourn]['tytle']]:
                    prev_quota = [tournaments[ass]['tournaments'][tournP]['quota'] for tournP in tournaments[ass]['tournaments'] \
                        if tournaments[ass]['tournaments'][tournP]['tytle'] == tournaments[ass]['tournaments'][tourn]['tytle'] \
                        and tournaments[ass]['tournaments'][tournP]['season'] == prev_season][0]
                if tournaments[ass]['tournaments'][tourn]['type'] == 'League':
                    prev = participants_nat_league(tourn, tourn_id, prev_season, prev_quota, [])   # список участников турнира PREV
                    tournaments[ass]['tournaments'][tourn]['participants'] = participants_nat_league(tourn, tourn_id, season, quota, prev)
                if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup':
                    prev = participants_nat_cup(tourn, tourn_id, prev_season, prev_quota, [])   # список участников турнира PREV
                    tournaments[ass]['tournaments'][tourn]['participants'] = participants_nat_cup(tourn, tourn_id, season, quota, prev)

    # TL participants
    with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r') as j:
        standings = json.load(j)
    tournaments['TopLiga']['tournaments']['TopLiga']['participants'] = []
    rank = 0
    for club in standings:
        tournaments['TopLiga']['tournaments']['TopLiga']['participants'].append({'club': club, 'id': standings[club]['IDapi']})
        rank += 1
        if rank == 10:  break

    # формирование participants.json из словаря tournaments
    # и выгрузка participants.json в репо и на runner: /sub_results
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'sub_results', 'participants.json', tournaments)
    from modules.runner_push import runner_push
    runner_push(str(mod_name), 'sub_results', 'participants.json', tournaments)

    # формирование строки из словаря в читабельном виде
    # github принимает только str для записи в файл
    participants_str = ""
    for ass in tournaments:
        participants_str += tournaments[ass]['as_short'] + '\n'
        for tourn in tournaments[ass]['tournaments']:
            if tourn != 'TopLiga':
                participants_str += "      {0} {1:20}"\
                .format(tournaments[ass]['tournaments'][tourn]['season'], tournaments[ass]['tournaments'][tourn]['name']) + '\n'
            elif tourn == 'TopLiga':
                participants_str += "      {0:26}"\
                .format(tournaments[ass]['tournaments'][tourn]['name']) + '\n'
            for club in tournaments[ass]['tournaments'][tourn]['participants']:
                participants_str += ' '*20 + club['club'] + '\n'
    participants_str = participants_str[:-1]

    # выгрузка standings.txt в репо: /content и /content_commits  и на runner: /content
    gh_push(str(mod_name), 'content', 'participants.txt', participants_str)
    runner_push(str(mod_name), 'content', 'participants.txt', participants_str)
    gh_push(str(mod_name), 'content_commits', 'participants.txt', participants_str)

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
