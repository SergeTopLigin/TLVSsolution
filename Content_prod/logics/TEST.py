import os, json, datetime
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
    standings = json.load(j)

with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/worktimes.json', 'r', encoding='utf-8') as j:
    worktimes = json.load(j)
moment_timestamp = worktimes[-1][1]   # время момента расчета
moment_datetime = datetime.date.fromtimestamp(moment_timestamp)
season = moment_datetime.year if moment_datetime.month > 7 else moment_datetime.year - 1
season = str(season)[2:]+'-'+str(season+1)[2:]
dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
for club in standings:
    print(standings[club]['nat'])
    # file_season = season if club['nat']+' League '+season+' stan.json' in dir_standings else \
    # str(int(season[:2])-1)+'-'+season[:2]