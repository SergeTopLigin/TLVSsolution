# UEFA tournaments rating & quota
# определение UEFA tournaments club set
# жеребьевка группового этапа еврокубков проходит в конце августа
# жеребьевка 1 стадии плей-офф еврокубков проходит на следующей неделе после 6-го тура групп.
    # 1/16 проходит в феврале/марте
    # победители групп UEL и UECL (до сезона 24/25) или 1-8 места общего этапа (с сезона 24/25) начинают с 1/8, 
    # жеребьевка которой проходит после 1/16
# в папке club set/ сформировать соответсвующие файлы
# во время групповой стадии с 01.09 требуются текущий group set и playoff set прошлого сезона; 
# после завершения групповой стадии по 31.08 требуется последний playoff set

Ass_TournRateQuot = {}     # общий словарь рейтингов и квот всех турниров {Association:[Tournament,Rating,Quota]}

# UEFA tournaments club set
# определение имени и наличия необходимого файла, необходимости api-запроса
UEFA_tourn_club_set = []   # список tournament club set
UEFA_tourn_club_set_ID = {}    # словарь ID клубов из club sets {club_set:[id]}
UEFA_leagues = ("UCL", "UEL", "UECL")
import datetime, sys
DateNow = datetime.datetime.utcnow()    # текущая дата по UTC
# определение имен файлов tournament club set, действующих на текущую дату
if DateNow < datetime.datetime(2024, 9, 1):    # до сезона 24/25
    for league in UEFA_leagues:
        if (DateNow.month > 8 and DateNow.month < 12) or (DateNow.month == 12 and DateNow.day < 16):
            UEFA_tourn_club_set.append([league, str(DateNow.year-1)+"-"+str(DateNow.year), "playoff set"])
            UEFA_tourn_club_set.append([league, str(DateNow.year)+"-"+str(DateNow.year+1), "group set"])
        elif DateNow.month < 9:
            UEFA_tourn_club_set.append([league, str(DateNow.year-1)+"-"+str(DateNow.year), "playoff set"])
        elif DateNow.month == 12 and DateNow.day > 15:
            UEFA_tourn_club_set.append([league, str(DateNow.year)+"-"+str(DateNow.year+1), "playoff set"])
elif DateNow > datetime.datetime(2024, 8, 31):    # с сезона 24/25
    for league in UEFA_leagues:
        if DateNow.month > 8:
            UEFA_tourn_club_set.append([league, str(DateNow.year-1)+"-"+str(DateNow.year), "playoff set"])
            UEFA_tourn_club_set.append([league, str(DateNow.year)+"-"+str(DateNow.year+1), "group set"])
        elif DateNow.month == 1:
            UEFA_tourn_club_set.append([league, str(DateNow.year-1)+"-"+str(DateNow.year), "group set"])
        else:
            UEFA_tourn_club_set.append([league, str(DateNow.year-1)+"-"+str(DateNow.year), "playoff set"])
# UEFA_tourn_club_set = [league("UCL", "UEL", "UECL"), season YYYY-YYYY, set('group', 'playoff')]
# определение наличия необходимого файла или необходимости api-запроса
import os
cancel_prog = 0
i = 0
while i < len(UEFA_tourn_club_set):
    create_flag = 1    # флаг необходимости создания файла
    for Set_file in os.listdir((os.path.abspath(__file__))[:-27]+'/cache/club_sets'):
    # прочитать названия файлов из каталога club_set
        if Set_file.find(str(UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2]))!=-1:  
            create_flag = 0
    if create_flag == 1:
        # если в каталоге club_set нет необходимого файла
        print('создать файл club set '+str(UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2]))
        cancel_prog = 1
    i += 1
if cancel_prog == 1:
    sys.exit()

i = 0
while i < len(UEFA_tourn_club_set):
    # заполнение словаря ID клубов из club sets
    LegueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
    with open((os.path.abspath(__file__))[:-27]+'/cache/club_sets/'\
        +UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2]+".txt", 'r') as f:
        for line in f:  # цикл по строкам
            kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
            end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
            LegueClubSetID.append(int(line[kursor:end_substr]))
    UEFA_tourn_club_set_ID[str(UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2])] =\
    LegueClubSetID
    i += 1
    # LegueClubSetID = {club_set:[id]}

