import json
with open('07_nat_tournaments.json', 'r', encoding='utf-8') as j:
    teams = json.load(j)
print(teams)