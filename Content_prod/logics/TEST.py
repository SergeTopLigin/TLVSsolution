# import os, json
# with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants_nat.json', 'r', encoding='utf-8') as j:
#     participants = json.load(j)

# from modules.nat_tournaments import Nat_Tournaments
# nat_tournaments = Nat_Tournaments()
# tourns = []
# for ass in participants:
#     if len(participants[ass])>1:
#         for nat_ass in nat_tournaments:
#             if nat_ass == ass:
#                 for tourn in nat_tournaments[nat_ass]:
#                     if [tourn[0], tourn[3]] not in tourns and tourn[3] != -1:
#                         tourns.append([tourn[0], tourn[3]])
# print(tourns)

if 'Cup' in 'ENG LCup':
    print('yes')