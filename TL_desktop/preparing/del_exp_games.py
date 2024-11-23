import os, json
with open((os.path.abspath(__file__))[:-26]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

# удаление оставшихся игр expected
del_club = []
for club_id in games:
    new_game_set = []
    for game in games[club_id]:
        if game['game_status'] != 'expected':
            new_game_set.append(game)
    games[club_id] = new_game_set

# удаление клубов без игр
    if len(games[club_id]) == 0:
        del_club.append(club_id)
for club in del_club:
    games.pop(club)

print(json.dumps(games, skipkeys=True, ensure_ascii=False, indent=2))