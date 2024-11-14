# формирование строки из словаря в читабельном виде и 
    # participants_nat.json (словарь участников по нац ассоциациям)
# представление participants по нац ассоциациям в порядке рейтинга ассоциаций
# строка нац ассоциации
# список квоты nat_league prev season с позициями перед клубами
# список квоты nat_league curr season с позициями перед клубами
# список невошедших в квоту nat_league без позиций но в порядке nat_league curr season
# клубы из ассоциаций без квоты
# поставить слева от клуба short_name турниров, в квоту которых он попал

import os, json
with open((os.path.abspath(__file__))[:-28]+'/workflow/10_participants.json', 'r', encoding='utf-8') as j:
    tournaments = json.load(j)

import datetime
from modules.nat_tournaments import Nat_Tournaments
Nat_Tournaments = Nat_Tournaments()
from modules.country_codes import country_codes
country_codes = country_codes()
participants_str = ""
participants_nat = {}
# определение curr и prev турниров
DateNow = datetime.datetime.utcnow()
if DateNow.month > 7:   curr_season = str(DateNow.year)[2:]+'-'+str(DateNow.year+1)[2:]
else:   curr_season = str(DateNow.year-1)[2:]+'-'+str(DateNow.year)[2:]
# набрать списки 
participants_id = []    # всех клубов участников
parts_not_nat = []      # клубов в квотах УЕФА и ТЛ
for ass in tournaments:
    for tourn in tournaments[ass]['tournaments']:
        for club in tournaments[ass]['tournaments'][tourn]['participants']:
            if club['id'] not in participants_id:
                participants_id.append(club['id'])
            if (ass == 'UEFA' or ass == 'TopLiga') and club['id'] not in [club['id'] for club in parts_not_nat]:
                parts_not_nat.append(club)
for ass in tournaments:
    ass_league = []
    for tourn in tournaments[ass]['tournaments']:
        if tournaments[ass]['tournaments'][tourn]['type'] =='League':
            for club in tournaments[ass]['tournaments'][tourn]['participants']:
                ass_league.append(club['id'])
        if tournaments[ass]['tournaments'][tourn]['type'] =='Cup':
            for club in tournaments[ass]['tournaments'][tourn]['participants']:
                if club['id'] not in ass_league and club['id'] not in parts_not_nat:
                    parts_not_nat.append(club)

