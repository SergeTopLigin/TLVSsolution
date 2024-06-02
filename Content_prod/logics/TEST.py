TL_standings = {
  "Manchester City": {
    "IDapi": 50,
    "nat": "ENG",
    "TL_rank": 2.2,
    "visual_rank": 100,
    "pl": 4
  },
  "Bayern Munich": {
    "IDapi": 157,
    "nat": "GER",
    "TL_rank": 2.07,
    "visual_rank": 96,
    "pl": 2
  },
  "Real Madrid": {
    "IDapi": 541,
    "nat": "ESP",
    "TL_rank": 1.66,
    "visual_rank": 84,
    "pl": 5
  },
  "Paris Saint Germain": {
    "IDapi": 85,
    "nat": "FRA",
    "TL_rank": 1.19,
    "visual_rank": 70,
    "pl": 1
  },
  "Liverpool": {
    "IDapi": 40,
    "nat": "ENG",
    "TL_rank": 1.13,
    "visual_rank": 69,
    "pl": 2
  },
  "Inter": {
    "IDapi": 505,
    "nat": "ITA",
    "TL_rank": 0.72,
    "visual_rank": 56,
    "pl": 1
  },
  "AS Roma": {
    "IDapi": 497,
    "nat": "ITA",
    "TL_rank": 0.69,
    "visual_rank": 56,
    "pl": 6
  }
}

import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

club_num = 0
club_prev_rank = 10
club_eqPos = 0

for club in TL_standings:
    club_num += 1
    if TL_standings[club]['TL_rank'] != club_prev_rank:
      TL_standings[club]['club_TLpos'] = club_num
      club_eqPos = 0
    else:
      club_eqPos += 1
      TL_standings[club]['club_TLpos'] = club_num - club_eqPos
    club_prev_rank = TL_standings[club]['TL_rank']
# 'club_qouta':               TL, UEFA, League, Cup
    TL_standings[club]['club_qouta'] = []
    for ass in participants:
        for tourn in participants[ass]['tournaments']:
            tourn_pos = 0
            for tourn_club in participants[ass]['tournaments'][tourn]['participants']:
                tourn_pos += 1
                if TL_standings[club]['IDapi'] == tourn_club['id']:
                    TL_standings[club]['club_qouta'].append({participants[ass]['tournaments'][tourn]['tytle']:tourn_pos})
    # 'club_NATpos'
    for club_id in games:
        if int(club_id) == TL_standings[club]['IDapi']:
            TL_standings[club]['club_NATpos'] = games[club_id][0]['club_NATpos']
            break



print(json.dumps(TL_standings, skipkeys=True, ensure_ascii=False, indent=2))