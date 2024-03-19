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
    # season = tournaments.json['UEFA']['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json['UEFA']['tournaments'][tourn]['quota']
    # prev = список участников турниров УЕФА PREV playoff = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        import os
        import json
        with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/final_standings.json', 'r') as j:
            standings = json.load(j)

        # актуализация fixtures и standings турнира
        from modules.uefa_tourn_files import uefa_tourn_files
        uefa_tourn_files(tourn, season, tourn_id, 'group')
        
        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-42]+'/cache/answers/fixtures'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1



        if file_find == 0:    # если файла нет - определить по TL standings (3 критерий) по /club_sets
            set_season = '20'+season[:2]+'-20'+season[3:]    # YYYY-YYYY
            LeagueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
            dir_sets = os.listdir((os.path.abspath(__file__))[:-42]+'/cache/sub_results/club_sets')
            set_file = [file_name for file_name in dir_sets if tourn in file_name and set_season in file_name and 'group' in file_name][0]
            with open((os.path.abspath(__file__))[:-42]+'/cache/sub_results/club_sets/'+set_file, 'r') as f:
                for line in f:  # цикл по строкам
                    kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
                    end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                    LeagueClubSetID.append(int(line[kursor:end_substr]))
            number = 0
            for club in standings:
                if standings[club]['IDapi'] in LeagueClubSetID and number < quota:
                    number += 1
                    participants.append({'club': club, 'id': standings[club]['IDapi']})
            # учет 4-го критерия (рандом) при прочих равных
            last_participant = participants[-1]['club']
            random_list = [{'club': club, 'id': standings[club]['IDapi']} for club in standings if standings[club]['TL_rank'] == standings[last_participant]['TL_rank']]



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
        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этого кубка
