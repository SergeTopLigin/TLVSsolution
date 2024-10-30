import json
with open('api_teams.json', 'r', encoding='utf-8') as j:
    teams = json.load(j)
from modules.country_codes import country_codes
country_codes = country_codes()

teams_res = {}
for country in teams:
    for ass in country_codes:
        if ass['name'] == country['response'][0]['team']['country']:
            nat = ass['fifa']
            break
    teams_res[nat] = []
    for team in country['response']:
        teams_res[nat].append(team['team']['name'])
    teams_res[nat].sort()

import json, os
with open((os.path.abspath(__file__))[:-24]+'/cache/teams_list.json', 'w', encoding='utf-8') as j:
    json.dump(teams_res, j, skipkeys=True, ensure_ascii=False, indent=2)

# print(json.dumps(teams_res, skipkeys=True, ensure_ascii=False, indent=2))