'''
расчет TL standings с формированием cache/sub_results/TL_standings.json
{
  club_name: {
    "IDapi": int,
    "nat": "STR",
    "TL_rank": float,
    "visual_rank": int
    "played": int (last 365 days)
  }
}
'''

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json, time
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
    TL_standings = {}
    curr_timestamp = time.time()
    year_ago = curr_timestamp - 3600*24*365
    del_club = []   # список клубов на удаление

    for club in games:
        
        # в TL standings учитывается клуб, хотя бы одна игра которого имеет статус 'fixed' и ее окончание не позднее 365 дней назад
        club_in_stands = 0
        for match in games[club]:
            if match['game_status'] == 'fixed' and match['timestamp']+115*60 > year_ago:
                club_in_stands = 1
                break

        if club_in_stands == 1:
            # формирование полей 'IDapi' и 'nat' словаря TL_standings
            TL_standings[games[club][0]['club_name']] = {}
            TL_standings[games[club][0]['club_name']]['IDapi'] = int(club)
            TL_standings[games[club][0]['club_name']]['nat'] = games[club][0]['club_nat']
            inc_div = 0     # увеличение знаменателя за счет игры, вышедшей из 365 дней
            del_match = []  # список игр на удаление
            pts = 0     # сумма очков за все матчи за последние 365 дней
            pl = 0          # количество матчей за последние 365 дней
            for match in games[club]:
                if match['game_status'] == 'fixed':
                    # opponent's rating
                    if match['result'] == 'win':
                        if match['opp_TLrate'] == None or match['opp_TLrate'] <= -1.2:
                            match_pts = 3
                        elif match['opp_TLrate'] >= 2.2:
                            match_pts = 5
                        elif match['opp_TLrate'] < 2.2 and match['opp_TLrate'] > -1.2:
                            match_pts = ((match['opp_TLrate']+1.2) / (2.2+1.2)) * 2 + 3
                    elif match['result'] == 'draw':
                        if match['opp_TLrate'] == None or match['opp_TLrate'] <= -1.2:
                            match_pts = -1
                        elif match['opp_TLrate'] >= 2.2:
                            match_pts = 1
                        elif match['opp_TLrate'] < 2.2 and match['opp_TLrate'] > -1.2:
                            match_pts = ((match['opp_TLrate']+1.2) / (2.2+1.2)) * 2 - 1
                    elif match['result'] == 'lose':
                        if match['opp_TLrate'] == None or match['opp_TLrate'] <= -1.2:
                            match_pts = -3
                        elif match['opp_TLrate'] >= 2.2:
                            match_pts = -1
                        elif match['opp_TLrate'] < 2.2 and match['opp_TLrate'] > -1.2:
                            match_pts = ((match['opp_TLrate']+1.2) / (2.2+1.2)) * 2 - 3
                    # goal difference
                    if match['goalDiff'] == 2:      match_pts += 0.4
                    elif match['goalDiff'] == -2:   match_pts -= 0.4
                    elif match['goalDiff'] == 3:    match_pts += 0.7
                    elif match['goalDiff'] == -3:   match_pts -= 0.7
                    elif match['goalDiff'] == 4:    match_pts += 0.9
                    elif match['goalDiff'] == -4:   match_pts -= 0.9
                    elif match['goalDiff'] >= 5:    match_pts += 1 + (match['goalDiff']-5)*0.05
                    elif match['goalDiff'] <= -5:   match_pts -= 1 - (match['goalDiff']-5)*0.05
                    # actuality
                    if match['timestamp']+115*60 > year_ago:    # если игра закончилась в течение последних 365 дней
                        match_pts -= match_pts * (curr_timestamp - match['timestamp']+115*60) / (3600*24*365)
                        pl += 1
                    else:   # если игра закончилась раньше последних 365 дней
                        match_pts = 0
                        # если это не последняя игра fixed
                        # если следующая игра закончилась в течение последних 365 дней И
                        # если окончание последней игры fixed не после выхода окончания рассматриваемой игры за пределы последних 365 дней
                        if games[club].index(match) < len(games[club])-1 and games[club][games[club].index(match)+1]['game_status'] == 'fixed' and \
                        games[club][games[club].index(match)+1]['timestamp']+115*60 > year_ago and \
                        max([fixed_m['timestamp'] for fixed_m in games[club] if fixed_m['game_status']=='fixed'])+115*60 < \
                        match['timestamp']+115*60 + (3600*24*365):
                            # учесть увеличение знаменателя
                            inc_div = 1 - (curr_timestamp - (match['timestamp']+115*60) - 3600*24*365) / \
                            (games[club][games[club].index(match)+1]['timestamp'] - match['timestamp'])
                        else:   # иначе - удалить игру
                            del_match.append(match)
                    # сумма очков за все матчи за последние 365 дней
                    pts += match_pts
            # averaging (+ actuality match 365+)
            rate = pts / (pl + inc_div)
            # stability
            if pl <= 3:     rate *= 0.7
            elif pl == 4:   rate *= 0.8
            elif pl == 5:   rate *= 0.9
            elif pl >= 6:   rate *= 1
            # multiquota
            if 'TopLiga' not in games[club][0]['club_qouta']:
                ways = len(games[club][0]['club_qouta'])
            elif 'TopLiga' in games[club][0]['club_qouta']:
                ways = len(games[club][0]['club_qouta']) - 1
            if ways == 0:   rate *= 0.95
            elif ways == 1: rate *= 1
            elif ways == 2: rate *= 1.05
            elif ways == 3: rate *= 1.1
            # 0.00
            TL_standings[games[club][0]['club_name']]['TL_rank'] = round(rate, 2)
            # played (buffer)
            TL_standings[games[club][0]['club_name']]['played'] = pl
            # удаление игр, закончившихся более 365 дней назад, кроме игры, вышедшей за 365 дней последней
            for match in del_match:
                games[club].remove(match)
            # удаление клуба с пустым списком игр (если остались только unfinished / expected - клуб остается в файле)
            if games[club] == []:
                del_club.append(club)

    # удаление клуба с пустым списком игр (если остались только unfinished / expected - клуб остается в файле)
    for club in del_club:
        games.pop(club)

    # visual_rank
    TL_max = max([TL_standings[club]['TL_rank'] for club in TL_standings])
    TL_min = min([TL_standings[club]['TL_rank'] for club in TL_standings])
    for club in TL_standings:
        TL_standings[club]['visual_rank'] = int(round(100 * (TL_standings[club]['TL_rank'] - TL_min) / (TL_max - TL_min), 0))

    # сортировка TL_standings с учетом buffer: 
    # в main_stands попадают клубы сыгравшие более 2 игр
    main_stands = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] > 2}
    main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
    # в buffer_2pl попадают клубы, сыгравшие 2 игры
    buffer_2pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] == 2}
    buffer_2pl = dict(sorted(buffer_2pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
    # в buffer_1pl попадают клубы, сыгравшие 1 игру
    buffer_1pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] == 1}
    buffer_1pl = dict(sorted(buffer_1pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
    # переинициализация TL-standings
    TL_standings = {}
    for club in main_stands:
        TL_standings[club] = main_stands[club]
    for club in buffer_2pl:
        TL_standings[club] = buffer_2pl[club]
    for club in buffer_1pl:
        TL_standings[club] = buffer_1pl[club]

    # выгрузка скорректированного games.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'games.json', games)
    runner_push(str(mod_name), 'sub_results', 'games.json', games)

    # выгрузка TL_standings.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'TL_standings.json', games)
    runner_push(str(mod_name), 'sub_results', 'TL_standings.json', games)


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
