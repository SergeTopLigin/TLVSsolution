'''
отправить сегодняшние игры из 1_matchday.json в games.json с "game_status": "expected"
и составить games_str

games = {club_id: 
    [
        {
        'club_name':
        'date': 'date'              begining date and time
        'match': 'home - away G:G'              90' result
        'game_status': 'fixed/unfinished/expected'   
            'fixed' - фиксируемая, с завершенным основным временем
            'expected' - ожидаемая по текущему списку участников                

        'opponent': 'opponent'
        'opp_id':
        'result': 'win/draw/lose'   90'
        'opp_TLrate': float         on matchday
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
    ]
}

'''

import os, json, datetime
with open((os.path.abspath(__file__))[:-25]+'/workflow/01_matchday.json', 'r', encoding='utf-8') as j:
    matchday = json.load(j)
with open((os.path.abspath(__file__))[:-25]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)
with open((os.path.abspath(__file__))[:-25]+'/preparing/api_teams.json', 'r', encoding='utf-8') as j:
    api_teams = json.load(j)
with open((os.path.abspath(__file__))[:-25]+'/cache/final_standings.json', 'r', encoding='utf-8') as j:
    TL_standings = json.load(j)
with open((os.path.abspath(__file__))[:-25]+'/cache/teams_list.json', 'r', encoding='utf-8') as j:
    teams_list = json.load(j)
