# import os, json
# tourn = 'ENG League'
# file_season = '23-24'
# club_id = 55
# club_NATpos = 0
# with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/ENG League 23-24 stan.json', 'r', encoding='utf-8') as j:
#     nat_standings = json.load(j)
# # from modules.nat_league_groups import nat_league_groups
# # nat_league_groups('BEL League', '23-24', nat_standings)
# with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
#     groups_dict = json.load(j)
# for league in groups_dict:
#     if tourn+' '+file_season in league:
#         # список стадий лиги ["league"] с сортировкой по приоритету
#         stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
# rank = 0
# for stage in stage_prior:
#     for group in nat_standings['response'][0]['league']['standings']:
#         for club in group:
#             if club['group'] == stage and club['team']['id'] == club_id:
#                 club_NATpos = club['rank'] + rank
#                 break
#             if club['group'] == stage and club['rank'] == len(group):
#                 rank += club['rank']
#         if club_NATpos != 0: break
#     if club_NATpos != 0: break
# print(club_NATpos)

season = '23-24'
print(str(int(season[:2])-1)+'-'+season[:2])