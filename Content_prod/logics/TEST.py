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

print(len(games[1]))

