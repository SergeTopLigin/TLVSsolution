# определение участников от турниров с квотой
# если для сезона curr турнира есть рейтинг, но он еще не начался (results = 0): определение участников по TL standings (3 критерий)
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
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/tournaments.json', 'r', encoding='utf-8') as j:
        tournaments = json.load(j)

    from modules.participants_uefa_group import participants_uefa_group
    from modules.participants_uefa_playoff import participants_uefa_playoff
    from modules.participants_nat_league import participants_nat_league
    from modules.participants_nat_cup import participants_nat_cup

    # инициализация списка participants для турниров:
    for ass in tournaments:
        for tourn in tournaments[ass]['tournaments']:
            tournaments[ass]['tournaments'][tourn]['participants'] = []

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
            if tournaments['UEFA']['tournaments'][tourn]['quota'] > 0:
                tourn_tytle = tournaments['UEFA']['tournaments'][tourn]['tytle']
                season = tournaments['UEFA']['tournaments'][tourn]['season']
                quota = tournaments['UEFA']['tournaments'][tourn]['quota']
                tourn_id = tournaments['UEFA']['tournaments'][tourn]['id']
                set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
                file_set = [file_name for file_name in dir_sets if tourn_tytle in file_name and set_season in file_name]
                for file_name in file_set:
                    if 'playoff' in file_name:  # турнир CURR на стадии playoff или турнир PREV, его участники CURR/PREV по uefa tourn season playoff set
                        tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_playoff(tourn_tytle, tourn_id, season, quota)
                        for club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                            prev.append(club)
        for tourn in tournaments['UEFA']['tournaments']:
            if tournaments['UEFA']['tournaments'][tourn]['quota'] > 0:
                tourn_tytle = tournaments['UEFA']['tournaments'][tourn]['tytle']
                season = tournaments['UEFA']['tournaments'][tourn]['season']
                quota = tournaments['UEFA']['tournaments'][tourn]['quota']
                tourn_id = tournaments['UEFA']['tournaments'][tourn]['id']
                set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
                file_set = [file_name for file_name in dir_sets if tourn_tytle in file_name and set_season in file_name]
                for file_name in file_set:
                    if 'group' in file_name:  # турнир CURR на групповой стадии, его участники CURR по uefa tourn season group set
                        tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_group(tourn_tytle, tourn_id, season, quota, prev)
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
                if tournaments[ass]['tournaments'][tourn]['quota'] > 0:
                    tourn_tytle = tournaments[ass]['tournaments'][tourn]['tytle']
                    season = tournaments[ass]['tournaments'][tourn]['season']
                    quota = tournaments[ass]['tournaments'][tourn]['quota']
                    tourn_id = tournaments[ass]['tournaments'][tourn]['id']
                    prev = []   # список участников турнира PREV
                    prev_season = str(int(season[:2])-1) + '-' + str(int(season[3:])-1)
                    prev_quota = 0   # инициализация квоты турнира PREV
                    # если в tournaments есть турнир PREV
                    if prev_season in [tournaments[ass]['tournaments'][tournP]['season'] for tournP in tournaments[ass]['tournaments'] \
                    if tournaments[ass]['tournaments'][tournP]['tytle'] == tournaments[ass]['tournaments'][tourn]['tytle']]:
                        prev_quota = [tournaments[ass]['tournaments'][tournP]['quota'] for tournP in tournaments[ass]['tournaments'] \
                            if tournaments[ass]['tournaments'][tournP]['tytle'] == tournaments[ass]['tournaments'][tourn]['tytle'] \
                            and tournaments[ass]['tournaments'][tournP]['season'] == prev_season][0]
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'League':
                        if prev_quota > 0:
                            prev = participants_nat_league(tourn_tytle, tourn_id, prev_season, prev_quota, [])   # список участников турнира PREV
                        tournaments[ass]['tournaments'][tourn]['participants'] = participants_nat_league(tourn_tytle, tourn_id, season, quota, prev)
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup':
                        if prev_quota > 0:
                            prev = participants_nat_cup(tourn_tytle, tourn_id, prev_season, prev_quota, [])   # список участников турнира PREV
                        tournaments[ass]['tournaments'][tourn]['participants'] = participants_nat_cup(tourn_tytle, tourn_id, season, quota, prev)

    # TL participants
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
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
    # participants_str = ""
    # for ass in tournaments:
    #     participants_str += tournaments[ass]['as_short'] + '\n'
    #     for tourn in tournaments[ass]['tournaments']:
    #         if tournaments[ass]['tournaments'][tourn]['quota'] > 0:
    #             if tourn != 'TopLiga':
    #                 participants_str += "      {0} {1:20}"\
    #                 .format(tournaments[ass]['tournaments'][tourn]['season'], tournaments[ass]['tournaments'][tourn]['name']) + '\n'
    #             elif tourn == 'TopLiga':
    #                 participants_str += "      {0:26}"\
    #                 .format(tournaments[ass]['tournaments'][tourn]['name']) + '\n'
    #             for club in tournaments[ass]['tournaments'][tourn]['participants']:
    #                 participants_str += ' '*30 + club['club'] + '\n'
    # participants_str = participants_str[:-1]

    # формирование строки из словаря в читабельном виде
    # представление participants по нац ассоциациям в порядке рейтинга ассоциаций
    # строка нац ассоциации
    # список квоты nat_league prev season с позициями перед клубами
    # список квоты nat_league curr season с позициями перед клубами
    # список невошедших в квоту nat_league без позиций но в порядке nat_league curr season
    # клубы из ассоциаций без квоты
    # поставить слева от клуба short_name турниров, в квоту которых он попал
    import time, datetime
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    from modules.apisports_key import api_key
    from modules.nat_tournaments import Nat_Tournaments
    from modules.bug_mail import bug_mail
    Nat_Tournaments = Nat_Tournaments()
    participants_str = ""
    # набрать список всех клубов участников
    participants_id = []
    for ass in tournaments:
        for tourn in tournaments[ass]['tournaments']:
            for club in tournaments[ass]['tournaments'][tourn]['participants']:
                participants_id.append(club['id'])
    club_account = []  # список учтеных клубов
    dir_standings = os.listdir((os.path.abspath(__file__))[:-23]+'/cache/answers/standings')
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/associations.json', 'r', encoding='utf-8') as j:
        associations = json.load(j)
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
        groups_dict = json.load(j)
    for ass in tournaments:
        # представление participants по нац ассоциациям в порядке рейтинга ассоциаций
        if ass in [country['fifa'] for country in country_codes if ass == country['fifa']]:
            # вписать строку нац ассоциации
            participants_str += tournaments[ass]['as_short'] + '\n'
            # список сезонов нац лиги с квотой > 0 в учитываемых турнирах
            league_seasons = [tournaments[ass]['tournaments'][tourn]['season'] for tourn in tournaments[ass]['tournaments'] \
                if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['quota'] > 0]
            league_name = [tournaments[ass]['tournaments'][tourn]['name'] for tourn in tournaments[ass]['tournaments'] \
                if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == max(league_seasons)][0]
            # если есть prev season
            if len(league_seasons) == 2:
                # вписать список квоты nat_league prev season с позициями перед клубами
                prev_parts = [tournaments[ass]['tournaments'][tourn]['participants'] for tourn in tournaments[ass]['tournaments'] \
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == min(league_seasons)][0]
                participants_str += "      {0} {1:20}".format(min(league_seasons), league_name) + '\n'
                rank = 1
                for club in prev_parts:
                    # uefa quota
                    uefa_quota = ''
                    for tourn in tournaments['UEFA']['tournaments']:
                        if club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                            uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                    # TL quota
                    TL_quota = ''
                    if club in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                        TL_quota = tournaments['TopLiga']['as_short']
                    # nat cup quota
                    nat_cup_quota = ''
                    for tourn in tournaments[ass]['tournaments']:
                        if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club in tournaments[ass]['tournaments'][tourn]['participants']:
                            nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
                    participants_str += ' '*27 + "{4}  {0:25}  {1:4}  {2:4}  {3:4}"\
                        .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
                    rank += 1
                    club_account.append(club['id'])
            # вписать список квоты nat_league curr season с позициями перед клубами
            curr_parts = [tournaments[ass]['tournaments'][tourn]['participants'] for tourn in tournaments[ass]['tournaments'] \
                if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == max(league_seasons)][0]
            participants_str += "      {0} {1:20}".format(max(league_seasons), league_name) + '\n'
            rank = 1
            for club in curr_parts:
                # uefa quota
                uefa_quota = ''
                for tourn in tournaments['UEFA']['tournaments']:
                    if club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                        uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                # TL quota
                TL_quota = ''
                if club in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                    TL_quota = tournaments['TopLiga']['as_short']
                # nat cup quota
                nat_cup_quota = ''
                for tourn in tournaments[ass]['tournaments']:
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club in tournaments[ass]['tournaments'][tourn]['participants']:
                        nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
                participants_str += ' '*27 + "{4}  {0:25}  {1:4}  {2:4}  {3:4}"\
                    .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
                rank += 1
                club_account.append(club['id'])
            # список невошедших в квоту nat_league без позиций но в порядке nat_league curr season
            # по nat standings
            file_standings = ass+' League'
            for file in dir_standings:
                if ass in file and file > file_standings:
                    file_standings = file
            with open((os.path.abspath(__file__))[:-23]+'/cache/answers/standings/'+file_standings, 'r', encoding='utf-8') as j:
                league_standings = json.load(j)
            for league in groups_dict:
                if file_standings[:16] in league:
                    # список стадий лиги ["league"] с сортировкой по приоритету
                    stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
            for stage in stage_prior:
                for group in league_standings['response'][0]['league']['standings']:
                    for club in group:
                        if club['group'] == stage and club['team']['id'] in participants_id and club['team']['id'] not in club_account:
                            # поставить справа от клуба short_name турниров, в квоту которых он попал
                            # uefa quota
                            uefa_quota = ''
                            for tourn in tournaments['UEFA']['tournaments']:
                                if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['UEFA']['tournaments'][tourn]['participants']:
                                    uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                            # TL quota
                            TL_quota = ''
                            if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                                TL_quota = tournaments['TopLiga']['as_short']
                            # nat cup quota
                            nat_cup_quota = ''
                            for tourn in tournaments[ass]['tournaments']:
                                if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and \
                                {'club': club['team']['name'], 'id': club['team']['id']} in tournaments[ass]['tournaments'][tourn]['participants']:
                                    nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
                            participants_str += ' '*30 + "{0:25}  {1:4}  {2:4}  {3:4}"\
                               .format(club['team']['name'], TL_quota, uefa_quota, nat_cup_quota) + '\n'
                            club_account.append(club['team']['id'])
    # клубы из ассоциаций без квоты
    other = list(set(participants_id) - set(club_account))
    if len(other) != 0:
        for ass in associations:
            if ass not in tournaments:
                file_standings = ass+' League'
                for file in dir_standings:
                    if ass in file and file > file_standings:
                        file_standings = file
                # если нет файла standings ассоциации
                if file_standings == ass+' League':
                    # добавить вручную ассоцацию в nat_tournaments.py и в /standings
                    gh_push(str(mod_name), 'bug_files', 'bug_file', "добавить вручную ассоцацию "+ass+" в nat_tournaments.py и в /standings")
                    bug_mail(str(mod_name), "добавить вручную ассоцацию "+ass+" в nat_tournaments.py и в /standings")
                with open((os.path.abspath(__file__))[:-23]+'/cache/answers/standings/'+file_standings, 'r', encoding='utf-8') as j:
                    league_standings = json.load(j)
                ass_str = ''
                update_time = ''
                print(ass)
                for group in league_standings['response'][0]['league']['standings']:
                    for club in group:
                        print(club['team']['name'])
                        if club['team']['id'] in other:
                            update_time = league_standings['response'][0]['league']['standings'][group][club]['update'][:10]
                            # обновить файл standings если standings не обновлялся больше недели
                            if datetime.datetime.utcnow() - datetime.timedelta(days=7) > \
                            datetime.datetime(int(update_time[:4]), int(update_time[5:7]), int(update_time[8:])):
                                LeagueID = [Nat_Tournaments[ass][tourn][3] for tourn in Nat_Tournaments[ass] if Nat_Tournaments[ass][tourn][0] == ass+' League'][0]
                                Season = str(datetime.datetime.utcnow().year if datetime.datetime.utcnow().month > 7 else datetime.datetime.utcnow().year -1)
                                answer = api_key("/standings?league="+str(LeagueID)+"&season="+Season)
                                time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical
                                # если 'results' != 0 - сохранить standings
                                answer_dict = json.loads(answer)
                                if answer_dict['results'] != 0:
                                    file_name = ass+' League '+Season[2:]+'-'+str(int(Season[2:])+1)+' stan.json'
                                    gh_push(str(mod_name), 'standings', file_name, answer_dict)
                                    runner_push(str(mod_name), 'standings', file_name, answer_dict)
                                else:
                                    gh_push(str(mod_name), 'bug_files', 'bug_file', "по запросу standings?league="+str(LeagueID)+"&season="+Season+" results=0")
                                    bug_mail(str(mod_name), "по запросу standings?league="+str(LeagueID)+"&season="+Season+" results=0")
                            break
                    if update_time != '': break
                dir_standings = os.listdir((os.path.abspath(__file__))[:-23]+'/cache/answers/standings')
                file_standings = ass+' League'
                for file in dir_standings:
                    if ass in file and file > file_standings:
                        file_standings = file
                with open((os.path.abspath(__file__))[:-23]+'/cache/answers/standings/'+file_standings, 'r', encoding='utf-8') as j:
                    league_standings = json.load(j)
                ass_str = ''
                for group in league_standings['response'][0]['league']['standings']:
                    for club in group:
                        if club['team']['id'] in other:
                            # строка асоциаии
                            if ass_str == '':
                                participants_str += ass + '\n'
                                ass_str = ass
                            # поставить справа от клуба short_name турниров, в квоту которых он попал
                            # uefa quota
                            uefa_quota = ''
                            for tourn in tournaments['UEFA']['tournaments']:
                                if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['UEFA']['tournaments'][tourn]['participants']:
                                    uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                            # TL quota
                            TL_quota = ''
                            if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                                TL_quota = tournaments['TopLiga']['as_short']
                            participants_str += ' '*30 + "{0:25}  {1:4}  {2:4}"\
                               .format(club['team']['name'], TL_quota, uefa_quota) + '\n'
                            club_account.append(club['team']['id'])
                            other = list(set(participants_id) - set(club_account))
                            if len(other) == 0:     break
                    if len(other) == 0:     break
            if len(other) == 0:     break
    # если в участниках не учтены все клубы из ассоциаций без квоты - значит: в associations.json нет ассоциации неучтеных клубов
    if len(other) != 0:
        gh_push(str(mod_name), 'bug_files', 'bug_file', "в associations.json нет ассоциации участника")
        bug_mail(str(mod_name), "в associations.json нет ассоциации участника")

    # выгрузка participants.txt в репо: /content и /content_commits  и на runner: /content
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
