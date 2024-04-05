from modules.country_codes import country_codes
country_codes = country_codes()

import os
dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
for file in dir_standings:
    if 'json' in file:
        print(file)