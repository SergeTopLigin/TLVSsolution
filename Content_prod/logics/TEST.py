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
                    club_id = club['team']['id']
                    pts_pl = round(club['points'] / club['all']['played'], 2)
                    dif_pl = round(club['goalsDiff'] / club['all']['played'], 2)
                    if club['team']['name'] in TL_standings:
                        TL_rank = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_club == club['team']['name']][0]
                    else:
                        TL_rank = -5
                    random_rank = random.random()
                    best_define.append({'club': club_name, 'id': club_id, 'pts/pl': pts_pl, 'dif/pl': dif_pl, 'TL_rank': TL_rank, 'random_rank': random_rank})
            best_define.sort(key=lambda crit: (crit['pts/pl'], crit['dif/pl'], crit['TL_rank'], crit['random_rank']), reverse=True)
            number = 0
            for club in best_define:
                if number < quota and club['club'] not in [prev_club['club'] for prev_club in prev]:
                    number += 1
                    participants.append({'club': club['club'], 'id': club['id']})

number = 0
for club in standings:
    if standings[club]['IDapi'] in LeagueClubSetID and number < quota and club not in [prev_club['club'] for prev_club in prev]:
        number += 1
        participants.append({'club': club, 'id': standings[club]['IDapi']})
# учет 4-го критерия (рандом) при прочих равных
last_participant = participants[-1]['club']
# список для рандома: из клубов, TL rank которых = TL rank последнего по квоте участника
random_list = [{'club': club, 'id': standings[club]['IDapi']} for club in standings if standings[club]['TL_rank'] == standings[last_participant]['TL_rank']]
if len(random_list) > 0:
    slots = 0   # инициализация количества слотов в списке участников, занятых клубами с одинаковыми TL rank
    for club in random_list:
        if club in participants:
            slots += 1
            participants.remove(club)
    fills = 0    # счётчик заполнений слотов рандомом
    import random
    while fills < slots:
        fills += 1
        fill_club = random.choice(random_list)
        participants.append(fill_club)
        random_list.remove(fill_club)

print(participants)
print(random_list)
print(slots)
