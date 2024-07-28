import datetime, os, json
from modules.api_request import PrevCupInfluence, CupFirst
DateNow = datetime.datetime.utcnow()    # текущая дата по UTC
Ass_TournRateQuot = {'UEFA': [['UCL', '23-24', 1.61, 16, 2, 'Cup'], ['UEL', '23-24', 0.61, 6, 3, 'Cup'], ['UECL', '23-24', 0.13, 1, 848, 'Cup']], 'TopLiga': [['TopLiga', None, 10, 10, None, None]], 'ENG': [['ENG League', 'curr', 'Premier League', 39, 'League'], ['ENG League', 'prev', 'Premier League', 39, 'League'], ['ENG Cup', 'curr', 'FA Cup', 45, 'Cup'], ['ENG Cup', 'prev', 'FA Cup', 45, 'Cup'], ['ENG LCup', 'curr', 'League Cup', 48, 'Cup'], ['ENG LCup', 'prev', 'League Cup', 48, 'Cup']], 'ESP': [['ESP League', 'curr', 'La Liga', 140, 'League'], ['ESP League', 'prev', 'La Liga', 140, 'League'], ['ESP Cup', 'curr', 'Copa del Rey', 143, 'Cup'], ['ESP Cup', 'prev', 'Copa del Rey', 143, 'Cup']], 'GER': [['GER League', 'curr', 'Bundesliga', 78, 'League'], ['GER League', 'prev', 'Bundesliga', 78, 'League'], ['GER Cup', 'curr', 'DFB Pokal', 81, 'Cup'], ['GER Cup', 'prev', 'DFB Pokal', 81, 'Cup']], 'ITA': [['ITA League', 'curr', 'Serie A', 135, 'League'], ['ITA League', 'prev', 'Serie A', 135, 'League'], ['ITA Cup', 'curr', 'Coppa Italia', 137, 'Cup'], ['ITA Cup', 'prev', 'Coppa Italia', 137, 'Cup']], 'POR': [['POR League', 'curr', 'Primeira Liga', 94, 'League'], ['POR League', 'prev', 'Primeira Liga', 94, 'League'], ['POR Cup', 'curr', 'Taça de Portugal', 96, 'Cup'], ['POR Cup', 'prev', 'Taça de Portugal', 96, 'Cup'], ['POR LCup', 'curr', 'Taça da Liga', 97, 'Cup'], ['POR LCup', 'prev', 'Taça da Liga', 97, 'Cup']], 'FRA': [['FRA League', 'curr', 'Ligue 1', 61, 'League'], ['FRA League', 'prev', 'Ligue 1', 61, 'League'], ['FRA Cup', 'curr', 'Coupe de France', 66, 'Cup'], ['FRA Cup', 'prev', 'Coupe de France', 66, 'Cup']], 'NED': [['NED League', 'curr', 'Eredivisie', 88, 'League'], ['NED League', 'prev', 'Eredivisie', 88, 'League'], ['NED Cup', 'curr', 'KNVB Beker', 90, 'Cup'], ['NED Cup', 'prev', 'KNVB Beker', 90, 'Cup']]}
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
            for tourn_file in os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/fixtures'):
                # проверить файл "prev" на отдаление финала от текущей даты
                if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1 and tourn[1] == "prev":
                    with open((os.path.abspath(__file__))[:-15]+'/cache/answers/fixtures/'+tourn_file, 'r', encoding='utf-8') as f:
                        file_content = json.load(f)
                    if DateNow >= PrevCupInfluence(json.dumps(file_content, skipkeys=True, ensure_ascii=False, indent=2)):  # если после финала прошло 150 дней и больше
                        Del_tourn.append(tourn)     # удалить кубок из списка учитываемых турниров
                # если есть файл "curr" (появляется в каталоге через 400 дней после 1-го матча "prev"), но не наступила дата его 1-го матча - 
                # удалить кубок "curr"
                if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1 and tourn[1] == "curr":
                    with open((os.path.abspath(__file__))[:-15]+'/cache/answers/fixtures/'+tourn_file, 'r', encoding='utf-8') as f:
                        file_content = json.load(f)
                    if DateNow <= CupFirst(json.dumps(file_content, skipkeys=True, ensure_ascii=False, indent=2)):
                        Del_tourn.append(tourn)     # удалить кубок из списка учитываемых турниров
                if tourn_file.find(tourn[0]) != -1 and tourn_file.find(tourn[1]) != -1 and tourn not in Del_tourn:
                    tourn[1] = tourn_file[-15:-10]   # изменение "curr/prev" на сезон
            if tourn[1] == "curr" and tourn not in Del_tourn:    # если нет файла fixtures кубка curr (сезон не начался - не изменен на YY-YY)
                Del_tourn.append(tourn)     # удалить кубок из списка учитываемых турниров
    for tourn in Del_tourn:     # удаление турниров prev после потери их актуальности
        Ass_TournRateQuot[ass_n].remove(tourn)    
    print(Ass_TournRateQuot[ass_n])