# UEFA Tournament rating = total club set SUM(pts+1.2>=0) in TL standigs / Number of clubs in the set
# определение UEFA tournaments rating
# определение наличия временного фактора при постепенном перетекании рейтинга из плейофф прошлого турнира 
    # в групповой этап текущего
time_factor = 0     # инициализация временного фактора
# и формирование списка UEFA_club_sets
UEFA_club_sets = []
for club_set in UEFA_tourn_club_set_ID:     # поиск слова group в названии ключа словаря
    if club_set.find("group") != -1:
        # при наличии слова group - задействовать временной фактор
        first_year = club_set[club_set.find(" ")+1:club_set.find(" ")+5]    # определение года начала турнира group set
        # кол-во дней прошедших с 01.09, деленное на 100 = % использования group set
        time_factor = min((DateNow - datetime.datetime(int(first_year), 8, 31)) / (datetime.timedelta(days=1) * 100), 1)  
    UEFA_club_sets.append(club_set)     # заполненине списка названием club set
Ass_TournRateQuot["UEFA"] = UEFA_club_sets  # начальное заполнение значений ключа UEFA списком длиной, 
# равной количеству турниров UEFA
# импорт final_standings.json
import json
with open((os.path.abspath(__file__))[:-27]+'/cache/final_standings.json', 'r', encoding='utf-8') as j:
    standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
i = 0   # счетчик итераций для индексов списка турниров UEFA в словаре Ass_TournRateQuot
for club_set in UEFA_tourn_club_set_ID:     # для каждого ключа словаря (рассматриваемого турнира)
    tourn_rating = 0    # рейтинг рассмтриваемого турнира
    for SetID in UEFA_tourn_club_set_ID[club_set]:     # для каждого элемента списка ключа словаря 
                                                       # (id клуба из club set рассматриваемого турнира)
        for club in standings:   # для каждого id клуба из TL standings
            if standings[club]['IDapi'] == SetID and standings[club]['buffer'] == False:
                tourn_rating += max(standings[club]['TL_rank'] + 1.2, 0)
                break
    # определение рейтинга турнира с увеличением вложенности словаря до {Association:[Tournament,Rating]}
    Ass_TournRateQuot["UEFA"][i] = [club_set, tourn_rating / len(UEFA_tourn_club_set_ID[club_set])]
    # если задействован временной фактор: уменьшать рейтинг playoff set с 100% до 0% и увеличивать рейтинг group set с 0% до 100% каждый день на 1% с 01.09
    if time_factor != 0:
        if club_set.find("group") != -1:
            Ass_TournRateQuot["UEFA"][i][1] *= time_factor
        elif club_set.find("playoff") != -1:
            Ass_TournRateQuot["UEFA"][i][1] *= 1 - time_factor
    Ass_TournRateQuot["UEFA"][i][1] = round(Ass_TournRateQuot["UEFA"][i][1], 2)
    i += 1

# UEFA tournament quota распределяется пропорционально рейтингам турниров
# словарь рейтингов и квот каждого турнира {tourn:[rate,quota]}  
# (во время групповой стадии: сумма рейтингов playoff set и group set)
whole_tourn_rate_quota = {"UCL": [0, 0], "UEL": [0, 0], "UECL": [0, 0]}     
# определить рейтинг каждого турнира 
for tourn in Ass_TournRateQuot["UEFA"]:
    for league in whole_tourn_rate_quota:
        if tourn[0].find(league) != -1:
            whole_tourn_rate_quota[league][0] += tourn[1]
# определить квоту каждого турнира
# импорт final_standings.json
import json
with open((os.path.abspath(__file__))[:-27]+'/cache/associations.json', 'r', encoding='utf-8') as j:
    associations = json.load(j) # {ass: {rating: , quota: }} 
sum_ratings = 0   # определение суммы рейтингов турниров
for league in whole_tourn_rate_quota:
    sum_ratings += whole_tourn_rate_quota[league][0]
for league in whole_tourn_rate_quota:
    whole_tourn_rate_quota[league][1] = associations["UEFA"]['quota'] * whole_tourn_rate_quota[league][0] / sum_ratings
# сумма квот турниров УЕФА, округленных до целого в меньшую сторону
import math
UEFA_tourn_quota_int_sum = 0   
for league in whole_tourn_rate_quota:
    UEFA_tourn_quota_int_sum += math.floor(whole_tourn_rate_quota[league][1])
