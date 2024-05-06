import os, json, time
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)
for club in games:
    print(max([fixed_m['timestamp'] for fixed_m in games[club] if fixed_m['game_status']=='fixed']))