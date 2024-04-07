from modules.nat_tournaments import Nat_Tournaments

Nat_Tournaments = Nat_Tournaments()

for ass in Nat_Tournaments:
    for tourn in Nat_Tournaments[ass]:
        print(ord(tourn[0][4:5]))