club_account = []  # список учтеных клубов
for ass in tournaments:
    # представление participants по нац ассоциациям в порядке рейтинга ассоциаций
    if ass in [country['fifa'] for country in country_codes if ass == country['fifa']]:
        # вписать строку нац ассоциации
        participants_str += tournaments[ass]['as_short'] + '\n'
        # добавить ключ в словарь participants_nat
        participants_nat[tournaments[ass]['as_short']] = []
        # список сезонов нац лиги с квотой > 0 в учитываемых турнирах
        league_seasons = [tournaments[ass]['tournaments'][tourn]['season'] for tourn in tournaments[ass]['tournaments'] \
            if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['quota'] > 0]
        league_name = [tournaments[ass]['tournaments'][tourn]['name'] for tourn in tournaments[ass]['tournaments'] \
            if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == max(league_seasons)][0]
        # если есть prev season
        if len(league_seasons) == 2:
            # вписать список квоты nat_league prev season с позициями перед клубами
            prev_parts = [tournaments[ass]['tournaments'][tourn]['participants'] for tourn in tournaments[ass]['tournaments'] \
                if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == min(league_seasons)][0]
            participants_str += "      {0} {1:20}".format(min(league_seasons), league_name) + '\n'
            rank = 1
            for club in prev_parts:
                # uefa quota
                uefa_quota = ''
                for tourn in tournaments['UEFA']['tournaments']:
                    if club['id'] in [participant['id'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants']]:
                        tourn_season = 'c' if tournaments['UEFA']['tournaments'][tourn]['season'] == curr_season else 'p'
                        uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle'] +' '+ tourn_season +' '+ \
                        str([participant['pos'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
                # TL quota
                TL_quota = ''
                if club['id'] in [participant['id'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants']]:
                    TL_quota = tournaments['TopLiga']['as_short'] +' '+ \
                    str([participant['pos'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants'] if participant['id']==club['id']][0])
                # nat cup quota
                nat_cup_quota = ''
                for tourn in tournaments[ass]['tournaments']:
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club['id'] in \
                    [participant['id'] for participant in tournaments[ass]['tournaments'][tourn]['participants']]:
                        tourn_season = 'c' if tournaments[ass]['tournaments'][tourn]['season'] == curr_season else 'p'
                        nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:] +' '+ tourn_season +' '+ \
                        str([participant['pos'] for participant in tournaments[ass]['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
                participants_str += ' '*27 + "{4}  {0:25}  {1:8}  {2:8}  {3:8}"\
                    .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
                rank += 1
                club_account.append(club['id'])
                # добавить участника в participants_nat
                participants_nat[tournaments[ass]['as_short']].append({'club': club['club'], 'id': club['id']})
        # вписать список квоты nat_league curr season с позициями перед клубами
        curr_parts = [tournaments[ass]['tournaments'][tourn]['participants'] for tourn in tournaments[ass]['tournaments'] \
            if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == max(league_seasons)][0]
        participants_str += "      {0} {1:20}".format(max(league_seasons), league_name) + '\n'
        # if len(curr_parts) > 0:
        #     with open((os.path.abspath(__file__))[:-23]+'/cache/answers/standings/'+ass+' League '+max(league_seasons)+' stan.json', 'r', encoding='utf-8') as j:
        #         curr_stands = json.load(j)
        for club in curr_parts:
            # rank
            rank = club['pos']
            # uefa quota
            uefa_quota = ''
            for tourn in tournaments['UEFA']['tournaments']:
                if club['id'] in [participant['id'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants']]:
                    tourn_season = 'c' if tournaments['UEFA']['tournaments'][tourn]['season'] == curr_season else 'p'
                    uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle'] +' '+ tourn_season +' '+ \
                    str([participant['pos'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
            # TL quota
            TL_quota = ''
            if club['id'] in [participant['id'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants']]:
                TL_quota = tournaments['TopLiga']['as_short'] +' '+ \
                str([participant['pos'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants'] if participant['id']==club['id']][0])
            # nat cup quota
            nat_cup_quota = ''
            for tourn in tournaments[ass]['tournaments']:
                if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club['id'] in \
                [participant['id'] for participant in tournaments[ass]['tournaments'][tourn]['participants']]:
                    tourn_season = 'c' if tournaments[ass]['tournaments'][tourn]['season'] == curr_season else 'p'
                    nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:] +' '+ tourn_season +' '+ \
                    str([participant['pos'] for participant in tournaments[ass]['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
            participants_str += ' '*27 + "{4}  {0:25}  {1:8}  {2:8}  {3:8}"\
                .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
            club_account.append(club['id'])
            # добавить участника в participants_nat
            participants_nat[tournaments[ass]['as_short']].append({'club': club['club'], 'id': club['id']})
       
        # список невошедших в квоту nat_league без позиций но в порядке nat_league curr season
        ass_parts_not_nat = []
        for club in parts_not_nat:
            if club['nat'] == ass:
                ass_parts_not_nat.append(club)
        ass_parts_not_nat.sort(key=lambda club: club['cur_nat_pos'])
        for club in ass_parts_not_nat:
            if club['id'] not in club_account:
                # поставить справа от клуба short_name турниров, в квоту которых он попал
                # uefa quota
                uefa_quota = ''
                for tourn in tournaments['UEFA']['tournaments']:
                    if club['id'] in [participant['id'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants']]:
                        tourn_season = 'c' if tournaments['UEFA']['tournaments'][tourn]['season'] == curr_season else 'p'
                        uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle'] +' '+ tourn_season +' '+ \
                        str([participant['pos'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
                # TL quota
                TL_quota = ''
                if club['id'] in [participant['id'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants']]:
                    TL_quota = tournaments['TopLiga']['as_short'] +' '+ \
                    str([participant['pos'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants'] if participant['id']==club['id']][0])
                # nat cup quota
                nat_cup_quota = ''
                for tourn in tournaments[ass]['tournaments']:
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and \
                    club['id'] in [participant['id'] for participant in tournaments[ass]['tournaments'][tourn]['participants']]:
                        tourn_season = 'c' if tournaments[ass]['tournaments'][tourn]['season'] == curr_season else 'p'
                        nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:] +' '+ tourn_season +' '+ \
                        str([participant['pos'] for participant in tournaments[ass]['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
                participants_str += ' '*30 + "{0:25}  {1:8}  {2:8}  {3:8}"\
                   .format(club['club'], TL_quota, uefa_quota, nat_cup_quota) + '\n'
                club_account.append(club['id'])
                # добавить участника в participants_nat
                participants_nat[tournaments[ass]['as_short']].append({'club': club['club'], 'id': club['id']})

# клубы из ассоциаций без квоты
# по порядку из UCL, UEL, UECL
other = list(set(participants_id) - set(club_account))
if len(other) != 0:
    other_ass = []
    for ass in tournaments:
        for tourn in tournaments[ass]['tournaments']:
            for club in tournaments[ass]['tournaments'][tourn]['participants']:
                for club_id in other:
                    if club['id'] == club_id and ass in ['UEFA', 'TopLiga'] and club['nat'] not in other_ass:
                        other_ass.append(club['nat'])
    for oth_ass in other_ass:
        participants_str += oth_ass + '\n'
        # добавить ключ в словарь participants_nat
        participants_nat[oth_ass] = []
        for ass in tournaments:
            for tournament in tournaments[ass]['tournaments']:
                for club in tournaments[ass]['tournaments'][tournament]['participants']:
                    if ass in ['UEFA', 'TopLiga'] and club['nat'] == oth_ass:
                        # поставить справа от клуба short_name турниров, в квоту которых он попал
                        # uefa quota
                        uefa_quota = ''
                        for tourn in tournaments['UEFA']['tournaments']:
                            if club['id'] in [participant['id'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants']]:
                                tourn_season = 'c' if tournaments['UEFA']['tournaments'][tourn]['season'] == curr_season else 'p'
                                uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle'] +' '+ tourn_season +' '+ \
                                str([participant['pos'] for participant in tournaments['UEFA']['tournaments'][tourn]['participants'] if participant['id']==club['id']][0])
                        # TL quota
                        TL_quota = ''
                        if club['id'] in [participant['id'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants']]:
                            TL_quota = tournaments['TopLiga']['as_short'] +' '+ \
                            str([participant['pos'] for participant in tournaments['TopLiga']['tournaments']['TopLiga']['participants'] if participant['id']==club['id']][0])
                        participants_str += ' '*30 + "{0:25}  {1:8}  {2:8}"\
                           .format(club['club'], TL_quota, uefa_quota) + '\n'
                        club_account.append(club['id'])
                        # добавить участника в participants_nat
                        participants_nat[oth_ass].append({'club': club['club'], 'id': club['id']})
                        other = list(set(participants_id) - set(club_account))
                        if len(other) == 0:     break
                if len(other) == 0:     break
            if len(other) == 0:     break
        if len(other) == 0:     break


# формирование result/4_participants.txt
with open((os.path.abspath(__file__))[:-28]+'/result/4_participants.txt', 'w', encoding='utf-8') as f:
    f.write(participants_str)

# формирование result/history/participants.txt
CreateDate = str(datetime.datetime.utcnow())[:19].replace(":", "-").replace(' ','_')
with open((os.path.abspath(__file__))[:-28]+'/result/history/participants '+CreateDate[:-9]+'.txt', 'w', encoding='utf-8') as f:
    f.write(participants_str)

# формирование .json из словаря participants_nat
with open((os.path.abspath(__file__))[:-28]+'/cache/participants_nat.json', 'w', encoding='utf-8') as j:
    json.dump(participants_nat, j, skipkeys=True, ensure_ascii=False, indent=2)
