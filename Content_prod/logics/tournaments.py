try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # UEFA tournaments rating & quota
    # определение UEFA tournaments club set
    # жеребьевка группового этапа еврокубков проходит в конце августа
    # для получения group set следует с 01.09 ежедневно делать запрос на игры в октябре, 
        # пока в папке club set/ не будет сформирован соответсвующий файл
    # жеребьевка 1 стадии плей-офф еврокубков проходит на следующей неделе после 6-го тура групп.
        # 1/16 проходит в феврале/марте
        # победители групп UEL и UECL (до сезона 24/25) или 1-8 места общего этапа (с сезона 24/25) начинают с 1/8, 
        # жеребьевка которой проходит после 1/16
    # для получения playoff set (до сезона 24/25) следует с 16.12 ежедневно делать запрос на игры в феврале и марте, 
        # пока в папке club set/ не будет сформирован соответсвующий файл
        # а также запрос standings на 1-е места групп для UEL и UECL, если запрос fixtures на февраль-март дал результат
    # для получения playoff set (с сезона 24/25) с 01.02 запрашивать standings на 1-24 места в общем групповом этапе во всех турнирах 
    # во время групповой стадии с 01.09 требуются текущий group set и playoff set прошлого сезона; 
    # после завершения групповой стадии по 31.08 требуется последний playoff set

    Ass_TournRateQuot = {}     # общий словарь рейтингов и квот всех турниров {Association:[Tournament,Rating,Quota]}

    # UEFA tournaments club set
    # определение имени и наличия необходимого файла, необходимости api-запроса
    UEFA_tourn_club_set = []   # список tournament club set
    UEFA_tourn_club_set_ID = {}    # словарь ID клубов из club sets {club_set:[id]}
    UEFA_leagues = ("UCL", "UEL", "UECL")
    import datetime
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
    # определение наличия необходимого файла или необходимости api-запроса
    import os
    from modules.UEFAtournaments_club_set import UEFAtournaments_club_set
    i = 0
    while i < len(UEFA_tourn_club_set):
        create_flag = 1    # флаг необходимости создания файла
        for Set_file in os.listdir((os.path.abspath(__file__))[:-22]+'/cache/sub_results/club_sets'):
        # прочитать названия файлов из каталога club_set
            if Set_file.find(str(UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2]))!=-1:  
                # если в каталоге club_set есть необходимый файл
                create_flag = 0    # опустить флаг создания файла
        if create_flag == 1:   # если флаг создания файла поднят - 
            # создать необходимый файл
            if UEFAtournaments_club_set(UEFA_tourn_club_set[i][0], UEFA_tourn_club_set[i][1], UEFA_tourn_club_set[i][2]) == \
            "use_prev":   
            # или использовать предыдущий club set при ошибках
                if DateNow < datetime.datetime(2024, 9, 1):    # до сезона 24/25
                    # если ошибка при запросе group set - использовать предыдущий playoff set, который уже есть в UEFA_tourn_club_set
                    if UEFA_tourn_club_set[i][2] == "group set":
                        # удалить UT_club_set из UEFA_tourn_club_set
                        del UEFA_tourn_club_set[i]
                        i -= 1   # смещение на итерацию назад, тк после удаления элемента номерация смещается
                    # если ошибка при запросе playoff set, выполненном 01.09-15.12
                    elif UEFA_tourn_club_set[i][2] == "playoff set" and ((DateNow.month > 8 and DateNow.month < 12) or \
                    (DateNow.month == 12 and DateNow.day < 16)):
                        # удалить UT_club_set из UEFA_tourn_club_set
                        del UEFA_tourn_club_set[i]
                        i -= 1
                    # если ошибка при запросе playoff set, выполненном после декабря
                    elif UEFA_tourn_club_set[i][2] == "playoff set" and DateNow.month < 9:
                        # изменить его на group set текущего розыгрыша
                        UEFA_tourn_club_set[i][1] = str(DateNow.year-1)+"-"+str(DateNow.year)
                        UEFA_tourn_club_set[i][2] = "group set"
                    # если ошибка при запросе playoff set, выполненном в декабре
                    elif UEFA_tourn_club_set[i][2] == "playoff set" and (DateNow.month == 12 and DateNow.day > 15):
                        # изменить его на group set текущего розыгрыша
                        UEFA_tourn_club_set[i][1] = str(DateNow.year)+"-"+str(DateNow.year+1)
                        UEFA_tourn_club_set[i][2] = "group set"
                elif DateNow > datetime.datetime(2024, 8, 31):    # с сезона 24/25
                    # если ошибка при запросе group set, выполненный до января - использовать предыдущий playoff set, который уже есть в UEFA_tourn_club_set
                    if UEFA_tourn_club_set[i][2] == "group set":
                        # удалить UT_club_set из UEFA_tourn_club_set
                        del UEFA_tourn_club_set[i]
                        i -= 1   # смещение на итерацию назад, тк после удаления элемента номерация смещается
                    # если ошибка при запросе playoff set, выполненном с сентября по декабрь
                    elif UEFA_tourn_club_set[i][2] == "playoff set" and DateNow.month > 8:
                        # удалить UT_club_set из UEFA_tourn_club_set
                        del UEFA_tourn_club_set[i]
                        i -= 1
                    # если ошибка при запросе group set, выполненном в январе
                    elif UEFA_tourn_club_set[i][2] == "group set" and DateNow.month == 1:
                        # изменить его на playoff set прошлого розыгрыша
                        UEFA_tourn_club_set[i][1] = str(DateNow.year-2)+"-"+str(DateNow.year-1)
                        UEFA_tourn_club_set[i][2] = "playoff set"
                    # если ошибка при запросе playoff set, выполненном с февраля по август
                    elif UEFA_tourn_club_set[i][2] == "playoff set" and (DateNow.month < 9 and DateNow.month > 1):
                        # изменить его на group set текущего розыгрыша
                        UEFA_tourn_club_set[i][1] = str(DateNow.year-1)+"-"+str(DateNow.year)
                        UEFA_tourn_club_set[i][2] = "group set"
        # заполнение словаря ID клубов из club sets
        LegueClubSetID = []    # создание списка id из файла UefaTournamentClubSet
        with open((os.path.abspath(__file__))[:-22]+'/cache/sub_results/club_sets/'\
            +UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2]+".txt", 'r') as f:
            for line in f:  # цикл по строкам
                kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
                end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                LegueClubSetID.append(int(line[kursor:end_substr]))
        UEFA_tourn_club_set_ID[str(UEFA_tourn_club_set[i][0]+" "+UEFA_tourn_club_set[i][1]+" "+UEFA_tourn_club_set[i][2])] =\
        LegueClubSetID
        i += 1

    # UEFA Tournament rating = total club set SUM(pts+1.2) in TL standigs / Number of clubs in the set
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
    with open((os.path.abspath(__file__))[:-22]+'/cache/sub_results/final_standings.json', 'r') as j:
        standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
    i = 0   # счетчик итераций для индексов списка турниров UEFA в словаре Ass_TournRateQuot
    for club_set in UEFA_tourn_club_set_ID:     # для каждого ключа словаря (рассматриваемого турнира)
        tourn_rating = 0    # рейтинг рассмтриваемого турнира
        for SetID in UEFA_tourn_club_set_ID[club_set]:     # для каждого элемента списка ключа словаря 
                                                           # (id клуба из club set рассматриваемого турнира)
            for club in standings:   # для каждого id клуба из TL standings
                if standings[club]['IDapi'] == SetID:
                    tourn_rating += standings[club]['TL_rank'] + 1.2
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
    with open((os.path.abspath(__file__))[:-22]+'/cache/sub_results/associations.json', 'r') as j:
        associations = json.load(j) # {ass: {rating: , quota: }} 
    for league in whole_tourn_rate_quota:
        whole_tourn_rate_quota[league][1] = associations["UEFA"]['quota'] * whole_tourn_rate_quota[league][0] / associations["UEFA"]['rating']
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
    Ass_TournRateQuot["TopLiga"] = [["TopLiga", "", associations['TopLiga']['rating'], associations['TopLiga']['quota'], "", ""]]



    # National tournaments rating & quota

    from modules.nat_tournaments import Nat_Tournaments
    from modules.cup_files import func_cup_files
    from modules.api_request import PrevCupInfluence, CupFirst
    from modules.cup_round_ratings import cup_round_ratings

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
                func_cup_files(tourn[0], DateNow)   # актуализация файлов кубков
                tourn[2] = 0        # изменение элемента на Rating
                tourn.insert(3, 0)  # добавление элемента Quota
                for tourn_file in os.listdir((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures'):
                    # проверить файл "prev" на отдаление финала от текущей даты
                    if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1 and tourn[1] == "prev":
                        with open((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures/'+tourn_file, 'r') as f:
                            file_content = f.read()
                        if DateNow >= PrevCupInfluence(file_content):  # если после финала прошло 150 дней и больше
                            Del_tourn.append(tourn)     # удалить кубок из списка учитываемых турниров
                    # если есть файл "curr" (появляется в каталоге через 400 дней после 1-го матча "prev"), но не наступила дата его 1-го матча - 
                    # удалить кубок "curr"
                    if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1 and tourn[1] == "curr":
                        with open((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures/'+tourn_file, 'r') as f:
                            file_content = f.read()
                        if DateNow <= CupFirst(file_content):
                            Del_tourn.append(tourn)     # удалить кубок из списка учитываемых турниров
                    if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1:
                        tourn[1] = tourn_file[-15:-10]   # изменение "curr/prev" на сезон
        for tourn in Del_tourn:     # удаление турниров prev после потери их актуальности
            Ass_TournRateQuot[ass_n].remove(tourn)    
    
    
    # Tournaments rating
    from modules.league_files import league_files
    from modules.api_request import CupLast
    import json
    for ass_n in Ass_TournRateQuot:
        for tourn in Ass_TournRateQuot[ass_n]:
            
            # рейтинг National League
            if tourn[0].find("League") != -1:
            # определение рейтинга через запрос standings: тк в нац лигах возможны несколько rounds: регулярный сезон, доп группы или матчи на вылет итд
            # League rating = total League clubs SUM(pts+1.2) in TL standigs / Number of clubs in the League
            # prev > curr (1/150 per day from 01.08)
                league_files(tourn[0], tourn[1], tourn[4])   # актуализация файла нац лиги
                # если файл лиги сформирован: расчет League rating, иначе League rating = 0 (это значение уже задано выше)
                for tourn_file in os.listdir((os.path.abspath(__file__))[:-22]+'/cache/answers/standings'):
                    if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1:
                        with open((os.path.abspath(__file__))[:-22]+'/cache/answers/standings/'+tourn_file, 'r', encoding='utf-8') as j:
                            standings_dict = json.load(j)
                        # club set лиги из клубов текущего раунда лиги (["group"] которых = ["group"] 1-го ["rank"] в ["standings"])
                        club_number = 0     # инициализация количества клубов в текущем раунде лиги
                        for team in standings_dict['response'][0]['league']['standings'][0]:
                            club_number += 1
                            for club in standings:   # для каждого id клуба из TL standings
                                if standings[club]['IDapi'] == team['team']['id']: 
                                    tourn[2] += standings[club]['TL_rank'] + 1.2
                        tourn[2] /= club_number
                        # временной фактор: prev > curr (1/150 per day from 01.08)
                        if DateNow.month > 7 and tourn[1][3:] == DateNow.year[2:]:     # для прошлого сезона
                            tourn[2] *= (150 - (DateNow - datetime.datetime(DateNow.year, 7, 31))/datetime.timedelta(days=1)) / 150
                        if DateNow.month > 7 and tourn[1][:2] == DateNow.year[2:]:     # для текущего сезона
                            tourn[2] *= ((DateNow - datetime.datetime(DateNow.year, 7, 31))/datetime.timedelta(days=1)) / 150
            
            # рейтинг National Cup(LCup)
            if tourn[0].find("Cup") != -1:
            # рейтинг кубка curr на протяжении его розыгрыша равен максимальному из своих значений на текущей или предыдущих стадиях
                # для текущей стадии: рейтинг рассчитывается по текущему TL standings
                # для предыдущей стадии: рейтинг рассчитывается по TL standings, актуальному на момент окончания последнего матча стадии
            # Cup rating = max (total Cup stage clubs SUM(pts+1.2) in TL standigs / Number of clubs in the Cup stage) / 5
            # prev > curr (1/150 per day from prev final)
                # формирование словаря из файла fixtures
                for tourn_file in os.listdir((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures'):
                    if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1:
                        with open((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures/'+tourn_file, 'r', encoding='utf-8') as j:
                            fixtures_dict = json.load(j)
                        fixtures_file = tourn_file
                        break
                # актуализация файла рейтингов стадий кубка /cup_round_ratings
                cup_round_ratings(tourn[0], tourn[1], fixtures_dict)
                # определение макс рейтинга стадии по каталогу /cup_round_ratings
                with open((os.path.abspath(__file__))[:-22]+'/cache/sub_results/cup_round_ratings/'\
                    +tourn[0]+' '+tourn[1]+' rate.json', 'r', encoding='utf-8') as j:
                    cup_round_dict = json.load(j)
                for cup_round in cup_round_dict:
                    if cup_round['rating'] > tourn[2]:
                        tourn[2] = cup_round['rating']
                # приведение рейтинга кубка к сложности лиги (/5)
                tourn[2] /= 5
                # учет временного фактора  prev > curr (1/150 per day from prev final)
                if 'prev' in fixtures_file:
                    with open((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures/'+fixtures_file, 'r') as f:
                        file_content = f.read()
                    tourn[2] *= max((150 - (DateNow - CupLast(file_content)) / datetime.timedelta(days=1)) / 150, 0)
                if 'curr' in fixtures_file:
                    with open((os.path.abspath(__file__))[:-22]+'/cache/answers/fixtures/'+fixtures_file.replace('curr', 'prev'), 'r') as f:
                        file_content = f.read()
                    tourn[2] *= min((DateNow - CupLast(file_content)) / datetime.timedelta(days=1) / 150, 1)


    # тест с выгрузкой результата на GH
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'sub_results', 'tournaments.json', Ass_TournRateQuot)


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
