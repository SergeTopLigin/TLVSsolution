# определение участников от нац лиги
# возвращает список участников = [{club: , id: }, ...]
# если стадия лиги одна:
    # 1. PTS/PL
    # 2. DIF/PL
    # 3. TL standings
    # 4. random
# если стадий лиги больше одной:
    # если количество участников стадии с макс приоритетом равно квоте: все участники этой стадии
    # если количество участников стадии с макс приоритетом больше квоты: среди участников этой стадии по rank этой стадии
    # если количество участников стадии с макс приоритетом меньше квоты: все участники этой стадии + среди участников следующей стадии по rank следующей стадии
# если участник от текущего сезона лиги входит в квоту предыдущего сезона: 
    # в квоту текущего сезона вместо этого участника включается следущий по критериям участник текущего сезона

# определение участников происходит по standings 
# для актуализации standings необходим актуальный fixtures
# актуализированы при расчете tournaments.py

def participants_nat_league(tourn, tourn_id, season, quota, prev):
    # tourn = tournaments.json[nat]['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json[nat]['tournaments'][tourn]['id']
    # season = tournaments.json[nat]['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json[nat]['tournaments'][tourn]['quota']
    # prev = список участников от league PREV season = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        best_define = []    # список с критериями определения лучших best_define = [{'club': , 'id': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
        import os
        import json
        import random
        with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/final_standings.json', 'r') as j:
            TL_standings = json.load(j)

        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-42]+'/cache/answers/standings'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1
                with open((os.path.abspath(__file__))[:-42]+'/cache/answers/standings/'+tourn_file, 'r') as j:
                    tourn_standings = json.load(j)
                break
        
        if file_find == 1:
            # если стадия лиги одна
            if len(tourn_standings['response'][0]['league']['standings']) == 1:
                for club in tourn_standings['response'][0]['league']['standings'][0]:
                    club_name = club['team']['name']
                    club_id = club['team']['id']
                    pts_pl = round(club['points'] / club['all']['played'], 2)
                    dif_pl = round(club['goalsDiff'] / club['all']['played'], 2)
                    if club['team']['name'] in TL_standings:
                        TL_rank = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_club == club_name][0]
                    else:
                        TL_rank = -5
                    random_rank = random.random()
                    best_define.append({'club': club_name, 'id': club_id, 'pts/pl': pts_pl, 'dif/pl': dif_pl, 'TL_rank': TL_rank, 'random_rank': random_rank})
                best_define.sort(key=lambda crit: (crit['pts/pl'], crit['dif/pl'], crit['TL_rank'], crit['random_rank']), reverse=True)
                for club in best_define:
                    if len(participants) < quota and club['id'] not in [prev_club['id'] for prev_club in prev]:
                        participants.append({'club': club['club'], 'id': club['id']})
            # если стадий лиги больше одной:
            else:    
                # составить список стадий лиги ["group"] с сортировкой по приоритету
                with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
                    groups_dict = json.load(j)
                for league in groups_dict:
                    if tourn in league and season in league:
                        # список стадий лиги ["group"] с сортировкой по приоритету
                        stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
                for stage in stage_prior:
                    for group in tourn_standings['response'][0]['league']['standings']:
                        for club in group:
                            if club['group'] == stage and club['team']['id'] not in [prev_club['id'] for prev_club in prev]:
                                participants.append({'club': club['team']['name'], 'id': club['team']['id']})
                                if len(participants) == quota:   break
                        if len(participants) == quota:   break
                    if len(participants) == quota:   break

        if file_find == 0:    # если файла нет - определить по файлу предыдущего сезона
            season = str(int(season[:2])-1)+'-'+str(int(season[3:])-1)
            for tourn_file in os.listdir((os.path.abspath(__file__))[:-42]+'/cache/answers/standings'):
                if tourn in tourn_file and season in tourn_file:
                    with open((os.path.abspath(__file__))[:-42]+'/cache/answers/standings/'+tourn_file, 'r') as j:
                        tourn_standings = json.load(j)
                    break
            # если стадия лиги одна
            if len(tourn_standings['response'][0]['league']['standings']) == 1:
                for club in tourn_standings['response'][0]['league']['standings'][0]:
                    club_name = club['team']['name']
                    club_id = club['team']['id']
                    pts_pl = round(club['points'] / club['all']['played'], 2)
                    dif_pl = round(club['goalsDiff'] / club['all']['played'], 2)
                    if club['team']['name'] in TL_standings:
                        TL_rank = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_club == club_name][0]
                    else:
                        TL_rank = -5
                    random_rank = random.random()
                    best_define.append({'club': club_name, 'id': club_id, 'pts/pl': pts_pl, 'dif/pl': dif_pl, 'TL_rank': TL_rank, 'random_rank': random_rank})
                best_define.sort(key=lambda crit: (crit['pts/pl'], crit['dif/pl'], crit['TL_rank'], crit['random_rank']), reverse=True)
                for club in best_define:
                    if len(participants) < quota and club['id'] not in [prev_club['id'] for prev_club in prev]:
                        participants.append({'club': club['club'], 'id': club['id']})
            # если стадий лиги больше одной:
            else:    
                # составить список стадий лиги ["group"] с сортировкой по приоритету
                with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
                    groups_dict = json.load(j)
                for league in groups_dict:
                    if tourn in league and season in league:
                        # список стадий лиги ["group"] с сортировкой по приоритету
                        stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
                for stage in stage_prior:
                    for group in tourn_standings['response'][0]['league']['standings']:
                        for club in group:
                            if club['group'] == stage and club['team']['id'] not in [prev_club['id'] for prev_club in prev]:
                                participants.append({'club': club['team']['name'], 'id': club['team']['id']})
                                if len(participants) == quota:   break
                        if len(participants) == quota:   break
                    if len(participants) == quota:   break
        
        return(participants)

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
