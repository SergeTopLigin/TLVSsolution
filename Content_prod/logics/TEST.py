# games = {1:[{'game_status': 'unfinished'}]}
games = {}
for club_list in games:
    for game in games[club_list]:
        if game['game_status'] == 'unfinished':
            print('yes')