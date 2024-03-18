import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/tournaments.json', 'r') as j:
    tournaments = json.load(j)

# # if 'UEFA' in tournaments:
# #     for tourn in tournaments['UEFA']['tournaments']:
# #         print(tourn)

# # dir_sets = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/sub_results/club_sets')
# dir_sets = ['UCL 2023-2024 playoff set.txt', 'UCL 2023-2024 group set.txt']
# # print([file_name for file_name in dir_sets if 'UCL' in file_name and '2023-2024' in file_name])

# if 'UEFA' in tournaments:
#     for tourn in tournaments['UEFA']['tournaments']:
#         season = tournaments['UEFA']['tournaments'][tourn]['season']
#         set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
#         file_set = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name]
#         for file_name in file_set:
#             if 'playoff' in file_name:
#                 print(tourn, season, 'playoff')
#                 # tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_playoff(tourn, season, quota)
#             else:   # турнир CURR на групповой стадии, его участники CURR по uefa tourn season group set
#                 prev_season = str(int(season[:2])-1) + '-' + str(int(season[3:])-1)
#                 prev_quota = 0
#                 if prev_season in [tournaments['UEFA']['tournaments'][tournP]['season'] for tournP in tournaments['UEFA']['tournaments'] \
#                     if tournaments['UEFA']['tournaments'][tournP]['tytle'] == tournaments['UEFA']['tournaments'][tourn]['tytle']]:
#                     prev_quota = [tournaments['UEFA']['tournaments'][tournP]['quota'] for tournP in tournaments['UEFA']['tournaments'] \
#                         if tournaments['UEFA']['tournaments'][tournP]['tytle'] == tournaments['UEFA']['tournaments'][tourn]['tytle'] \
#                         and tournaments['UEFA']['tournaments'][tournP]['season'] == prev_season][0]
#                 # prev = participants_uefa_playoff(tourn, prev_season, prev_quota)   # список участников турнира PREV
#                 # tournaments['UEFA']['tournaments'][tourn]['participants'] = participants_uefa_group(tourn, season, quota, prev)
#                 print(prev_quota)

# from modules.country_codes import country_codes
# country_codes = country_codes()
# for ass in tournaments:
#     if ass in [country['fifa'] for country in country_codes if ass == country['fifa']]:
#         print(ass)



# TL participants
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r') as j:
    standings = json.load(j)
tournaments['TopLiga']['tournaments']['TopLiga']['participants'] = []
rank = 0
for club in standings:
    tournaments['TopLiga']['tournaments']['TopLiga']['participants'].append({'club': club, 'id': standings[club]['IDapi']})
    # tournaments['TopLiga']['tournaments']['TopLiga']['participants'][rank]['id'] = standings[club]['IDapi']
    rank += 1
    if rank == 10:  break
# print(json.dumps(tournaments, skipkeys=True, ensure_ascii=False, indent=2))
print(tournaments['TopLiga']['tournaments']['TopLiga']['participants'])
# # формирование строки из словаря в читабельном виде
# # github принимает только str для записи в файл
# participants_str = ""
# for ass in tournaments:
#     participants_str += tournaments[ass]['as_short'] + '\n'
#     for tourn in tournaments[ass]['tournaments']:
#         if tourn != 'TopLiga':
#             participants_str += "      {0} {1:20}"\
#             .format(tournaments[ass]['tournaments'][tourn]['season'], tournaments[ass]['tournaments'][tourn]['name']) + '\n'
#         elif tourn == 'TopLiga':
#             participants_str += "      {0:26}"\
#             .format(tournaments[ass]['tournaments'][tourn]['name']) + '\n'
#             for club in tournaments[ass]['tournaments'][tourn]['participants']:
#                 participants_str += ' '*20 + club['club'] + '\n'
# participants_str = participants_str[:-1]

# print(participants_str)