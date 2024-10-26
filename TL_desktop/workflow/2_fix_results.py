'''
запись результатов игр из matchday.json в games.json
'''

import os, json
with open('1_matchday.json', 'r', encoding='utf-8') as j:
    matchday = json.load(j)
with open((os.path.abspath(__file__))[:-26]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

print(matchday)