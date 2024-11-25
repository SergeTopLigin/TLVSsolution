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

import os, json, datetime
from modules.nat_tournaments import Nat_Tournaments
Nat_Tournaments = Nat_Tournaments()
mod_name = os.path.basename(__file__)[:-3]
with open((os.path.abspath(__file__))[:-32]+'/cache/final_standings.json', 'r', encoding='utf-8') as j:
    standings = json.load(j)
with open((os.path.abspath(__file__))[:-32]+'/workflow/10_participants.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)
with open((os.path.abspath(__file__))[:-32]+'/cache/games.json', 'r', encoding='utf-8') as j:
    games = json.load(j)

# определение текущего сезона
moment_datetime = datetime.datetime.utcnow()
Season = moment_datetime.year if moment_datetime.month > 7 else moment_datetime.year - 1
SeasonYY = str(Season)[2:]+'-'+str(Season+1)[2:]

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
    standings[club]['club_NATpos'] = ''
# 'club_qouta':               TL, UEFA, League, Cup
    standings[club]['club_qouta'] = []
    for ass in participants:
        for tourn in participants[ass]['tournaments']:
            for tourn_club in participants[ass]['tournaments'][tourn]['participants']:
                if standings[club]['IDapi'] == tourn_club['id']:
                    if ass == 'TopLiga':
                        tourn_status = 'curr'
                    else:
                        Start_Year = int('20'+participants[ass]['tournaments'][tourn]['season'][:2])
                        if moment_datetime.month < 8:     tourn_status = 'c'
                        if Start_Year < moment_datetime.year and moment_datetime.month > 7:     tourn_status = 'p'
                        if Start_Year == moment_datetime.year and moment_datetime.month > 7:     tourn_status = 'c'
                    if participants[ass]['as_short'] == 'UEFA':
                        standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'], tourn_status, tourn_club['pos']])
                    elif participants[ass]['as_short'] == 'TL':
                        standings[club]['club_qouta'].append([participants[ass]['as_short'], '', tourn_club['pos']])
                    else:
                        if 'LCup' in participants[ass]['tournaments'][tourn]['tytle']:
                            standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'][:6], tourn_status, tourn_club['pos']])
                        else:
                            standings[club]['club_qouta'].append([participants[ass]['tournaments'][tourn]['tytle'][:5], tourn_status, tourn_club['pos']])

# print(json.dumps(standings, skipkeys=True, ensure_ascii=False, indent=2))

# выгрузка final_standings.json
with open((os.path.abspath(__file__))[:-32]+'/cache/final_standings.json', 'w', encoding='utf-8') as j:
    json.dump(standings, j, skipkeys=True, ensure_ascii=False, indent=2)

# # формирование строки из словаря в читабельном виде
# final_standings_str = ''   # github принимает только str для записи в файл
# for club in standings:
#     quotas = [quota[0] for quota in standings[club]['club_qouta']]
#     club_qouta = ''
#     for quota in standings[club]['club_qouta']:
#         club_qouta += quota[0] + ' ' + quota[1] + ' ' + str(quota[2]) + ('     ' if len(str(quota[2]))==1 else '    ')
#     if 'TL' not in quotas and 'UCL' not in quotas and 'UEL' not in quotas and 'UECL' not in quotas:
#         club_qouta = ' '*22 + club_qouta
#     elif 'UCL' not in quotas and 'UEL' not in quotas and 'UECL' not in quotas:
#         club_qouta = ' '*12 + club_qouta
#     elif 'TL' not in quotas and ('UCL' in quotas or 'UEL' in quotas or 'UECL' in quotas):
#         club_qouta = club_qouta[:12] + ' '*10 + club_qouta[12:]
#     final_standings_str += "{0:>2}  {1:25}{2:3.0f}   {3:5.2f}   {4:>3} pl {5}    {6} {7:<3}      {8}".\
#     format(standings[club]['club_TLpos'], club, standings[club]['visual_rank'], standings[club]['TL_rank'], \
#         standings[club]['played'], 'bf' if standings[club]['buffer'] else '  ', standings[club]['nat'], standings[club]['club_NATpos'], club_qouta) + '\n'

# # выгрузка standings.txt в репо: /content и /content_commits  и на runner: /content
# gh_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
# runner_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
# gh_push(str(mod_name), 'content_commits', 'standings.txt', final_standings_str)