# общая квота УЕФА, отброшенная в качестве дробных частей
fractional_quota = associations["UEFA"]['quota'] - UEFA_tourn_quota_int_sum
# распределение суммы дробных частей квот между турнирами в качестве целых квот в порядке уменьшения их дробной части
if fractional_quota == 1:   # если сумма дробных частей квот равна 1
    fractional_part = 0   # дробная часть квоты турнира (инициализация)
    for league in whole_tourn_rate_quota:   # определение макс дробной части среди квот турниров
        if whole_tourn_rate_quota[league][1] % 1 > fractional_part:
            fractional_part = whole_tourn_rate_quota[league][1] % 1
            add_tourn = league
    whole_tourn_rate_quota[add_tourn][1] += 1   # присвоение целой квоты турниру с макс дробной частью
if fractional_quota == 2:   # если сумма дробных частей квот равна 2
    fractional_part = 1   # дробная часть квоты турнира (инициализация)
    for league in whole_tourn_rate_quota:   # определение мин дробной части среди квот турниров
        if whole_tourn_rate_quota[league][1] % 1 < fractional_part:
            fractional_part = whole_tourn_rate_quota[league][1] % 1
            not_add_tourn = league
    for league in whole_tourn_rate_quota:   # присвоение целой квоты двум турнирам с макс дробной частью
        if league != not_add_tourn:
            whole_tourn_rate_quota[league][1] += 1
# округление до целого квоты каждого турнира
for league in whole_tourn_rate_quota:
    whole_tourn_rate_quota[league][1] = math.floor(whole_tourn_rate_quota[league][1])
# во время групповой стадии квота распределяется между playoff set и group set пропорционально их рейтингам 
# с округлением до целого в сторону playoff set
for tourn in Ass_TournRateQuot["UEFA"]:
    for league in whole_tourn_rate_quota:
        if tourn[0].find(league) != -1:
            if tourn[0].find("group") != -1:
                tourn.append(math.floor(round(whole_tourn_rate_quota[league][1] * tourn[1] / whole_tourn_rate_quota[league][0], 3)))
            if tourn[0].find("playoff") != -1:
                tourn.append(math.ceil(round(whole_tourn_rate_quota[league][1] * tourn[1] / whole_tourn_rate_quota[league][0], 3)))

# расширить Ass_TournRateQuot до {Association:[Tournament,Season,Rating,Quota,TournID,TournType]} 
# изменением первых двух элементов и
# добавлением ID турнира и его типа (лига, кубок)
for tourn in Ass_TournRateQuot["UEFA"]:
     if tourn[0].find("UCL") != -1:
        tourn.insert(1, tourn[0][6:8]+"-"+tourn[0][11:13])
        tourn[0] = tourn[0][:3]
        tourn.append(2)
        tourn.append("Cup")
     if tourn[0].find("UEL") != -1:
        tourn.insert(1, tourn[0][6:8]+"-"+tourn[0][11:13])
        tourn[0] = tourn[0][:3]
        tourn.append(3)
        tourn.append("Cup")
     if tourn[0].find("UECL") != -1:
        tourn.insert(1, tourn[0][7:9]+"-"+tourn[0][12:14])
        tourn[0] = tourn[0][:4]
        tourn.append(848)
        tourn.append("Cup")

# учет квоты TL на 10 лидеров
Ass_TournRateQuot["TopLiga"] = [["TopLiga", None, 10, associations['TopLiga']['quota'], None, None]]



# National tournaments rating & quota

from modules.nat_tournaments import Nat_Tournaments
from modules.country_codes import country_codes

# добавить в Ass_TournRateQuot ассоциации с квотой > 0 в качестве ключей
# включить в Ass_TournRateQuot турниры нац ассоциаций
Ass_TournIdType = Nat_Tournaments()
for ass_n in associations:
    if ass_n not in Ass_TournRateQuot.keys() and associations[ass_n]['quota'] > 0:
        for Ass in Ass_TournIdType:
            if ass_n == Ass:
                Ass_TournRateQuot[ass_n] = Ass_TournIdType[Ass]
