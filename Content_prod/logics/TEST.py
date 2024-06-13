import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

# создание словаря игр, исключая повторения путем использования fixture_id в качестве ключей
games_upd = {}
for club_id in games:
    for match in games[club_id]:
        fixture_id = match['fixture_id']
        timestamp = match['timestamp']
        home_team = match['match'].split(' - ')[0]
        away_team = (match['match'].split(' - ')[1]).split('   ')[0]
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
        games_upd[str(fixture_id)] = {'timestamp':timestamp, 'home_team':home_team, 'away_team':away_team, 'score':score, 'date':date, 'time':time, \
        'tourn':tourn, 'season':season, 'tourn_round':tourn_round, 'home_nat':home_nat, 'away_nat':away_nat, 'home_NATpos':home_NATpos, \
        'away_NATpos':away_NATpos, 'home_TLpos':home_TLpos, 'away_TLpos':away_TLpos, 'home_quota':home_quota, 'away_quota':away_quota}
# сортировка игр от прошлого к будущему
games_upd = dict(sorted(games_upd.items(), key=lambda x: x[1].get("timestamp"), reverse=False))   

# print(json.dumps(games_upd, skipkeys=True, ensure_ascii=False, indent=2))

# формирование строки из словаря в читабельном виде
games_str = ''   # github принимает только str для записи в файл
date = '' # инициализация даты
for game in games_upd:
    # tourn_round
    if 'Regular Season' in games_upd[game]['tourn_round']:  tourn_round = games_upd[game]['tourn_round'].replace('Regular Season - ', 'RS-')
    elif 'Semi-finals' in games_upd[game]['tourn_round']:  tourn_round = '1/2'
    else:   tourn_round = games_upd[game]['tourn_round'][:5]
    # score
    if 'NS' in games_upd[game]['score']:    score = 'TBD' if games_upd[game]['time']=='00:00' else games_upd[game]['time']
    else:   score = games_upd[game]['score']
    if games_upd[game]['date'] != date:
        games_str += ' '*39 + games_upd[game]['date'][8:] + '|' + games_upd[game]['date'][5:7] + '|' + games_upd[game]['date'][:4] + '\n'*2
        date = games_upd[game]['date']
    # врехняя строка
    games_str += "{0:^5}  {1:^5}   {2:>25}  {3:^5}  {4:<25}".\
    format(games_upd[game]['tourn'][:5].replace(' ', '-'), tourn_round, \
        games_upd[game]['home_team'], score, games_upd[game]['away_team']) + '\n'
    # quota
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
    # nat_pos
    home_NATpos = games_upd[game]['home_nat'] + '-' + str(games_upd[game]['home_NATpos'])
    away_NATpos = games_upd[game]['away_nat'] + '-' + str(games_upd[game]['away_NATpos'])
    # TL_pos
    home_TLpos = 'TL-' + str(games_upd[game]['home_TLpos'])
    away_TLpos = 'TL-' + str(games_upd[game]['away_TLpos'])
    # нижние строки
    games_str += ' '*26 + "{0:>6} {1:>7}  {2:^5}  {3:<7} {4:<6}".\
    format(home_NATpos, home_TLpos, '', away_TLpos, away_NATpos) + '\n'
    games_str += ' '*16 + "{0:>24}  {1:^5}  {2:<24}".\
    format(home_quota, '', away_quota) + '\n'*2

print(games_str)