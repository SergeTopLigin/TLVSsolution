import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants_nat.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
    TL_standings = json.load(j)
club_id = 50
# if club_id in [TL_standings[club]['IDapi'] for club in TL_standings]:
#     print('ok')

for club in TL_standings:
    print(TL_standings[club]['IDapi'])