for ass_n in Ass_TournRateQuot:
    Del_tourn = []  # список турниров на удаление
    for tourn in Ass_TournRateQuot[ass_n]:
        if tourn[0].find("League") != -1 or tourn[0].find("Cup") != -1: # из нац турниров
            if tourn[2] == "None" or tourn[0].find("SCup") != -1:   # удалить несуществующие и суперкубки
                Del_tourn.append(tourn)
    for tourn in Del_tourn:
        Ass_TournRateQuot[ass_n].remove(tourn)    

    # приведение всех списков нац турниров Ass_TournRateQuot к виду [Tournament,Season,Rating,Quota,TournID,TournType]
with open((os.path.abspath(__file__))[:-27]+'/workflow/07_nat_tournaments.json', 'r', encoding='utf-8') as j:
    nat_cups = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
for ass_n in Ass_TournRateQuot:
    Del_tourn = []  # список турниров на удаление
    for tourn in Ass_TournRateQuot[ass_n]:
        if tourn[0].find("League") != -1:   # для League: если рассматриваемая дата с августа по декабрь - оставить оба турнира, иначе только curr
            tourn[2] = 0        # изменение элемента на Rating
            tourn.insert(3, 0)  # добавление элемента Quota
            if DateNow.month < 8 and tourn[1] == "prev":
                Del_tourn.append(tourn)
            if DateNow.month < 8 and tourn[1] == "curr":
                tourn[1] = str(DateNow.year-1)[2:]+"-"+str(DateNow.year)[2:]
            if DateNow.month > 7 and tourn[1] == "prev":
                tourn[1] = str(DateNow.year-1)[2:]+"-"+str(DateNow.year)[2:]
            if DateNow.month > 7 and tourn[1] == "curr":
                tourn[1] = str(DateNow.year)[2:]+"-"+str(DateNow.year+1)[2:]
        if tourn[0].find("Cup") != -1:  # для всех кубковых турниров учитываются: незавершившийся турнир и предыдущий, если с его финала прошло <150 дней
            tourn[2] = 0        # изменение элемента на Rating
            tourn.insert(3, 0)  # добавление элемента Quota
            cup_found = 0
            for cup in nat_cups:
                if tourn[0] == cup['name'] and tourn[1] == cup['status']:
                    tourn[1] = cup['season']
                    cup_found = 1
            if cup_found == 0:
                Del_tourn.append(tourn) # удалить кубок из списка учитываемых турниров
    for tourn in Del_tourn:     # удаление турниров prev после потери их актуальности
        Ass_TournRateQuot[ass_n].remove(tourn)    


# Tournaments rating
import json
with open((os.path.abspath(__file__))[:-27]+'/workflow/07_nat_tournaments.json', 'r', encoding='utf-8') as j:
    nat_tourns = json.load(j)
