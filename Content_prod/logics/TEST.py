import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
    TL_standings = json.load(j)
club_id = 50
club_nat = [TL_standings[club]['nat'] for club in TL_standings if TL_standings[club]['IDapi'] == club_id][0]
print(club_nat)