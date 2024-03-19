import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/final_standings.json', 'r') as j:
    standings = json.load(j)

# same_ranks = [standings[club]['TL_rank'] for club in standings if standings[club]['TL_rank'] == ]
all_ranks = []
same_ranks = []
for club in standings:
    all_ranks.append(standings[club]['TL_rank'])
for rank in range(0, len(all_ranks)-2):
    if all_ranks[rank] == all_ranks[rank+1] and all_ranks[rank] not in same_ranks:
        same_ranks.append(all_ranks[rank])
