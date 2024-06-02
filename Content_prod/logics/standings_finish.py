'''
добавить в final_standings.json ключ 'club_qouta' по только что рассчитаным participants
а также 'club_TLpos' и 'club_NATpos'
в квоту добавить подробнее: нац лига сезон и место

итоговый вид словаря final_standings.json
{
  "Atalanta": {
    "IDapi": 499,
    "nat": "ITA",
    "TL_rank": 1.63,
    "visual_rank": 67,
    "played": 3,
    "buffer": false,
добавить:
    "club_TLpos": 1
    "club_NATpos": 7
    "club_qouta": [
        {"UCL curr": 8},
        {"TopLiga": 1},
        {"ITA League prev": 2}
        ]
    }
}
'''

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
        standings = json.load(j)
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
        participants = json.load(j)
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)

    club_num = 0
    club_prev_rank = 10
    club_eqPos = 0
    for club in standings:
    # 'club_TLpos':
        club_num += 1
        if standings[club]['TL_rank'] != club_prev_rank:
          standings[club]['club_TLpos'] = club_num
          club_eqPos = 0
        else:
          club_eqPos += 1
          standings[club]['club_TLpos'] = club_num - club_eqPos
        club_prev_rank = standings[club]['TL_rank']
    # 'club_NATpos'
        for club_id in games:
            if int(club_id) == standings[club]['IDapi']:
                standings[club]['club_NATpos'] = games[club_id][0]['club_NATpos']
                break
    # 'club_qouta':               TL, UEFA, League, Cup
        standings[club]['club_qouta'] = []
        for ass in participants:
            for tourn in participants[ass]['tournaments']:
                tourn_pos = 0
                for tourn_club in participants[ass]['tournaments'][tourn]['participants']:
                    tourn_pos += 1
                    if standings[club]['IDapi'] == tourn_club['id']:
                        standings[club]['club_qouta'].append({participants[ass]['tournaments'][tourn]['tytle']:tourn_pos})

    # выгрузка final_standings.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'final_standings.json', standings)
    runner_push(str(mod_name), 'sub_results', 'final_standings.json', standings)


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
