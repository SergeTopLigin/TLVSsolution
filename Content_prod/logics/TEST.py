games = {1:[{"club_name": "Borussia Dortmund"}, {"club_name": "Paris Saint Germain"}], 2:[{"club_name": "Bayern Munich"}, {"club_name": "Real Madrid"}]}
del_match = [{"club_name": "Paris Saint Germain"}, {"club_name": "Borussia Dortmund"}]
del_club = []

# for club in games:
#     for match in del_match:
#         if match in games[club]:
#             games[club].remove(match)
#     if games[club] == []:
#         del_club.append(club)

# for club in del_club:
#     games.pop(club)
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

# main_stands = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['pl'] > 2}
# main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))

# сортировка TL_standings с учетом buffer: 
# в main_stands попадают клубы сыгравшие более 2 игр
main_stands = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['pl'] > 2}
main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
# в buffer_2pl попадают клубы, сыгравшие 2 игры
buffer_2pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['pl'] == 2}
buffer_2pl = dict(sorted(buffer_2pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
# в buffer_1pl попадают клубы, сыгравшие 1 игру
buffer_1pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['pl'] == 1}
buffer_1pl = dict(sorted(buffer_1pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
# переинициализация TL-standings
TL_standings = {}
for club in main_stands:
    TL_standings[club] = main_stands[club]
for club in buffer_2pl:
    TL_standings[club] = buffer_2pl[club]
for club in buffer_1pl:
    TL_standings[club] = buffer_1pl[club]

import json
print(json.dumps(TL_standings, skipkeys=True, ensure_ascii=False, indent=2))
