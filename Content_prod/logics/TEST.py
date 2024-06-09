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
        games_upd[fixture_id] = {'timestamp':timestamp, 'home_team':home_team, 'away_team':away_team, 'score':score, 'date':date, 'time':time, \
        'tourn':tourn, 'season':season, 'tourn_round':tourn_round, 'home_nat':home_nat, 'away_nat':away_nat, 'home_NATpos':home_NATpos, \
        'away_NATpos':away_NATpos, 'home_TLpos':home_TLpos, 'away_TLpos':away_TLpos, 'home_quota':home_quota, 'away_quota':away_quota}
# сортировка игр от прошлого к будущему
games_upd = dict(sorted(games_upd.items(), key=lambda x: x[1].get("timestamp"), reverse=False))   

print(json.dumps(games_upd, skipkeys=True, ensure_ascii=False, indent=2))
