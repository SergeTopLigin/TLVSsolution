'''
запись результатов игр из matchday.json в games.json
'''

import os, json
with open((os.path.abspath(__file__))[:-27]+'/workflow/01_matchday.json', 'r', encoding='utf-8') as j:
    matchday = json.load(j)
with open((os.path.abspath(__file__))[:-27]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

for match in matchday:
    for club_id in games:
        if games[club_id][0]['club_name'] in [match['home'], match['away']]:
            for game in games[club_id]:
                if match['home'] in game['match'] and match['away'] in game['match'] and match['date'] == game['date']:
                    game['match'] += ('   ' + str(match['goals']['home']) + ':' + str(match['goals']['away']))
                    game['game_status'] = 'fixed'
                    if match['goals']['home'] == match['goals']['away']:
                        game['result'] = 'draw'
                        game['goalDiff'] = 0
                    elif (game['club_name'] == match['home'] and match['goals']['home'] > match['goals']['away']) or \
                    (game['club_name'] == match['away'] and match['goals']['home'] < match['goals']['away']):
                        game['result'] = 'win'
                        game['goalDiff'] = max(match['goals']['home'], match['goals']['away']) - min(match['goals']['home'], match['goals']['away'])
                    elif (game['club_name'] == match['away'] and match['goals']['home'] > match['goals']['away']) or \
                    (game['club_name'] == match['home'] and match['goals']['home'] < match['goals']['away']):
                        game['result'] = 'lose'
                        game['goalDiff'] = min(match['goals']['home'], match['goals']['away']) - max(match['goals']['home'], match['goals']['away'])

with open((os.path.abspath(__file__))[:-26]+'/cache/games.json', 'w', encoding='utf-8') as j:
    json.dump(games, j, skipkeys=True, ensure_ascii=False, indent=2)

# print(json.dumps(games, skipkeys=True, ensure_ascii=False, indent=2))