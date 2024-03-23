import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/BEL League 23-24 stan.json', 'r') as j:
    tourn_standings = json.load(j)
print(len(tourn_standings['response'][0]['league']['standings']))