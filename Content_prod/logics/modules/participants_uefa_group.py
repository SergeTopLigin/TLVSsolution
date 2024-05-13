# определение участников group set турнира UEFA
# возвращает список участников = [{club: , id: }, ...]
# best from group stage by
    # 1. PTS/PL (only in group, without qualifing)
    # 2. DIF/PL (only in group, without qualifing)
    # 3. TL standings
    # 4. random
# if tourn N curr.season participant == UCL/UEL/UECL tourn prev.season participant => next tourn N curr.season participant

# определение участников происходит по standings 
# для актуализации standings необходим актуальный fixtures

def participants_uefa_group(tourn, tourn_id, season, quota, prev):
    # tourn = tournaments.json['UEFA']['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json['UEFA']['tournaments'][tourn]['id']
    # season = tournaments.json['UEFA']['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json['UEFA']['tournaments'][tourn]['quota']
    # prev = список участников турниров УЕФА PREV playoff = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        best_define = []    # список с критериями определения лучших best_define = [{'club': , 'id': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
        import os
        import json
        import random
        with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
            TL_standings = json.load(j)

        # актуализация fixtures и standings турнира
        from modules.uefa_tourn_files import uefa_tourn_files
        uefa_tourn_files(tourn, season, tourn_id, 'group')
        
        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-42]+'/cache/answers/standings'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1
                with open((os.path.abspath(__file__))[:-42]+'/cache/answers/standings/'+tourn_file, 'r', encoding='utf-8') as j:
                    tourn_standings = json.load(j)
                break
        
        if file_find == 1:
            for group in tourn_standings['response'][0]['league']['standings']:
                for club in group:
                    club_name = club['team']['name']
                    club_id = club['team']['id']
                    pts_pl = round(club['points'] / club['all']['played'], 2)
                    dif_pl = round(club['goalsDiff'] / club['all']['played'], 2)
                    if club['team']['name'] in TL_standings and TL_standings[club['team']['name']]['buffer'] == False:
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

        if file_find == 0:    # если файла нет - определить по TL standings (3 критерий) по /club_sets и random (4 критерий)
            set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
            LeagueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
            dir_sets = os.listdir((os.path.abspath(__file__))[:-42]+'/cache/sub_results/club_sets')
            set_file = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name and 'group' in file_name][0]
            with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/club_sets/'+set_file, 'r') as f:
                for line in f:  # цикл по строкам
                    kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
                    end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                    LeagueClubSetID.append(int(line[kursor:end_substr]))
            for clubID in LeagueClubSetID:
                club_name = [TL_club for TL_club in TL_standings if clubID == TL_standings[TL_club]['IDapi']][0]
                club_id = clubID
                if clubID in [TL_standings[TL_club]['IDapi'] for TL_club in TL_standings if TL_standings[TL_club]['buffer'] == False]:
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

        return(participants)

    except: 
        # запись ошибки/исключения в переменную через временный файл
        import traceback
        with open("bug_file.txt", 'w+') as f:
            traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
            f.seek(0)                       # установка курсора в начало временного файла
            bug_info = f.read()
        # отправка bug_file в репозиторий GitHub и на почту
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'bug_files', 'bug_file', bug_info)
        from modules.bug_mail import bug_mail
        bug_mail(str(mod_name), bug_info)
        
        return([])
