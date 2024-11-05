import json
with open('api_teams.json', 'r', encoding='utf-8') as j:
    teams = json.load(j)


for country in teams:
    teams_res = []
    for team in country['response']:
        teams_res.append([team['team']['name'], team['team']['id']])
        print('["'+team['team']['name']+'", '+str(team['team']['id'])+'],')
    print()