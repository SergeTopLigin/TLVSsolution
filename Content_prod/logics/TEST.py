participants = []   # результирующий список участников от турнира
import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r') as j:
    standings = json.load(j)

tourn = 'UCL'
season = '23-24'
quota = 10

file_find = 0   # флаг наличия файла турнира
for tourn_file in os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/fixtures'):
    if tourn in tourn_file and season in tourn_file:
        file_find = 1


if file_find == 0:    # если файла нет - определить по TL standings (3 критерий) по /club_sets
    set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
    LeagueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
    dir_sets = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/sub_results/club_sets')
    set_file = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name and 'playoff' in file_name][0]
    with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/club_sets/'+set_file, 'r') as f:
        for line in f:  # цикл по строкам
            kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
            end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
            LeagueClubSetID.append(int(line[kursor:end_substr]))
    number = 0
    for club in standings:
        if standings[club]['IDapi'] in LeagueClubSetID and number < quota:
            number += 1
            participants.append({'club': club, 'id': standings[club]['IDapi']})

print(participants)