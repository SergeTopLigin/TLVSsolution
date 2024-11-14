# определение года в веб-адресе
import datetime
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
    message = \
        'uefa_standings\n'+\
        'ошибка при парсинге UEFA club ranking\n'+\
        'https://kassiesa.net/uefa/data/method5/trank'+str(adress_year)+'.html\n'+\
        'код ответа сервера != 200'
    print(message)

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
    from modules.clubname_fix import clubname_fix  # модуль словаря {kassiesa:apifootball}
    converting = clubname_fix()
    for club in UEFA50:
        for club_fix in converting:
            if club == club_fix:
                UEFA50upg[converting[club_fix]] = UEFA50[club]
                DelUEFA.append(club)    # внесение неверных ключей словаря в словарь на удаление
    for club in DelUEFA:     # удаление исправленных
        del UEFA50[club] 
    for club in UEFA50upg:      # добавление исправленных
        UEFA50[club] = UEFA50upg[club]


# import json, os
# with open((os.path.abspath(__file__))[:-30]+'/preparing/UEFA50.json', 'r', encoding='utf-8') as j:
#     UEFA50 = json.load(j)

# если в словаре есть клуб несоответсвующий ни одному из имен в каталоге /standings - создать bug_file
import os   # импорт модуля работы с каталогами
import json
with open((os.path.abspath(__file__))[:-30]+'/cache/teams_list.json', 'r', encoding='utf-8') as j:
    teams_list = json.load(j)
for club in UEFA50:
    find_club = 0
    for nat in teams_list:
        for team in teams_list[nat]:
            if team == club:
                find_club = 1
                break
        if find_club == 1:
            break
    if find_club == 0:
        # отправка bug_file в репозиторий GitHub и на почту
        message = \
            club+'   имя клуба не соответсвует apisports,'+\
            ' внести в clubname_fix или добавить лигу в /cache/teams_list.json'
        print(message)

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
uefa_standings = dict(sorted(UEFA50.items(), key=lambda x: x[1], reverse=True))

# приведение словаря uefa_standings к виду {club:[TL_rank,visual_rank]} 
# с установкой визуально понятного рейтинга - в диапазоне 0-100 между 1-м и последним клубом
TL_max = max(uefa_standings.values())
TL_min = min(uefa_standings.values())
for club in uefa_standings:
    TL_rank = uefa_standings[club]
    visual_rank = int(round(100 * (uefa_standings[club] - TL_min) / (TL_max - TL_min), 0))
    uefa_standings[club] = [TL_rank, visual_rank]
    
# приведение словаря uefa_standings {club:[TL_rank,visual_rank]} 
# к виду {club: {IDapi: , nat: , TL_rank: , visual_rank: , buffer: }}
with open((os.path.abspath(__file__))[:-30]+'/preparing/api_teams.json', 'r', encoding='utf-8') as j:
    api_teams = json.load(j)
uefa_standings_upg = {}
for club in uefa_standings:
    for nat in api_teams:
        for team in nat['response']:
            if team['team']['name'] == club:
                for nat_l in teams_list:
                    for team_l in teams_list[nat_l]:
                        if team_l == club:
                            uefa_standings_upg[club] = {'IDapi': team["team"]["id"], 'nat': nat_l, \
                            'TL_rank': uefa_standings[club][0], 'visual_rank': uefa_standings[club][1], 'buffer': False}

with open((os.path.abspath(__file__))[:-30]+'/cache/uefa_standings.json', 'w', encoding='utf-8') as j:
    json.dump(uefa_standings_upg, j, skipkeys=True, ensure_ascii=False, indent=2)

# print(json.dumps(uefa_standings_upg, skipkeys=True, ensure_ascii=False, indent=2))