with open((os.path.abspath(__file__))[:-25]+'/cache/participants.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)

# определение текущего сезона
moment_datetime = datetime.datetime.utcnow()
season = moment_datetime.year if moment_datetime.month > 7 else moment_datetime.year - 1
season = str(season)[2:]+'-'+str(season+1)[2:]

# определение club_id
for match in matchday:
    match['id'] = {'home': None, 'away': None}
    for league in api_teams:
        for team in league['response']:
            if match['home'] == team['team']['name']:
                match['id']['home'] = team['team']['id']
            if match['away'] == team['team']['name']:
                match['id']['away'] = team['team']['id']

# формирование словаря игры в games.json
for match in matchday:
    if str(match['id']['home']) not in list(games.keys()):  # создание ключа
        games[str(match['id']['home'])] = []
    if str(match['id']['away']) not in list(games.keys()):  # создание ключа
        games[str(match['id']['away'])] = []
    for club_id in games:
        club_id = int(club_id)
        if match['id']['home'] == club_id or match['id']['away'] == club_id:
            game = {}   # результирующий словарь
        # club_name
            game['club_name'] = match['home'] if match['id']['home'] == club_id else match['away']
        # date
            game['date'] = match['date']
        # match
            game['match'] = match['home'] +' - '+ match['away']
        # game_status
            game['game_status'] = 'expected'
        # opponent
            game['opponent'] = match['away'] if match['id']['home'] == club_id else match['home']
        # opp_id
            game['opp_id'] = match['id']['away'] if match['id']['home'] == club_id else match['id']['home']
        # result
            game['result'] = None
        # opp_TLrate
            if game['opp_id'] in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
                game['opp_TLrate'] = [TL_standings[club]['TL_rank'] for club in TL_standings if TL_standings[club]['IDapi'] == game['opp_id']][0]
            else:
                game['opp_TLrate'] = None
        # goalDiff
            game['goalDiff'] = None
        # timestamp
            game['timestamp'] = int(datetime.datetime(int(game['date'][:4]), int(game['date'][5:7]), int(game['date'][8:10]), int(game['date'][11:13]), \
                int(game['date'][14:16])).timestamp())
        # 'tourn_short': str          
            game['tourn_short'] = match['tourn_short']
        # 'season': YY-YY
            game['season'] = match['season']
        # 'tourn_round': str
            game['tourn_round'] = match['tourn_round']
        # 'club_nat', 'opp_nat':
            for nat in teams_list:
                for team in teams_list[nat]:
                    if team == match['home'] and game['club_name'] == match['home']:
                        game['club_nat'] = nat
                    if team == match['away'] and game['club_name'] == match['away']:
                        game['club_nat'] = nat
                    if team == match['home'] and game['opponent'] == match['home']:
                        game['opp_nat'] = nat
                    if team == match['away'] and game['opponent'] == match['away']:
                        game['opp_nat'] = nat
        # 'club_TLpos':
            if club_id in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
                game['club_TLpos'] = [list(TL_standings.values()).index(club)+1 for club in list(TL_standings.values()) if club['IDapi'] == club_id][0]
            else:
                game['club_TLpos'] = None
        # 'opp_TLpos'
            if game['opp_id'] in [TL_standings[club]['IDapi'] for club in TL_standings if TL_standings[club]['buffer'] == False]:
                game['opp_TLpos'] = [list(TL_standings.values()).index(club)+1 for club in list(TL_standings.values()) if club['IDapi'] == game['opp_id']][0]
            else:
                game['opp_TLpos'] = None
        # 'club_NATpos':
            game['club_NATpos'] = match['NATpos']['home'] if match['id']['home'] == club_id else match['NATpos']['away']
        # 'opp_NATpos':        
            game['opp_NATpos'] = match['NATpos']['away'] if match['id']['home'] == club_id else match['NATpos']['home']
        # 'club_qouta':
            game['club_qouta'] = []
            for p_ass in participants:
                for p_tourn in participants[p_ass]['tournaments']:
                    for p_participant in participants[p_ass]['tournaments'][p_tourn]['participants']:
                        if p_participant['id'] == club_id:
                            if participants[p_ass]['as_full'] == 'TopLiga': tourn_tytle = 'TL'
                            elif participants[p_ass]['as_full'] == 'UEFA':  tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle']
                            elif 'LCup' in participants[p_ass]['tournaments'][p_tourn]['tytle']:    tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle'][4:6]
                            else:   tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle'][4:5]
                            if participants[p_ass]['as_full'] == 'TopLiga':   tourn_season = '' 
                            elif participants[p_ass]['tournaments'][p_tourn]['season'] == season:  tourn_season = 'c'
                            else:   tourn_season = 'p'
                            pos = str(p_participant['pos'])
                            game['club_qouta'].append([tourn_tytle, tourn_season, pos])
        # 'opp_qouta':
            game['opp_qouta'] = []
            for p_ass in participants:
                for p_tourn in participants[p_ass]['tournaments']:
                    for p_participant in participants[p_ass]['tournaments'][p_tourn]['participants']:
                        if p_participant['id'] == game['opp_id']:
                            if participants[p_ass]['as_full'] == 'TopLiga':    tourn_tytle = 'TL'
                            elif participants[p_ass]['as_full'] == 'UEFA': tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle']
                            elif 'LCup' in participants[p_ass]['tournaments'][p_tourn]['tytle']:    tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle'][4:6]
                            else:   tourn_tytle = participants[p_ass]['tournaments'][p_tourn]['tytle'][4:5]
                            if participants[p_ass]['as_full'] == 'TopLiga':   tourn_season = '' 
                            elif participants[p_ass]['tournaments'][p_tourn]['season'] == season:  tourn_season = 'c'
                            else:   tourn_season = 'p'
                            pos = str(p_participant['pos'])
                            game['opp_qouta'].append([tourn_tytle, tourn_season, pos])

            games[str(club_id)].append(game)

with open((os.path.abspath(__file__))[:-25]+'/cache/games.json', 'w', encoding='utf-8') as j:
    json.dump(games, j, skipkeys=True, ensure_ascii=False, indent=2)


# создание словаря всех игр TL, исключая повторения путем использования fixture_id в качестве ключей
games_upd = {}
for club_id in games:
    for match in games[club_id]:
        timestamp = match['timestamp']
        home_team = match['match'].split(' - ')[0]
        away_team = (match['match'].split(' - ')[1]).split('   ')[0]
        fixture_id = match['date'][:10] + ' ' + home_team + ' - ' + away_team
        score = (match['match'].split(' - ')[1]).split('   ')[1] if len((match['match'].split(' - ')[1]).split('   ')) == 2 else 'NS'
        date = match['date'][:10]
        time = match['date'][11:16]
        tourn = match['tourn_short']
        season = match['season']
        tourn_round = match['tourn_round']
        # NAT
        home_nat = match['club_nat'] if home_team == match['club_name'] else match['opp_nat']
        away_nat = match['club_nat'] if away_team == match['club_name'] else match['opp_nat']
        # NATpos
        home_NATpos = match['club_NATpos'] if home_team == match['club_name'] else match['opp_NATpos']
        away_NATpos = match['club_NATpos'] if away_team == match['club_name'] else match['opp_NATpos']
        # TLpos
        home_TLpos = match['club_TLpos'] if home_team == match['club_name'] else match['opp_TLpos']
        away_TLpos = match['club_TLpos'] if away_team == match['club_name'] else match['opp_TLpos']
        # quota
        home_quota = match['club_qouta'] if home_team == match['club_name'] else match['opp_qouta']
        away_quota = match['club_qouta'] if away_team == match['club_name'] else match['opp_qouta']
        # добавить игру в обновленный словарь games
        games_upd[fixture_id] = {'timestamp':timestamp, 'home_team':home_team, 'away_team':away_team, 'score':score, 'date':date, 'time':time, \
        'tourn':tourn, 'season':season, 'tourn_round':tourn_round, 'home_nat':home_nat, 'away_nat':away_nat, 'home_NATpos':home_NATpos, \
        'away_NATpos':away_NATpos, 'home_TLpos':home_TLpos, 'away_TLpos':away_TLpos, 'home_quota':home_quota, 'away_quota':away_quota}
# сортировка игр от прошлого к будущему
games_upd = dict(sorted(games_upd.items(), key=lambda x: x[1].get("timestamp"), reverse=False))   

# print(json.dumps(games_upd, skipkeys=True, ensure_ascii=False, indent=2))

# формирование строки из словаря в читабельном виде
games_str = ''   
date = '' # инициализация даты
scoreNS = 0
for game in games_upd:
    # линия раздела между матчами fixed и unfinished
    if games_upd[game]['score'] == 'NS' and scoreNS == 0:
        games_str += '\n' + '='*80 + '\n'*2
    # tourn_short
    tourn_short = (games_upd[game]['tourn'][:6] if 'LCup' in games_upd[game]['tourn'] else games_upd[game]['tourn'][:5]).replace(' ', '-')
    # tourn_round
    if 'Regular Season' in games_upd[game]['tourn_round']:  tourn_round = games_upd[game]['tourn_round'].replace('Regular Season - ', 'RS-')
    elif 'Semi-finals' in games_upd[game]['tourn_round']:  tourn_round = '1/2'
    elif 'League Stage' in games_upd[game]['tourn_round']:  tourn_round = games_upd[game]['tourn_round'].replace('League Stage - ', 'LS-')
    elif 'Round of 16' in games_upd[game]['tourn_round']:  tourn_round = '1/8'
    else:   tourn_round = games_upd[game]['tourn_round'][:5]
    # score
    if 'NS' in games_upd[game]['score']:    
        score = 'TBD' if games_upd[game]['time']=='00:00' else games_upd[game]['time']
        scoreNS = 1
    else:   score = games_upd[game]['score']
    if games_upd[game]['date'] != date:
        games_str += ' '*40 + games_upd[game]['date'][8:] + '|' + games_upd[game]['date'][5:7] + '|' + games_upd[game]['date'][:4] + '\n'*2
        date = games_upd[game]['date']
    # врехняя строка
    games_str += "{0:^6}  {1:^5}   {2:>25}  {3:^5}  {4:<25}".\
    format(tourn_short, tourn_round, \
        games_upd[game]['home_team'], score, games_upd[game]['away_team']) + '\n'
    # quota
    if int(games_upd[game]['timestamp']) < 1725267241:
        home_quota = ''
        for tourn in games_upd[game]['home_quota']:
            if 'TopLiga' in tourn:  home_quota += 'TL|'
            elif 'League' in tourn:  home_quota += 'league|'
            elif 'LCup' in tourn:  home_quota += 'lcup|'
            elif 'Cup' in tourn:  home_quota += 'cup|'
            else:   home_quota += tourn+'|'
        home_quota = home_quota[:-1]
        away_quota = ''
        for tourn in games_upd[game]['away_quota']:
            if 'TopLiga' in tourn:  away_quota += 'TL|'
            elif 'League' in tourn:  away_quota += 'league|'
            elif 'LCup' in tourn:  away_quota += 'lcup|'
            elif 'Cup' in tourn:  away_quota += 'cup|'
            else:   away_quota += tourn+'|'
        away_quota = away_quota[:-1]
    else:
        home_quota = ''
        for tourn in games_upd[game]['home_quota']:
            home_quota += tourn[0] + tourn[1] + tourn[2] + ' | '
        home_quota = home_quota[:-3]
        away_quota = ''
        for tourn in games_upd[game]['away_quota']:
            away_quota += tourn[0] + tourn[1] + tourn[2] + ' | '
        away_quota = away_quota[:-3]

    # nat_pos
    home_NATpos = games_upd[game]['home_nat'] + '-' + str(games_upd[game]['home_NATpos'])
    away_NATpos = games_upd[game]['away_nat'] + '-' + str(games_upd[game]['away_NATpos'])
    # TL_pos
    home_TLpos = 'TL-' + str(games_upd[game]['home_TLpos'])
    away_TLpos = 'TL-' + str(games_upd[game]['away_TLpos'])
    # нижние строки
    games_str += ' '*27 + "{0:>6} {1:>7}  {2:^5}  {3:<7} {4:<6}".\
    format(home_NATpos, home_TLpos, '', away_TLpos, away_NATpos) + '\n'
    games_str += ' '*17 + "{0:>24}  {1:^5}  {2:<24}".\
    format(home_quota, '', away_quota) + '\n'*2

# формирование result/5_games.txt
with open((os.path.abspath(__file__))[:-25]+'/result/5_games.txt', 'w', encoding='utf-8') as f:
    f.write(games_str)

# формирование result/history/games.txt
CreateDate = str(datetime.datetime.utcnow())[:19].replace(":", "-").replace(' ','_')
with open((os.path.abspath(__file__))[:-25]+'/result/history/games '+CreateDate[:-9]+'.txt', 'w', encoding='utf-8') as f:
    f.write(games_str)
