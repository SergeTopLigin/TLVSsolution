import json
with open('api_teams.json', 'r', encoding='utf-8') as j:
    teams = json.load(j)

teams_res = {}
for country in teams:
    teams_res[country['response'][0]['team']['country']] = []
    for team in country['response']:
        teams_res[country['response'][0]['team']['country']].append(team['team']['name'])
    teams_res[country['response'][0]['team']['country']].sort()

print(json.dumps(teams_res, skipkeys=True, ensure_ascii=False, indent=2))