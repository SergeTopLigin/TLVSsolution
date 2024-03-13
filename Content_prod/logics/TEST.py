import os
import json
from modules.nat_tournaments import Nat_Tournaments
from modules.country_codes import country_codes

with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/tournaments.json', 'r') as j:
    Ass_TournRateQuot = json.load(j) # {ass: {rating: , quota: }} 
country_codes = country_codes()
Nat_Tournaments = Nat_Tournaments()
# {as_short:{'as_short': , 'as_full': , 'tournaments': {tytle:{'tytle': , 'season': , 'quota': , 'id': , 'type': , 'name': }}}}
tournaments = {}
for ass_n in Ass_TournRateQuot:
    # as_short
    if ass_n == 'TopLiga':      short = 'TL'
    else:                       short = ass_n
    # as_full
    if ass_n == 'UEFA':         full = 'UEFA'
    elif ass_n == 'TopLiga':    full = 'TopLiga'
    else:                       full = [country_codes[country_codes.index(elem)]['name'] for elem in country_codes if ass_n in elem['fifa']][0]
    # tournaments
    tourns = {}
    for tourn in Ass_TournRateQuot[ass_n]:
        if tourn[3] > 0:
            # tourn name
            if tourn[0] == 'UCL':       name = 'Champions League'
            elif tourn[0] == 'UEL':     name = 'Europa League'
            elif tourn[0] == 'UECL':    name = 'Conference League'
            elif tourn[0] == 'TopLiga': name = 'TopLiga'
            else:       name = [Nat_Tournaments[ass_n][Nat_Tournaments[ass_n].index(elem)][2] for elem in Nat_Tournaments[ass_n] if tourn[0] in elem[0]][0]
            tourns[tourn[0]] = {'tytle': tourn[0], 'season': tourn[1], 'quota': tourn[3], 'id': tourn[4], 'type': tourn[5], 'name': name}
    tournaments[ass_n] = {'as_short': short, 'as_full': full, 'tournaments': tourns}

# формирование строки из словаря в читабельном виде
# github принимает только str для записи в файл
tournaments_str = "{0:>31}".format('quota') + '\n'  # шапка таблицы
rank = 1
for ass in tournaments:
    tournaments_str += tournaments[ass]['as_short'] + '\n'
    for tourn in tournaments[ass]['tournaments']:
        tournaments_str += "      {0:20}  {1:>2}"\
        .format(tournaments[ass]['tournaments'][tourn]['name'], tournaments[ass]['tournaments'][tourn]['quota']) + '\n'
tournaments_str = tournaments_str[:-1]
print(tournaments_str)