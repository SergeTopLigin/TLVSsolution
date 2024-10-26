import os, json
with open((os.path.abspath(__file__))[:-26]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)
matchday = []

for club_id in games:
    for game in games[club_id]:
        if game['game_status'] == 'expected':
            matchday.append({'tourn_short': game['tourn_short'], })

print(matchday)