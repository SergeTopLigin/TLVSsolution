import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r') as j:
    TL_standings = json.load(j)

# same_ranks = [standings[club]['TL_rank'] for club in standings if standings[club]['TL_rank'] == ]
# all_ranks = []
# same_ranks = []
# for club in standings:
#     all_ranks.append(standings[club]['TL_rank'])
# for rank in range(0, len(all_ranks)-2):
#     if all_ranks[rank] == all_ranks[rank+1] and all_ranks[rank] not in same_ranks:
#         same_ranks.append(all_ranks[rank])
# print(same_ranks)

participants = []

season = '23-24'
tourn = 'UCL'
quota = 5
prev = [{'club': 'Inter', 'id': 505}, {'club': 'Real Madrid', 'id': 541}]

set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
LeagueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
dir_sets = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/sub_results/club_sets')
set_file = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name and 'playoff' in file_name][0]
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/club_sets/'+set_file, 'r') as f:
    for line in f:  # цикл по строкам
        kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
        end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
        LeagueClubSetID.append(int(line[kursor:end_substr]))

for clubID in LeagueClubSetID:
    club_name = [TL_club for TL_club in TL_standings if clubID == TL_standings[TL_club]['IDapi']][0]
    club_id = clubID
    if clubID in [TL_standings[TL_club]['IDapi'] for TL_club in TL_standings]:
        TL_rank = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_standings[TL_club]['IDapi'] == clubID][0]
    else:
        TL_rank = -5
    random_rank = random.random()
    best_define.append({'club': club_name, 'id': club_id, 'TL_rank': TL_rank, 'random_rank': random_rank})
best_define.sort(key=lambda crit: (crit['TL_rank'], crit['random_rank']), reverse=True)
number = 0
for club in best_define:
    if number < quota and club['club'] not in [prev_club['club'] for prev_club in prev]:
        number += 1
        participants.append({'club': club['club'], 'id': club['id']})

print(participants)