for ass_n in Ass_TournRateQuot:
    for tourn in Ass_TournRateQuot[ass_n]:
        
        # рейтинг National League
        if tourn[0].find("League") != -1:
        # League rating = total League clubs SUM(pts+1.2>=0) in TL standigs / Number of clubs in the League
        # prev > curr (1/150 per day from 01.08)
            for nat_tourn in nat_tourns:
                if nat_tourn['name'] == tourn[0] and nat_tourn['season'] == tourn[1]:
                    for team in nat_tourn['teams']:
                        for club in standings:   # для каждого id клуба из TL standings
                            if standings[club]['IDapi'] == team[1] and standings[club]['buffer'] == False:
                                tourn[2] += max(standings[club]['TL_rank'] + 1.2, 0)
                    tourn[2] /= len(nat_tourn['teams'])
                    # временной фактор: prev > curr (1/150 per day from 01.08)
                    if DateNow.month > 7 and tourn[1][3:] == str(DateNow.year)[2:]:     # для прошлого сезона
                        tourn[2] *= max((150 - (DateNow - datetime.datetime(DateNow.year, 7, 31)) / datetime.timedelta(days=1)) / 150, 0)
                    if DateNow.month > 7 and tourn[1][:2] == str(DateNow.year)[2:]:     # для текущего сезона
                        tourn[2] *= min(((DateNow - datetime.datetime(DateNow.year, 7, 31)) / datetime.timedelta(days=1)) / 150, 1)
                    tourn[2] = round(tourn[2], 2)
            
        # рейтинг National Cup(LCup)
        if tourn[0].find("Cup") != -1:
        # рейтинг кубка на протяжении его розыгрыша равен максимальному из своих значений на текущей или предыдущих стадиях (для prev - только на предыдущих)
            # для текущей стадии: рейтинг рассчитывается по текущему TL standings
            # для предыдущей стадии: рейтинг рассчитывается по TL standings, актуальному на момент окончания последнего матча стадии
        # Cup rating = max (total Cup stage clubs SUM(pts+1.2>=0) in TL standigs / Number of clubs in the Cup stage) / 5
        # prev > curr (1/150 per day from prev final)
            # определение рейтингов стадий
            for nat_tourn in nat_tourns:
                if nat_tourn['name'] == tourn[0] and nat_tourn['season'] == tourn[1]:
                    for stage in nat_tourn['rounds']:
                        if stage['status'] == 'curr':
                            stage_standings = standings
                        elif stage['status'] == 'prev':
                            round_last_date = stage['last_date'][:10]
                            use_standings_date = '2100-01-01'    # установить дату первого standings в /standings_history
                            for standings_file in os.listdir((os.path.abspath(__file__))[:-27]+'/cache/standings_history'):
                                standings_date = standings_file[10:20]
                                if 'standings' in standings_file and standings_date < use_standings_date:
                                    use_standings_date = standings_date
                            for standings_file in os.listdir((os.path.abspath(__file__))[:-27]+'/cache/standings_history'):
                                standings_date = standings_file[10:20]
                                if 'standings' in standings_file and standings_date < round_last_date and standings_date > use_standings_date:
                                    use_standings_date = standings_date
                            with open((os.path.abspath(__file__))[:-27]+'/cache/standings_history/standings '\
                                +str(use_standings_date)+'.json', 'r', encoding='utf-8') as j:
                                stage_standings = json.load(j)
                        stage_rating = 0
                        for cup_club in stage['teams_TL']:
                            for stan_club in stage_standings:
                                if cup_club[1] == stage_standings[stan_club]['IDapi'] and stage_standings[stan_club]['buffer'] == False:
                                    stage_rating += max(stage_standings[stan_club]['TL_rank'] + 1.2, 0)
                                    break
                        stage_rating /= stage['total_teams']
                        if stage_rating > tourn[2]:
                            tourn[2] = stage_rating
                    # приведение рейтинга кубка к сложности лиги (/5)
                    tourn[2] /= 5
                    # учет временного фактора  prev > curr (1/150 per day from prev final)
                    if nat_tourn['status'] == 'prev':
                        final_date = datetime.datetime(int(nat_tourn['dates']['final'][:4]), int(nat_tourn['dates']['final'][5:7]), int(nat_tourn['dates']['final'][8:10]))
                        tourn[2] *= max((150 - (DateNow - final_date) / datetime.timedelta(days=1)) / 150, 0)
                    if nat_tourn['status'] == 'curr':
                        for prev_cup in nat_tourns:
                            if prev_cup['name'] == tourn[0] and prev_cup['status'] == 'prev':
                                final_date = datetime.datetime(int(nat_tourn['dates']['final'][:4]), int(nat_tourn['dates']['final'][5:7]), int(nat_tourn['dates']['final'][8:10]))
                                tourn[2] *= min(((DateNow - final_date) / datetime.timedelta(days=1)) / 150, 1)
                    tourn[2] = round(tourn[2], 2)

                    break


# Tournaments quota
for ass_n in Ass_TournRateQuot:
    if ass_n not in ['UEFA', 'TopLiga']:
        # квота ассоциации
        ass_quota = associations[ass_n]['quota']
        # сумма рейтингов турниров ассоциации        
        sum_ratings = 0
        for tourn in Ass_TournRateQuot[ass_n]:
            sum_ratings += tourn[2]
        # квота распределяется прямо пропорционально рейтингам турниров
        for tourn in Ass_TournRateQuot[ass_n]:
            tourn[3] = round(ass_quota * tourn[2] / sum_ratings, 10)
        # округление квот кубков до целого в меньшую сторону, сохранение суммы отброшенных дробных частей квот кубков в переменную
        cup_fract = 0   # сумма дробных частей квот кубков
        league_sum = 0   # сумма рейтингов учитываемых сезонов лиги
        for tourn in Ass_TournRateQuot[ass_n]:
            if 'Cup' in tourn[0]:
                cup_fract += round(tourn[3] % 1, 10)
                tourn[3] = tourn[3] // 1
            if 'League' in tourn[0]:
                league_sum += tourn[2]
        # распределеие суммы дробных частей квот кубков между сезонами лиги прямо пропорционально их рейтингам
        for tourn in Ass_TournRateQuot[ass_n]:
            if 'League' in tourn[0]:
                tourn[3] += round(cup_fract * tourn[2] / league_sum, 10)
        # опредление текущего и предыдущего сезонов лиги
        seasons = []    # инициализация списка сезонов лиги
        for tourn in Ass_TournRateQuot[ass_n]:
            if 'League' in tourn[0]:
                seasons.append(int(tourn[1][:2]))
        # распределение квоты лиги между текущим и предыдущим сезоном: округляется до целого в сторону предыдущего сезона
        for tourn in Ass_TournRateQuot[ass_n]:
            if 'League' in tourn[0]:
                if len(seasons) > 1 and int(tourn[1][:2]) == min(seasons):  # для предыдущего сезона лиги
                    tourn[3] = math.ceil(tourn[3])
                if len(seasons) > 1 and int(tourn[1][:2]) == max(seasons):  # для текущего сезона лиги
                    tourn[3] = math.floor(tourn[3])
            tourn[3] = int(round(tourn[3], 0))    # квота - целое число



