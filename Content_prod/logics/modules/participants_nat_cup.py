# определение участников от нац кубка
# возвращает список участников = [{club: , id: }, ...]

# текущая стадия (1/8, 1/4 итд): последняя несыгранная, если известны все ее участники, или финал
# стадии с Replays объединяются с основными стадиями (пр: ENG Cup)
# бывают групповые стадии (пр: POR LCup): все матчи групп объединяются в одну стадию
# если количество участников текущей стадии равно квоте: все участники текущей стадии
# если количество участников текущей стадии больше квоты: победитель турнира или лучшие среди участников текущей стадии
# если количество участников текущей стадии меньше квоты: все участники текущей стадии + лучшие среди участников предыдущей стадии
# критерии определения лучших участников стадии:
    # 1. TL_rank (own curr + passed rivals on round date) +1.2 >=0
    # 2. PTS/PL
    # 3. DIF/PL
    # 4. TL standings
    # 5. random

# определение участников происходит по fixtures
# актуализация fixtures в cup_files, вызываемого из tournaments

def participants_nat_cup(tourn, tourn_id, season, quota, prev):
    # tourn = tournaments.json[nat]['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json[nat]['tournaments'][tourn]['id']
    # season = tournaments.json[nat]['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json[nat]['tournaments'][tourn]['quota']
    # prev = список участников от cup PREV season = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        import os
        import json
        import random
        from modules.history_standings import history_standings
        with open((os.path.abspath(__file__))[:-39]+'/cache/sub_results/final_standings.json', 'r') as j:
            TL_standings = json.load(j)

        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-39]+'/cache/answers/fixtures'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1
                with open((os.path.abspath(__file__))[:-39]+'/cache/answers/fixtures/'+tourn_file, 'r') as j:
                    tourn_fixtures = json.load(j)
                break
        if file_find == 0:  # если fixtures не найден - расчет по fixtures предыдущего сезона
            tourn_file = tourn+' '+str(int(season[:2])-1)+'-'+str(int(season[3:])-1)+' prev.json'
            with open((os.path.abspath(__file__))[:-39]+'/cache/answers/fixtures/'+tourn_file, 'r') as j:
                tourn_fixtures = json.load(j)

        # список всех стадий
        rounds = {}    # {round: {'last_date': , 'status': }}
        for fixture in tourn_fixtures['response']:
            if fixture['league']['round'].replace(' Replays', '') not in rounds or\
            fixture['fixture']['timestamp'] > [rounds[stage]['last_date'] for stage in rounds if fixture['league']['round'].replace(' Replays', '') == stage][0]:
                rounds[fixture['league']['round'].replace(' Replays', '')] = \
                {'last_date': fixture['fixture']['timestamp'], 'status': fixture['fixture']['status']['short']}
        # объединение всех групповых матчей в одну стадию 'Group'
        del_stage = []
        group_round = {}
        for stage in rounds:
            if 'Group' in stage:
                del_stage.append(stage)
                if 'Group' not in rounds:
                    group_round = {'last_date': rounds[stage]['last_date'], 'status': rounds[stage]['status']}
                if rounds[stage]['last_date'] > group_round['last_date']:
                    group_round = {'last_date': rounds[stage]['last_date'], 'status': rounds[stage]['status']}
        for stage in del_stage:
            rounds.pop(stage)
        if len(group_round) > 0:
            rounds['Group'] = {'last_date': group_round['last_date'], 'status': group_round['status']}
        # определение времени текущей стадии
        cancelled = ['FT', 'AET', 'PEN', 'CANC', 'AWD', 'WO']   # список статусов завершения
        rounds_cont_time = {stage: rounds[stage]['last_date'] for stage in rounds if rounds[stage]['status'] not in cancelled}   # время незавершенных стадий
        if len(rounds_cont_time) != 0:   # если есть хотя бы одна неавершенная стадия
            curr_round_time = min(rounds_cont_time.values())    # время текущей стадии - ранней из незавершенных
        else:
            curr_round_time = 4000000000      # символическое время след стадии, если еще не было жеребьевки и незавершенных стадий нет
        # выборка стадий не позднее текущей
        actual_rounds = {stage: rounds[stage]['last_date'] for stage in rounds if rounds[stage]['last_date'] <= curr_round_time}
        # сортировка стадий от текущей в прошлое
        actual_rounds = sorted(actual_rounds, key=lambda stage: actual_rounds[stage], reverse=True)
        # добавить в начало списка стадий 'next round', если еще не было ее жеребьевки и незавершенных стадий нет
        if curr_round_time == 4000000000 and actual_rounds[0] != 'Final':  
            actual_rounds.insert(0, 'next round')

        # добавить в квоту победителя кубка, если сыгран финал
        if curr_round_time == 4000000000 and actual_rounds[0] == 'Final':
            for fixture in tourn_fixtures['response']:
                if fixture['league']['round'] == 'Final':
                    participants.append({'club': fixture['teams']['home']['name'] if fixture['teams']['home']['winner'] else fixture['teams']['away']['name'],\
                        'id': fixture['teams']['home']['id'] if fixture['teams']['home']['winner'] else fixture['teams']['away']['id']})
            if quota == 1:
                return(participants)

        # расчет rivals_rank для стадии 'Group', если она есть
        if 'Group' in actual_rounds:
            # все участники групповой стадии
            group_set_home_id = [fixture['teams']['home']['id'] for fixture in tourn_fixtures['response'] if 'Group' in fixture['league']['round']]
            group_set_away_id = [fixture['teams']['away']['id'] for fixture in tourn_fixtures['response'] if 'Group' in fixture['league']['round']]
            group_set_id = list(set(group_set_home_id + group_set_away_id))
            # прошедшие в следующую стадию
            after_group = actual_rounds[actual_rounds.index('Group')-1]   # стадия, следующая после групповой
            next_set_home_id = [fixture['teams']['home']['id'] for fixture in tourn_fixtures['response'] if after_group in fixture['league']['round']]
            next_set_away_id = [fixture['teams']['away']['id'] for fixture in tourn_fixtures['response'] if after_group in fixture['league']['round']]
            next_set_id = list(set(next_set_home_id + next_set_away_id))
            # непрошедшие в следующую стадию
            group_loose_set_id = list(set(group_set_id)-set(next_set_id))
            # найти соперников прошедших
            # найти TL_rank соперников на дату игр с прошедшими
            # добавить TL_rank соперников в основной критерий прошедшего
            stage_winners = {}  # инициализация словаря вышедших из групп {id: {rival_id: [rival_TLranks]}} если в группе играется по два матча между соперниками дома и в гостях
            for club in next_set_id:
                stage_winners[club] = {}
                for fixture in tourn_fixtures['response']:
                    if 'Group' in fixture['league']['round'] and (club == fixture['teams']['home']['id'] or club == fixture['teams']['away']['id']) and\
                    (fixture['teams']['home']['id'] in group_loose_set_id or fixture['teams']['away']['id'] in group_loose_set_id):
                        # найти TL-standings на дату окончания стадии (ее последнего матча с участием прошедшего клуба)
                        round_last_date = fixture['fixture']['date'][:10]
                        hist_standings = history_standings(round_last_date)
                        # и добавить TL-rank непрошедшего в основной критерий прошедшего, если проигравший в hist_standings
                        if club == fixture['teams']['home']['id'] and\
                        fixture['teams']['away']['id'] in [hist_standings[hist_club]['IDapi'] for hist_club in hist_standings]:
                            stage_winners[club] = {fixture['teams']['away']['id']: []}
                            stage_winners[club][fixture['teams']['away']['id']].append(max([hist_standings[hist_club]['TL_rank'] for hist_club in hist_standings \
                                if hist_standings[hist_club]['IDapi'] == fixture['teams']['away']['id']][0] +1.2, 0))
                        if club == fixture['teams']['away']['id'] and\
                        fixture['teams']['home']['id'] in [hist_standings[hist_club]['IDapi'] for hist_club in hist_standings]:
                            stage_winners[club] = {fixture['teams']['home']['id']: []}
                            stage_winners[club][fixture['teams']['home']['id']].append(max([hist_standings[hist_club]['TL_rank'] for hist_club in hist_standings \
                                if hist_standings[hist_club]['IDapi'] == fixture['teams']['home']['id']][0] +1.2, 0))

        reg_time = ['ET', 'BT', 'P', 'FT', 'AET', 'PEN']  # список статусов окончания основного времени
        for stage in actual_rounds:
            # набор stage_set [{'club': , 'id': , 'pts': , 'dif': , 'pl': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
            stage_set = []
            if stage == 'next round' and actual_rounds[1] != 'Group':   
            # если известны все участники следующей стадии, но не было ее жеребьевки (отсутствует в fixtures)
            # И если предыдущая стадия не 'Group', для которой не посчитать 'next round' по 'goalsDiff'
                # набрать stage_set из победителей предыдущей стадии actual_rounds[1]
                next_stage_set = []
                # набрать список участников стадии [{'club': , 'id': , 'goalsDiff': (goals+penalty)}, ...]
                for fixture in tourn_fixtures['response']:
                    if fixture['league']['round'] == actual_rounds[1] and fixture['teams']['home']['id'] not in [club['id'] for club in next_stage_set]:
                        next_stage_set.append({'club': fixture['teams']['home']['name'], 'id': fixture['teams']['home']['id'], 'goalsDiff': 0})
                    if fixture['league']['round'] == actual_rounds[1] and fixture['teams']['away']['id'] not in [club['id'] for club in next_stage_set]:
                        next_stage_set.append({'club': fixture['teams']['away']['name'], 'id': fixture['teams']['away']['id'], 'goalsDiff': 0})
                for fixture in tourn_fixtures['response']:
                    pen_home = fixture['score']['penalty']['home'] if type(fixture['score']['penalty']['home']) == int else 0
                    pen_away = fixture['score']['penalty']['away'] if type(fixture['score']['penalty']['away']) == int else 0
                    for club in next_stage_set:
                        if fixture['league']['round'].replace(' Replays', '') == actual_rounds[1] and fixture['teams']['home']['id'] == club['id']:
                            club['goalsDiff'] += fixture['goals']['home'] + pen_home - fixture['goals']['away'] - pen_away
                        if fixture['league']['round'].replace(' Replays', '') == actual_rounds[1] and fixture['teams']['away']['id'] == club['id']:
                            club['goalsDiff'] += fixture['goals']['away'] + pen_away - fixture['goals']['home'] - pen_home
                # из списка участников стадии набрать список прошедших: goalsDiff > 0
                for club in next_stage_set:
                    if club['goalsDiff'] > 0:
                        stage_set.append({'club': club['club'], 'id': club['id'],\
                         'own_rivals_TLrank': 0,'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
            else:
                for fixture in tourn_fixtures['response']:
                    # набор stage_set участников действительных стадий (кроме 'next round')
                    # объединенная стадия 'Group' не сущ в fixtures
                    if (fixture['league']['round'] == stage or (stage == 'Group' and 'Group' in fixture['league']['round']))\
                    and fixture['teams']['home']['id'] not in [club['id'] for club in stage_set]\
                    and fixture['teams']['home']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['home']['name'], 'id': fixture['teams']['home']['id'],\
                         'own_rivals_TLrank': 0,'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
                    if (fixture['league']['round'] == stage or (stage == 'Group' and 'Group' in fixture['league']['round']))\
                    and fixture['teams']['away']['id'] not in [club['id'] for club in stage_set]\
                    and fixture['teams']['away']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['away']['name'], 'id': fixture['teams']['away']['id'],\
                         'own_rivals_TLrank': 0,'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})

            # набор критериев и сортировка stage_set
            for club in stage_set:
                for fixture in tourn_fixtures['response']:
                    if (fixture['league']['round'].replace(' Replays', '') in actual_rounds or ('Group' in actual_rounds and 'Group' in fixture['league']['round']))\
                    and club['id'] == fixture['teams']['home']['id'] and fixture['fixture']['status']['short'] in reg_time:
                        club['pl'] += 1
                        if fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away']:     club['pts'] += 3
                        elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:  club['pts'] += 1
                        club['dif'] += fixture['score']['fulltime']['home'] - fixture['score']['fulltime']['away']
                        # определение TL_rank пройденных соперников на момент окончания матча (учитывая Replays и Group round)
                        # для матча, в котором определится прошедший в следующую стадию (в единственном или в переигровке):
                        if fixture['teams']['home']['winner'] and 'Group' not in fixture['league']['round']:    
                            # найти TL-standings на дату окончания стадии (ее последнего матча с участием прошедшего клуба)
                            round_last_date = fixture['fixture']['date'][:10]
                            hist_standings = history_standings(round_last_date)
                            # и добавить TL-rank проигравшего в основной критерий победителя, если проигравший в hist_standings
                            if fixture['teams']['away']['id'] in [hist_standings[hist_club]['IDapi'] for hist_club in hist_standings]:
                                club['own_rivals_TLrank'] += max([hist_standings[hist_club]['TL_rank'] for hist_club in hist_standings if \
                                    hist_standings[hist_club]['IDapi'] == fixture['teams']['away']['id']][0] +1.2, 0)
                    if (fixture['league']['round'].replace(' Replays', '') in actual_rounds or ('Group' in actual_rounds and 'Group' in fixture['league']['round']))\
                    and club['id'] == fixture['teams']['away']['id'] and fixture['fixture']['status']['short'] in reg_time:
                        club['pl'] += 1
                        if fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away']:     club['pts'] += 3
                        elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:  club['pts'] += 1
                        club['dif'] += fixture['score']['fulltime']['away'] - fixture['score']['fulltime']['home']
                        # определение TL_rank пройденных соперников на момент окончания матча (учитывая Replays и Group round)
                        # для матча, в котором определится прошедший в следующую стадию (в единственном или в переигровке):
                        if fixture['teams']['away']['winner'] and 'Group' not in fixture['league']['round']:    
                            # найти TL-standings на дату окончания стадии (ее последнего матча с участием прошедшего клуба)
                            round_last_date = fixture['fixture']['date'][:10]
                            hist_standings = history_standings(round_last_date)
                            # и добавить TL-rank проигравшего в основной критерий победителя, если проигравший в hist_standings
                            if fixture['teams']['home']['id'] in [hist_standings[hist_club]['IDapi'] for hist_club in hist_standings]:
                                club['own_rivals_TLrank'] += max([hist_standings[hist_club]['TL_rank'] for hist_club in hist_standings if \
                                    hist_standings[hist_club]['IDapi'] == fixture['teams']['home']['id']][0] +1.2, 0)
                club['pts/pl'] = club['pts'] / club['pl']
                club['dif/pl'] = club['dif'] / club['pl']
                if club['id'] in [TL_standings[TL_club]['IDapi'] for TL_club in TL_standings]:
                    club['TL_rank'] = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_club == club['club']][0]
                else:
                    club['TL_rank'] = -5
                club['own_rivals_TLrank'] += max(club['TL_rank']+1.2, 0) if club['TL_rank'] >-5 else 0
        
                # если участник групповой стадии прошел дальше, добавить TL_rank соперников из группы участника, если они не вышли дальше
                # и внести id рассмотренного участника в group_set_calc
                if 'Group' in actual_rounds and club['id'] in next_set_id:
                    # при двух играх с одним соперником (дома и в гостях) берется среднее значение TL-rank пройденного соперника между датами игр
                    # {id: {rival_id: [rival_TLranks]}}
                    if stage_winners[club['id']]:
                        club['own_rivals_TLrank'] += [sum([sum(rival_rank)/len(rival_rank) for rival_rank in list(stage_winners[winner_id].values())]) \
                        for winner_id in stage_winners if winner_id == club['id']][0]

                club['own_rivals_TLrank'] = round(club['own_rivals_TLrank'], 2)
                club['random_rank'] = random.random()
            
            stage_set.sort(key=lambda crit: (crit['own_rivals_TLrank'], crit['pts/pl'], crit['dif/pl'], crit['TL_rank'], crit['random_rank']), reverse=True)

            # набор квоты турнира
            club_from_stage = 0
            while len(participants) < quota and club_from_stage < len(stage_set):
                participants.append({'club': stage_set[club_from_stage]['club'], 'id': stage_set[club_from_stage]['id']})
                club_from_stage += 1
            if quota == len(participants):
                break

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
