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
        ["UCL", "curr", 8],
        ["TopLiga", "curr", 1],
        ["ITA League", "prev", 2]
        ]
    }
}
'''

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json, datetime
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
        standings = json.load(j)
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
        participants = json.load(j)
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)

    DateNow = datetime.datetime.utcnow()    # текущая дата по UTC
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
        # если клуба нет в games
        if str(standings[club]['IDapi']) not in list(games.keys()):
            # извлечение времени последнего расчета
            with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/worktimes.json', 'r', encoding='utf-8') as j:
                worktimes = json.load(j)
            moment_timestamp = worktimes[-1][1]   # время момента расчета
            moment_datetime = datetime.date.fromtimestamp(moment_timestamp)
            # определение текущего сезона
            season = moment_datetime.year if moment_datetime.month > 7 else moment_datetime.year - 1
            season = str(season)[2:]+'-'+str(season+1)[2:]
            dir_standings = os.listdir((os.path.abspath(__file__))[:-27]+'/cache/answers/standings')
            file_season = season if standings[club]['nat']+' League '+season+' stan.json' in dir_standings else str(int(season[:2])-1)+'-'+season[:2]
            stand_file = standings[club]['nat'] + ' League ' + file_season + ' stan.json'
            with open((os.path.abspath(__file__))[:-27]+'/cache/answers/standings/'+stand_file, 'r', encoding='utf-8') as j:
                nat_standings = json.load(j)
            from modules.nat_league_groups import nat_league_groups
            nat_league_groups(standings[club]['nat']+' League', file_season, nat_standings)
            with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
                groups_dict = json.load(j)
            for league in groups_dict:
                if standings[club]['nat']+' League '+file_season in league:
                    # список стадий лиги ["league"] с сортировкой по приоритету
                    stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
            rank = 0
            flag = 0
            standings[club]['club_NATpos'] = 0
            for stage in stage_prior:
                for group in nat_standings['response'][0]['league']['standings']:
                    for gr_club in group:
                        if gr_club['group'] == stage and gr_club['team']['id'] == standings[club]['IDapi']:
                            standings[club]['club_NATpos'] = gr_club['rank'] + rank
                            flag = 1
                            break
                        if gr_club['group'] == stage and gr_club['rank'] == len(group):       # учет количества клубов из более высокой стадии
                            rank += gr_club['rank']
                    if flag == 1: break
                if flag == 1: break
    # 'club_qouta':               TL, UEFA, League, Cup
        standings[club]['club_qouta'] = []
        for ass in participants:
            for tourn in participants[ass]['tournaments']:
                tourn_pos = 0
                for tourn_club in participants[ass]['tournaments'][tourn]['participants']:
                    tourn_pos += 1
                    if standings[club]['IDapi'] == tourn_club['id']:
                        if ass == 'TopLiga':
                            tourn_status = 'curr'
                        else:
                            Start_Year = int('20'+participants[ass]['tournaments'][tourn]['season'][:2])
                            if DateNow.month < 8:     tourn_status = 'curr'
                            if Start_Year < DateNow.year and DateNow.month > 7:     tourn_status = 'prev'
                            if Start_Year == DateNow.year and DateNow.month > 7:     tourn_status = 'curr'
                        if participants[ass]['as_short'] == 'UEFA':
                            standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'], tourn_status, tourn_pos])
                        elif participants[ass]['as_short'] == 'TL':
                            standings[club]['club_qouta'].append([participants[ass]['as_short'], '', tourn_pos])
                        else:
                            if 'LCup' in participants[ass]['tournaments'][tourn]['tytle']:
                                standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'][:6], tourn_status, tourn_pos])
                            else:
                                standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'][:5], tourn_status, tourn_pos])

    # выгрузка final_standings.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'final_standings.json', standings)
    runner_push(str(mod_name), 'sub_results', 'final_standings.json', standings)

    # формирование строки из словаря в читабельном виде
    final_standings_str = ''   # github принимает только str для записи в файл
    for club in standings:
        quotas = [quota[0] for quota in standings[club]['club_qouta']]
        club_qouta = ''
        for quota in standings[club]['club_qouta']:
            club_qouta += quota[0] + ' ' + quota[1] + ' ' + str(quota[2]) + ('     ' if len(str(quota[2]))==1 else '    ')
        if 'TL' not in quotas and 'UCL' not in quotas and 'UEL' not in quotas and 'UECL' not in quotas:
            club_qouta = ' '*22 + club_qouta
        elif 'UCL' not in quotas and 'UEL' not in quotas and 'UECL' not in quotas:
            club_qouta = ' '*12 + club_qouta
        elif 'TL' not in quotas and ('UCL' in quotas or 'UEL' in quotas or 'UECL' in quotas):
            club_qouta = club_qouta[:12] + ' '*10 + club_qouta[12:]
        final_standings_str += "{0:>2}  {1:25}{2:3.0f}   {3:5.2f}    {4} {5:>2}      {6}".\
        format(standings[club]['club_TLpos'], club, standings[club]['visual_rank'], standings[club]['TL_rank'], \
            standings[club]['nat'], standings[club]['club_NATpos'], club_qouta) + '\n'

    # выгрузка standings.txt в репо: /content и /content_commits  и на runner: /content
    gh_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
    runner_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
    gh_push(str(mod_name), 'content_commits', 'standings.txt', final_standings_str)

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