# формирование словаря для выгрузки
country_codes = country_codes()
Nat_Tournaments = Nat_Tournaments()
# {as_short:{'as_short': , 'as_full': , 'tournaments': {tytle_season:{'tytle': , 'season': , 'rating': , 'quota': , 'id': , 'type': , 'name': }}}}
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
        # if tourn[2] > 0:
        # tourn name
        if tourn[0] == 'UCL':       name = 'Champions League'
        elif tourn[0] == 'UEL':     name = 'Europa League'
        elif tourn[0] == 'UECL':    name = 'Conference League'
        elif tourn[0] == 'TopLiga': name = 'TopLiga'
        else:       name = [Nat_Tournaments[ass_n][Nat_Tournaments[ass_n].index(elem)][2] \
                            for elem in Nat_Tournaments[ass_n] if tourn[0] in elem[0]][0]
        if ass_n != 'TopLiga':
            tourns[tourn[0]+' '+tourn[1]] = {'tytle': tourn[0], 'season': tourn[1], 'rating': tourn[2], 'quota': tourn[3], 'id': tourn[4], \
            'type': tourn[5], 'name': name}
        else:
            tourns[tourn[0]] = {'tytle': tourn[0], 'season': tourn[1], 'rating': tourn[2], 'quota': tourn[3], 'id': tourn[4], \
            'type': tourn[5], 'name': name}
    tournaments[ass_n] = {'as_short': short, 'as_full': full, 'tournaments': tourns}


# формирование .json из словаря tournaments
with open((os.path.abspath(__file__))[:-27]+'/cache/tournaments.json', 'w', encoding='utf-8') as j:
    json.dump(tournaments, j, skipkeys=True, ensure_ascii=False, indent=2)

# формирование строки из словаря в читабельном виде
# github принимает только str для записи в файл
tournaments_str = "{0:>36}".format('quota') + '\n'  # шапка таблицы
for ass in tournaments:
    tournaments_str += tournaments[ass]['as_short'] + '\n'
    for tourn in tournaments[ass]['tournaments']:
        if tournaments[ass]['tournaments'][tourn]['quota'] > 0:
            if tourn != 'TopLiga':
                tournaments_str += "      {0} {1:20}  {2:>2}"\
                .format(tournaments[ass]['tournaments'][tourn]['season'], tournaments[ass]['tournaments'][tourn]['name'], tournaments[ass]['tournaments'][tourn]['quota']) + '\n'
            elif tourn == 'TopLiga':
                tournaments_str += "      {0:26}  {1:>2}"\
                .format(tournaments[ass]['tournaments'][tourn]['name'], tournaments[ass]['tournaments'][tourn]['quota']) + '\n'
tournaments_str = tournaments_str[:-1]

# формирование result/3_tournaments.txt
with open((os.path.abspath(__file__))[:-27]+'/result/3_tournaments.txt', 'w', encoding='utf-8') as f:
    f.write(tournaments_str)

# формирование result/history/tournaments.txt
CreateDate = str(datetime.datetime.utcnow())[:19].replace(":", "-").replace(' ','_')
with open((os.path.abspath(__file__))[:-27]+'/result/history/tournaments '+CreateDate[:-9]+'.txt', 'w', encoding='utf-8') as f:
    f.write(tournaments_str)
