import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/associations.json', 'r') as j:
    associations = json.load(j) # {ass: [rating, quota]} 

print(associations["UEFA"]['quota'])