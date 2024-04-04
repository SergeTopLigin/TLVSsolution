import os, json

with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/BEL League 23-24 stan.json', 'r', encoding='utf-8') as f:
    standings_dict = json.load(f)

for stage in standings_dict["response"][0]["league"]["standings"]:
    for f_club in stage:
    # print(json.dumps(f_club, skipkeys=True, ensure_ascii=False, indent=2))
        print(f_club)
        print()
