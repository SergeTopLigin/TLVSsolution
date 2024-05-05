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
del_club = []   # ключи удаляемых клубов

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
        if match['game_status'] == 'fixed' and match['timestamp']+100*60 > year_ago:
            club_in_stands = 1

    if club_in_stands == 1:
        print(club)

    # # формирование полей 'IDapi' и 'nat' словаря TL_standings
    # TL_standings[games[club][0]['club_name']] = {}
    # TL_standings[games[club][0]['club_name']]['IDapi'] = club
    # TL_standings[games[club][0]['club_name']]['nat'] = games[club][0]['club_nat']

    # for match in games[club]:
    #     # TL_rank = 
    #     if match['result'] == 'win':



# print(json.dumps(games, skipkeys=True, ensure_ascii=False, indent=2))



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
