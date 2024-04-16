import os, datetime, time, json
# print(datetime.datetime.utcfromtimestamp(os.path.getmtime((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/NOR League 23-24 stan.json')))
# print(datetime.datetime.utcnow())

# print(time.time() - os.path.getmtime((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/NOR League 23-24 stan.json'))
# with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/ENG League 23-24 stan.json', 'r', encoding='utf-8') as j:
#     league_standings = json.load(j)
# update_time = league_standings['response'][0]['league']['standings'][0][0]['update'][:10]
# print(datetime.datetime.utcnow() + datetime.timedelta(days=7))
# print(update_time)
# print(datetime.datetime.utcnow() + datetime.timedelta(days=7) < datetime.datetime(int(update_time[:4]), int(update_time[5:7]), int(update_time[8:])))

# print(datetime.datetime.utcnow().year if datetime.datetime.utcnow().month > 4 else datetime.datetime.utcnow().year -1)
Season = str(datetime.datetime.utcnow().year if datetime.datetime.utcnow().month > 3 else datetime.datetime.utcnow().year -1)
print(str(int(Season[2:])+1))