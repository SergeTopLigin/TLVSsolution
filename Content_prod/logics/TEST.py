import os
import json
club = []
max_len = 0
for file in os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings'):
    if file.find('json') != -1:
        with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file, 'r', encoding='utf-8') as f:
            file_content = json.load(f)
        for club in file_content['response'][0]['league']['standings'][0]:
            if len(list(club['team']['name'])) > max_len:
                max_len = len(list(club['team']['name']))
            # print(club['team']['name'], len(list(club['team']['name'])))
print(max_len)