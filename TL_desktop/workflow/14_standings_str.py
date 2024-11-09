import os, json
mod_name = os.path.basename(__file__)[:-3]
with open((os.path.abspath(__file__))[:-29]+'/cache/final_standings.json', 'r', encoding='utf-8') as j:
    standings = json.load(j)

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
    final_standings_str += "{0:>2}  {1:25}{2:3.0f}   {3:5.2f}   {4:>3} pl {5}    {6} {7:<3}      {8}".\
    format(standings[club]['club_TLpos'], club, standings[club]['visual_rank'], standings[club]['TL_rank'], \
        standings[club]['played'], 'bf' if standings[club]['buffer'] else '  ', standings[club]['nat'], standings[club]['club_NATpos'], club_qouta) + '\n'

# формирование result/1_standings.txt
with open((os.path.abspath(__file__))[:-29]+'/result/1_standings.txt', 'w', encoding='utf-8') as f:
    f.write(final_standings_str)
