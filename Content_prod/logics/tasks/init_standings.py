import traceback    # модуль трассировки для отслеживания ошибок
import datetime     # модуль для определния текущей даты
DateNowExc = str(datetime.datetime.utcnow())[:19].replace(":", "-")    # текущая дата по UTC, отформатированная под строку для имени файла

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # определение года в веб-адресе
    adress_year = datetime.datetime.utcnow()
    if adress_year.month < 9:
        adress_year = adress_year.year
    else:
        adress_year = adress_year.year +1

    from bs4 import BeautifulSoup
    import requests
    url = 'https://kassiesa.net/uefa/data/method5/trank'+str(adress_year)+'.html'
    response = requests.get(url)
    if str(response) != '<Response [200]>':     # создание файла ошибки с указанием файла кода и строки в нем
        with open("../../bug_files/"+DateNowExc+" init_standings.txt", 'w', encoding='utf-8') as f:
            f.write('ошибка при парсинге UEFA club ranking\n')
            f.write('https://kassiesa.net/uefa/data/method5/trank'+str(adress_year)+'.html\n')
            f.write('код ответа сервера != 200')

    else:
        Page = str(BeautifulSoup(response.text,"html.parser"))
        # формирование словаря рейтинга УЕФА из html кода страницы
        UEFA50 = {}     # словарь рейтинга УЕФА {club:rate}
        kursor = 0      # начальная позиция поиска
        for num in range(0, 50):
            NameBegin = Page.find('>', Page.find('<td class="aleft', kursor)) +1
            NameEnd = Page.find('</td>', NameBegin)
            kursor = NameEnd
            club = Page[NameBegin : NameEnd]     # создание ключа словаря: имя клуба
            RateBegin = Page.find('<th class="lgray">', kursor) +18
            RateEnd = Page.find('</th>', RateBegin)
            kursor = RateEnd
            UEFA50[club] = Page[RateBegin : RateEnd]     # создание значения словаря: рейтинг клуба

        # преобразование имен клубов по apisports
        UEFA50upg = {}      # словарь измененных ключей
        DelUEFA = []        # список ключей словаря на удаление
        for club in UEFA50:
            if club == 'West Ham United':   UEFA50upg['West Ham'] = UEFA50[club]
            if club == 'Tottenham Hotspur':   UEFA50upg['Tottenham'] = UEFA50[club]
            if club == 'Bayern MÃ¼nchen':   UEFA50upg['Bayern Munich'] = UEFA50[club]
            if club == 'FC Barcelona':   UEFA50upg['Barcelona'] = UEFA50[club]
            if club == 'AtlÃ©tico Madrid':   UEFA50upg['Atletico Madrid'] = UEFA50[club]
            if club == 'Paris Saint-Germain':   UEFA50upg['Paris Saint Germain'] = UEFA50[club]
            if club == 'Olympique Lyon':   UEFA50upg['Lyon'] = UEFA50[club]
            if club == 'Stade Rennais':   UEFA50upg['Rennes'] = UEFA50[club]
            if club == 'Lille OSC':   UEFA50upg['Lille'] = UEFA50[club]
            if club == 'Internazionale':   UEFA50upg['Inter'] = UEFA50[club]
            if club == 'Olympique Marseille':   UEFA50upg['Marseille'] = UEFA50[club]
            if club == 'Sporting CP Lisbon':   UEFA50upg['Sporting CP'] = UEFA50[club]
            if club == 'Sporting Braga':   UEFA50upg['SC Braga'] = UEFA50[club]
            if club == 'Toulouse FC':   UEFA50upg['Toulouse'] = UEFA50[club]
            if club == 'RC Lens':   UEFA50upg['Lens'] = UEFA50[club]
            if club == 'Glasgow Rangers':   UEFA50upg['Rangers'] = UEFA50[club]
            if club == 'Club Brugge':   UEFA50upg['Club Brugge KV'] = UEFA50[club]
            if club == 'AA Gent':   UEFA50upg['Gent'] = UEFA50[club]
            if club == 'Union Saint-Gilloise':   UEFA50upg['Union St. Gilloise'] = UEFA50[club]
            if club == 'Viktoria Plzen':   UEFA50upg['Plzen'] = UEFA50[club]
            if club == 'FC Basel':   UEFA50upg['FC Basel 1893'] = UEFA50[club]
            if club == 'Young Boys':   UEFA50upg['BSC Young Boys'] = UEFA50[club]
            if club == 'Servette FC Genève':   UEFA50upg['Servette FC'] = UEFA50[club]
            if club == 'FC KÃ¸benhavn':   UEFA50upg['FC Copenhagen'] = UEFA50[club]
            if club == 'FC Salzburg':   UEFA50upg['Red Bull Salzburg'] = UEFA50[club]
            if club == 'LASK':   UEFA50upg['Lask Linz'] = UEFA50[club]
            if club == 'Red Star Belgrade':   UEFA50upg['FK Crvena Zvezda'] = UEFA50[club]
            if club == 'PAOK Thessaloniki':   UEFA50upg['PAOK'] = UEFA50[club]
            if club == 'Maccabi Tel-Aviv':   UEFA50upg['Maccabi Tel Aviv'] = UEFA50[club]
            if club == 'FenerbahÃ§e':   UEFA50upg['Fenerbahce'] = UEFA50[club]
            if club == 'Qarabag FK':   UEFA50upg['Qarabag'] = UEFA50[club]
            if club == 'BodÃ¸/Glimt':   UEFA50upg['Bodo/Glimt'] = UEFA50[club]
            if club == 'Molde FK':   UEFA50upg['Molde'] = UEFA50[club]
            if club == 'Ludogorets Razgrad':   UEFA50upg['Ludogorets'] = UEFA50[club]
            if club == 'Legia Warsaw':   UEFA50upg['Legia Warszawa'] = UEFA50[club]
            if club == 'FerencvÃ¡ros':   UEFA50upg['Ferencvarosi TC'] = UEFA50[club]
        # внесение неверных ключей словаря в словарь на удаление
            if club == 'West Ham United':   DelUEFA.append(club)
            if club == 'Tottenham Hotspur':   DelUEFA.append(club)
            if club == 'Bayern MÃ¼nchen':   DelUEFA.append(club)
            if club == 'FC Barcelona':   DelUEFA.append(club)
            if club == 'AtlÃ©tico Madrid':   DelUEFA.append(club)
            if club == 'Paris Saint-Germain':   DelUEFA.append(club)
            if club == 'Olympique Lyon':   DelUEFA.append(club)
            if club == 'Stade Rennais':   DelUEFA.append(club)
            if club == 'Lille OSC':   DelUEFA.append(club)
            if club == 'Internazionale':   DelUEFA.append(club)
            if club == 'Olympique Marseille':   DelUEFA.append(club)
            if club == 'Sporting CP Lisbon':   DelUEFA.append(club)
            if club == 'Sporting Braga':   DelUEFA.append(club)
            if club == 'Toulouse FC':   DelUEFA.append(club)
            if club == 'RC Lens':   DelUEFA.append(club)
            if club == 'Glasgow Rangers':   DelUEFA.append(club)
            if club == 'Club Brugge':   DelUEFA.append(club)
            if club == 'AA Gent':   DelUEFA.append(club)
            if club == 'Union Saint-Gilloise':   DelUEFA.append(club)
            if club == 'Viktoria Plzen':   DelUEFA.append(club)
            if club == 'FC Basel':   DelUEFA.append(club)
            if club == 'Young Boys':   DelUEFA.append(club)
            if club == 'Servette FC Genève':   DelUEFA.append(club)
            if club == 'FC KÃ¸benhavn':   DelUEFA.append(club)
            if club == 'FC Salzburg':   DelUEFA.append(club)
            if club == 'LASK':   DelUEFA.append(club)
            if club == 'Red Star Belgrade':   DelUEFA.append(club)
            if club == 'PAOK Thessaloniki':   DelUEFA.append(club)
            if club == 'Maccabi Tel-Aviv':   DelUEFA.append(club)
            if club == 'FenerbahÃ§e':   DelUEFA.append(club)
            if club == 'Qarabag FK':   DelUEFA.append(club)
            if club == 'BodÃ¸/Glimt':   DelUEFA.append(club)
            if club == 'Molde FK':   DelUEFA.append(club)
            if club == 'Ludogorets Razgrad':   DelUEFA.append(club)
            if club == 'Legia Warsaw':   DelUEFA.append(club)
            if club == 'FerencvÃ¡ros':   DelUEFA.append(club)

        for club in DelUEFA:     # удаление исправленных
            del UEFA50[club] 

        for club in UEFA50upg:      # добавление исправленных
            UEFA50[club] = UEFA50upg[club]

        # если в словаре есть клуб несоответсвующий ни одному из имен в каталоге - создать bug_file
        import os   # импорт модуля работы с каталогами
        for club in UEFA50:
            find_club = 0
            for file in os.listdir('standings/'):  
                with open("standings/"+file, 'r') as f:
                    for line in f:  # цикл по строкам
                        end_substr = 0
                        while True:     # бесконечный цикл
                            if line.find('name":"',end_substr) ==-1:
                                break
                            kursor = line.find('name":"',end_substr) +7    # переместить курсор перед искомой подстрокой
                            end_substr = line.find('","',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                            if club == line[kursor:end_substr]:
                                find_club = 1
                                break
                if find_club == 1:
                    break
            if find_club == 0:
                with open("bug_file.txt", 'w', errors='replace') as f:
                    traceback.print_stack(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки
                    f.write(club+'   имя клуба не соответсвует apisports, внести в раздел "преобразование"')
                with open("bug_file.txt", 'r') as f:
                    bug_info = f.read()             # чтение ошибки в переменную для дальнейшего импорта при создании файла в репозиторие
                repo.create_file("bug_files/"+DateNow+".txt", "bug_file", bug_info, branch="main")


        # расчет TLstandings initial
        # (UEFA_club - UEFA_min) * (TL_max(2.2) - TL_min(-1.2)) / (UEFA_max - UEFA_min) - 1.2
        for club in UEFA50:
            UEFA50[club] = float(UEFA50[club])  # приведение строки к числу
        # определение макс и мин коэф в УЕФА топ50 
        UEFA_max = max(UEFA50.values())
        UEFA_min = min(UEFA50.values())
        for club in UEFA50:
            UEFA50[club] = round((UEFA50[club] - UEFA_min) * (2.2 - (-1.2)) / (UEFA_max - UEFA_min) - 1.2, 2)

        # сортировка TLstandings по убыванию: словаря по значению
        TL_standings = dict(sorted(UEFA50.items(), key=lambda x: x[1], reverse=True))

        # приведение словаря TL_standings к виду {club:[TL_rank,visual_rank]} 
        # с установкой визуально понятного рейтинга - в диапазоне 0-100 между 1-м и последним клубом
        TL_max = max(TL_standings.values())
        TL_min = min(TL_standings.values())
        for club in TL_standings:
            TL_rank = TL_standings[club]
            visual_rank = round(100 * (TL_standings[club] - TL_min) / (TL_max - TL_min), 0)
            TL_standings[club] = [TL_rank, visual_rank]

        # формирование строки из словаря в читабельном виде
        TL_standings_str = ''   # github принимает только str для записи в файл
        for club in TL_standings:
            TL_standings_str += "{0:20}   {2:3.0f}   {1:5.2f}".format(club, TL_standings[club][0], TL_standings[club][1]) + '\n'
        # формирование в конце строки списка для передачи в дальнейшие расчеты
        TL_standings_str += '\noutput list['
        for club in TL_standings:
            TL_standings_str += r'["'+club+r'", '+str(TL_standings[club][0])+', '+str(TL_standings[club][1])+'],'
        TL_standings_str = TL_standings_str[:-1] + ']'      # удаление последней запятой
        # вывод строки в .txt в репозиторий
        all_contents = repo.get_contents("")    # если в репозитории есть этот файл - сделать его update
        if "TLstandings_fromUEFAcoef.txt" in str(all_contents):
            contents = repo.get_contents("TLstandings_fromUEFAcoef.txt", ref="main")
            repo.update_file(contents.path, "TL standings from current UEFA ranking without >1/365>", TL_standings_str, contents.sha, branch="main")
        else:   # иначе создать файл
            repo.create_file("TLstandings_fromUEFAcoef.txt", "TL standings from current UEFA ranking without >1/365>", TL_standings_str, branch="main")

        # for club in TL_standings:
        #     print(club,'   ',TL_standings[club])

except: 
    with open("bug_file.txt", 'w') as f:
        traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки
    with open("bug_file.txt", 'r') as f:
        bug_info = f.read()             # чтение ошибки в переменную для дальнейшего импорта при создании файла в репозиторие
    repo.create_file("bug_files/"+DateNow+".txt", "bug_file", bug_info, branch="main")

g.close()