'''
отправить сегодняшние игры из 1_matchday.json в games.json с "game_status": "expected"

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
        

            games[str(club_id)].append(game)


print(json.dumps(games, skipkeys=True, ensure_ascii=False, indent=2))