import os   # импорт модуля работы с каталогами
dir_standings = os.listdir(os.path.dirname(os.path.abspath(__file__))[:-7]+'/cache/answers/standings')
print(dir_standings)
for file in dir_standings:
    with open(os.path.dirname(os.path.abspath(__file__))[:-7]+'/cache/answers/standings/'+file, 'r') as f:
        for line in f:  # цикл по строкам
            print(line[100:200])