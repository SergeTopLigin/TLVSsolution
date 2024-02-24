import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/uefa_standings.json', 'r') as j:
    uefa_standings = json.load(j)   # {club: {IDapi: , nat: , TL_rank: , visual_rank: }}
# uefa_standings = 'uefa standings'
mod_name = os.path.basename(__file__)[:-3]
from modules.runner_push import runner_push
runner_push(str(mod_name), 'sub_results', 'test.json', uefa_standings)
