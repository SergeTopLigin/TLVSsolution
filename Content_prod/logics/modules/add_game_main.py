'''
модуль формирует из игры списка fixtures['response'] словарь вида:
    {
    'club_name':
    'date': 'date'              begining date and time
    'match': 'home - away G:G'              90' result
    'game_status': 'fixed/unfinished/expected'   
        'fixed' - фиксируемая, с завершенным основным временем
        'unfinished' - фиксируемая, начавшаяся, с незавершенным основным временем
        'expected' - ожидаемая по текущему списку участников                

    'opponent': 'opponent'
    'opp_id':
    'result': 'win/draw/lose'   90'
    'opp_TLrate': float         on match start
    'goalDiff': int             90'
    'timestamp': float          datetime in sec
    
    'fixture_id': int           id api sport
    'tourn_id': int             id api sport
    'tourn_name':
    'tourn_short': str          nat_tournaments[ass][0]
    'season': YY-YY
    'tourn_round': str
    'club_nat':
    'club_TLpos':
    'club_qouta':               TL, UEFA, League, Cup
    'club_NATpos'
    'opp_nat':
    'opp_TLpos':
    'opp_qouta':
    'opp_NATpos':
    }
для включения его в словарь games
'''

def add_game(fixture, club_id, tourn, season):      # fixture - словарь из списка fixtures['response']
                                                    # club_id - ключ словаря games, в список значения которого следует добавить игру
                                                    # tourn - имя турнира по int/nat_tournaments ass[tourn][0]
                                                    # season - YY-YY
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        game = {}   # результирующий словарь
        import os, json
    # club_name
        game['club_name'] = fixture['teams']['home']['name'] if fixture['teams']['home']['id'] == club_id else fixture['teams']['away']['name']
    # date
        game['date'] = fixture['fixture']['date']
    # match
        game['match'] = fixture['teams']['home']['name'] +' - '+ fixture['teams']['away']['name'] + \
            ('   '+ str(fixture['score']['fulltime']['home']) +':'+ str(fixture['score']['fulltime']['away']) if fixture['score']['fulltime']['home'] != None \
            else '')
    # game_status
        game['game_status'] = 'expected'
    # opponent
        game['opponent'] = fixture['teams']['away']['name'] if fixture['teams']['home']['id'] == club_id else fixture['teams']['home']['name']
    # opp_id
        game['opp_id'] = fixture['teams']['away']['id'] if fixture['teams']['home']['id'] == club_id else fixture['teams']['home']['id']
    # result
        game['result'] = None
    # opp_TLrate
        with open((os.path.abspath(__file__))[:-32]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
            TL_standings = json.load(j)
        if game['opp_id'] in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
            game['opp_TLrate'] = [TL_standings[club]['TL_rank'] for club in TL_standings if TL_standings[club]['IDapi'] == game['opp_id']][0]
        else:
            game['opp_TLrate'] = None
    # goalDiff
        game['goalDiff'] = None
    # timestamp
        game['timestamp'] = fixture['fixture']['timestamp']
    # fixture_id
        game['fixture_id'] = fixture['fixture']['id']
    # 'tourn_id': int             id api sport
        game['tourn_id'] = fixture['league']['id']
    # 'tourn_name':
        game['tourn_name'] = fixture['league']['name']
    # 'tourn_short': str          nat/int_tournaments[ass][0]
        game['tourn_short'] = tourn
    # 'season': YY-YY
        game['season'] = season
    # 'tourn_round': str
        game['tourn_round'] = fixture['league']['round']
    # 'club_nat':
        game['club_nat'] = ''
        dir_standings = os.listdir((os.path.abspath(__file__))[:-32]+'/cache/answers/standings')
        for stand_file in dir_standings:
            if 'League' in stand_file:
                with open((os.path.abspath(__file__))[:-32]+'/cache/answers/standings/'+stand_file, 'r', encoding='utf-8') as j:
                    standings = json.load(j)
                for group in standings['response'][0]['league']['standings']:
                    for club in group:
                        if club['team']['id'] == club_id:
                            game['club_nat'] = stand_file[:3]
                            break
                    if game['club_nat'] == stand_file[:3]:   break
                if game['club_nat'] == stand_file[:3]:   break
    # 'club_TLpos':
        if club_id in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
            game['club_TLpos'] = [list(TL_standings.values()).index(club)+1 for club in list(TL_standings.values()) if club['IDapi'] == club_id][0]
        else:
            game['club_TLpos'] = None
    # 'club_qouta':               TL, UEFA, League, Cup
        game['club_qouta'] = []
        with open((os.path.abspath(__file__))[:-32]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
            participants = json.load(j)
        for ass in participants:
            for tourn in participants[ass]['tournaments']:
                if club_id in [club['id'] for club in participants[ass]['tournaments'][tourn]['participants']]:
                    game['club_qouta'].append(participants[ass]['tournaments'][tourn]['tytle'])
    # 'club_NATpos'
        file_season = season if game['club_nat']+' League '+season+' stan.json' in dir_standings else str(int(season[:2])-1)+'-'+season[:2]
        stand_file = game['club_nat'] + ' League ' + file_season + ' stan.json'
        with open((os.path.abspath(__file__))[:-32]+'/cache/answers/standings/'+stand_file, 'r', encoding='utf-8') as j:
            nat_standings = json.load(j)
        from modules.nat_league_groups import nat_league_groups
        nat_league_groups(game['club_nat']+' League', file_season, nat_standings)
        with open((os.path.abspath(__file__))[:-32]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
            groups_dict = json.load(j)
        for league in groups_dict:
            if game['club_nat']+' League '+file_season in league:
                # список стадий лиги ["league"] с сортировкой по приоритету
                stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
        rank = 0
        game['club_NATpos'] = 0
        for stage in stage_prior:
            for group in nat_standings['response'][0]['league']['standings']:
                for club in group:
                    if club['group'] == stage and club['team']['id'] == club_id:
                        game['club_NATpos'] = club['rank'] + rank
                        break
                    if club['group'] == stage and club['rank'] == len(group):       # учет количества клубов из более высокой стадии
                        rank += club['rank']
                if game['club_NATpos'] != 0: break
            if game['club_NATpos'] != 0: break
    # 'opp_nat':
        game['opp_nat'] = ''
        for stand_file in dir_standings:
            if 'League' in stand_file:
                with open((os.path.abspath(__file__))[:-32]+'/cache/answers/standings/'+stand_file, 'r', encoding='utf-8') as j:
                    standings = json.load(j)
                for group in standings['response'][0]['league']['standings']:
                    for club in group:
                        if club['team']['id'] == game['opp_id']:
                            game['opp_nat'] = stand_file[:3]
                            break
                    if game['opp_nat'] == stand_file[:3]:   break
                if game['opp_nat'] == stand_file[:3]:   break
    # 'opp_TLpos':
        if game['opp_id'] in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
            game['opp_TLpos'] = [list(TL_standings.values()).index(club)+1 for club in list(TL_standings.values()) if club['IDapi'] == game['opp_id']][0]
        else:
            game['opp_TLpos'] = None
    # 'opp_qouta':          TL, UEFA, League, Cup
        game['opp_qouta'] = []
        for ass in participants:
            for tourn in participants[ass]['tournaments']:
                if game['opp_id'] in [club['id'] for club in participants[ass]['tournaments'][tourn]['participants']]:
                    game['opp_qouta'].append(participants[ass]['tournaments'][tourn]['tytle'])
    # 'opp_NATpos':
        file_season = season if game['opp_nat']+' League '+season+' stan.json' in dir_standings else str(int(season[:2])-1)+'-'+season[:2]
        stand_file = game['opp_nat'] + ' League ' + file_season + ' stan.json'
        with open((os.path.abspath(__file__))[:-32]+'/cache/answers/standings/'+stand_file, 'r', encoding='utf-8') as j:
            nat_standings = json.load(j)
        from modules.nat_league_groups import nat_league_groups
        nat_league_groups(game['opp_nat'] + ' League', file_season, nat_standings)
        with open((os.path.abspath(__file__))[:-32]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
            groups_dict = json.load(j)
        for league in groups_dict:
            if game['opp_nat'] + ' League '+file_season in league:
                # список стадий лиги ["league"] с сортировкой по приоритету
                stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
        rank = 0
        game['opp_NATpos'] = 0
        for stage in stage_prior:
            for group in nat_standings['response'][0]['league']['standings']:
                for club in group:
                    if club['group'] == stage and club['team']['id'] == game['opp_id']:
                        game['opp_NATpos'] = club['rank'] + rank
                        break
                    if club['group'] == stage and club['rank'] == len(group):
                        rank += club['rank']
                if game['opp_NATpos'] != 0: break
            if game['opp_NATpos'] != 0: break

        return(game)

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
