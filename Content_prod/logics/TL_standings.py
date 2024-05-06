'''
расчет TL standings с формированием cache/sub_results/TL_standings.json
{
  club_name: {
    "IDapi": int,
    "nat": "STR",
    "TL_rank": float,
    "visual_rank": int
  }
}
'''

# try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

import os, json, time
with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)
TL_standings = {}
curr_timestamp = time.time()
year_ago = curr_timestamp - 3600*24*365

# из games удалить неучитываемые игры:
    # если последняя игра клуба закончилась ранее 365 дней назад - удалить клуб
    # если игра закончилась ранее: 365 дней назад + количество дней между ней и следующей 'fixed'
    # если игра закончилась ранее 365 дней назад и в период времени между ее выходом за 365 дней и выходом следующей за 365 дней клубом была сыграна новая игра
# for club in games:
#     del_match = []  # индексы удаляемых игр в списке клуба
#     # если последняя игра клуба закончилась ранее 365 дней назад - удалить клуб
#     if games[club][-1]['timestamp']+100*60 < year_ago:
#         del_club.append(club)
#     # если последняя игра клуба 'fixed' закончилась ранее 365 дней назад - удалить клуб
#     else:
#     # если игра закончилась ранее: 365 дней назад + количество дней между ней и следующей 'fixed'
#         for match in range(len(games[club])-1):     # последняя игра не учитывается
#             print(match)
#         # del_match.append(games[club].index(games[club][0]))

# for club in del_club:
#     games.pop(club)


    # выгрузка измененного games_upd.json в репо и на runner: /sub_results


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
        TL_standings[games[club][0]['club_name']]['IDapi'] = club
        TL_standings[games[club][0]['club_name']]['nat'] = games[club][0]['club_nat']
        inc_div = 0     # увеличение знаменателя за счет игры, вышедшей из 365 дней
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
                        inc_div = 1 - (curr_timestamp - match['timestamp']+115*60 - 3600*24*365) / \
                        (games[club][games[club].index(match)+1]['timestamp'] - match['timestamp'])
                    # else:   # иначе - удалить игру
        print(inc_div)
                # print(match['date'])
                # print(match['club_name'], match['match'], match['opp_TLrate'], match_pts, sep='***')
                # print()

# print(json.dumps(TL_standings, skipkeys=True, ensure_ascii=False, indent=2))



# except: 

#     # запись ошибки/исключения в переменную через временный файл
#     import traceback
#     with open("bug_file.txt", 'w+') as f:
#         traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
#         f.seek(0)                       # установка курсора в начало временного файла
#         bug_info = f.read()

#     # отправка bug_file в репозиторий GitHub и на почту
#     import os
#     mod_name = os.path.basename(__file__)[:-3]
#     from modules.gh_push import gh_push
#     gh_push(str(mod_name), 'bug_files', 'bug_file', bug_info)
#     from modules.bug_mail import bug_mail
#     bug_mail(str(mod_name), bug_info)
