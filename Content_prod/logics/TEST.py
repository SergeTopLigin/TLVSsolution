import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
    standings = json.load(j)
for club in standings:
    if str(standings[club]['IDapi']) not in list(games.keys()):
        print(club)
# print(list(games.keys()))