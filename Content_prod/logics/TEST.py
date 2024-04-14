import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
    tournaments = json.load(j)

from modules.country_codes import country_codes
country_codes = country_codes()

participants_str = ""
# набрать список всех клубов участников
participants_id = []
for ass in tournaments:
    for tourn in tournaments[ass]['tournaments']:
        for club in tournaments[ass]['tournaments'][tourn]['participants']:
            participants_id.append(club['id'])
club_account = []  # список учтеных клубов
dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/associations.json', 'r', encoding='utf-8') as j:
    associations = json.load(j)
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/nat_league_groups.json', 'r', encoding='utf-8') as j:
    groups_dict = json.load(j)
for ass in tournaments:
    # представление participants по нац ассоциациям в порядке рейтинга ассоциаций
    if ass in [country['fifa'] for country in country_codes if ass == country['fifa']]:
        # вписать строку нац ассоциации
        participants_str += tournaments[ass]['as_short'] + '\n'
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
                    if club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                        uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                # TL quota
                TL_quota = ''
                if club in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                    TL_quota = tournaments['TopLiga']['as_short']
                # nat cup quota
                nat_cup_quota = ''
                for tourn in tournaments[ass]['tournaments']:
                    if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club in tournaments[ass]['tournaments'][tourn]['participants']:
                        nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
                participants_str += ' '*27 + "{4}  {0:25}  {1:4}  {2:4}  {3:4}"\
                    .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
                rank += 1
                club_account.append(club['id'])
        # вписать список квоты nat_league curr season с позициями перед клубами
        curr_parts = [tournaments[ass]['tournaments'][tourn]['participants'] for tourn in tournaments[ass]['tournaments'] \
            if tournaments[ass]['tournaments'][tourn]['type'] == 'League' and tournaments[ass]['tournaments'][tourn]['season'] == max(league_seasons)][0]
        participants_str += "      {0} {1:20}".format(max(league_seasons), league_name) + '\n'
        rank = 1
        for club in curr_parts:
            # uefa quota
            uefa_quota = ''
            for tourn in tournaments['UEFA']['tournaments']:
                if club in tournaments['UEFA']['tournaments'][tourn]['participants']:
                    uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
            # TL quota
            TL_quota = ''
            if club in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                TL_quota = tournaments['TopLiga']['as_short']
            # nat cup quota
            nat_cup_quota = ''
            for tourn in tournaments[ass]['tournaments']:
                if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and club in tournaments[ass]['tournaments'][tourn]['participants']:
                    nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
            participants_str += ' '*27 + "{4}  {0:25}  {1:4}  {2:4}  {3:4}"\
                .format(club['club'], TL_quota, uefa_quota, nat_cup_quota, rank) + '\n'
            rank += 1
            club_account.append(club['id'])
        # список невошедших в квоту nat_league без позиций но в порядке nat_league curr season
        # по nat standings
        file_standings = ass+' League'
        for file in dir_standings:
            if ass in file and file > file_standings:
                file_standings = file
        with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file_standings, 'r', encoding='utf-8') as j:
            league_standings = json.load(j)
        for league in groups_dict:
            if file_standings[:16] in league:
                # список стадий лиги ["league"] с сортировкой по приоритету
                stage_prior = sorted(groups_dict[league], key=groups_dict[league].get, reverse=True)
        for stage in stage_prior:
            for group in league_standings['response'][0]['league']['standings']:
                for club in group:
                    if club['group'] == stage and club['team']['id'] in participants_id and club['team']['id'] not in club_account:
                        # поставить слева от клуба short_name турниров, в квоту которых он попал
                        # uefa quota
                        uefa_quota = ''
                        for tourn in tournaments['UEFA']['tournaments']:
                            if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['UEFA']['tournaments'][tourn]['participants']:
                                uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                        # TL quota
                        TL_quota = ''
                        if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                            TL_quota = tournaments['TopLiga']['as_short']
                        # nat cup quota
                        nat_cup_quota = ''
                        for tourn in tournaments[ass]['tournaments']:
                            if tournaments[ass]['tournaments'][tourn]['type'] == 'Cup' and \
                            {'club': club['team']['name'], 'id': club['team']['id']} in tournaments[ass]['tournaments'][tourn]['participants']:
                                nat_cup_quota = tournaments[ass]['tournaments'][tourn]['tytle'][4:]
                        participants_str += ' '*30 + "{0:25}  {1:4}  {2:4}  {3:4}"\
                           .format(club['team']['name'], TL_quota, uefa_quota, nat_cup_quota) + '\n'
                        club_account.append(club['team']['id'])

# клубы из ассоциаций без квоты
other = list(set(participants_id) - set(club_account))
for ass in associations:
    if ass not in tournaments:
        file_standings = ass+' League'
        for file in dir_standings:
            if ass in file and file > file_standings:
                file_standings = file
        with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file_standings, 'r', encoding='utf-8') as j:
            league_standings = json.load(j)
        ass_str = ''
        for group in league_standings['response'][0]['league']['standings']:
            for club in group:
                if club['team']['id'] in other:
                    # строка асоциаии
                    if ass_str == '':
                        participants_str += ass + '\n'
                        ass_str = ass
                    # поставить слева от клуба short_name турниров, в квоту которых он попал
                    # uefa quota
                    uefa_quota = ''
                    for tourn in tournaments['UEFA']['tournaments']:
                        if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['UEFA']['tournaments'][tourn]['participants']:
                            uefa_quota = tournaments['UEFA']['tournaments'][tourn]['tytle']
                    # TL quota
                    TL_quota = ''
                    if {'club': club['team']['name'], 'id': club['team']['id']} in tournaments['TopLiga']['tournaments']['TopLiga']['participants']:
                        TL_quota = tournaments['TopLiga']['as_short']
                    participants_str += ' '*30 + "{0:25}  {1:4}  {2:4}"\
                       .format(club['team']['name'], TL_quota, uefa_quota) + '\n'
                    club_account.append(club['team']['id'])
                    other = list(set(participants_id) - set(club_account))
                    if len(other) == 0:     break
            if len(other) == 0:     break
    if len(other) == 0:     break

print(participants_str)