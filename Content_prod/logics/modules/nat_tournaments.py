# модуль содержит словарь национальных турниров большинства европейских ассоциаций, используемых в TL: высшие лиги, кубки стран, кубки лиг, суперкубки
# {Association:[AssType,Season,Tournament,TournID,TournType]}
def Nat_Tournaments():
    Ass_TournIdType = {
                        "ENG": 
                        [
                            ["ENG League", "curr", "Premier League", 39, "League"],
                            ["ENG League", "prev", "Premier League", 39, "League"],
                            ["ENG Cup", "curr", "FA Cup", 45, "Cup"],
                            ["ENG Cup", "prev", "FA Cup", 45, "Cup"],
                            ["ENG LCup", "curr", "League Cup", 48, "Cup"],
                            ["ENG LCup", "prev", "League Cup", 48, "Cup"],
                            ["ENG SCup", "curr", "Community Shield", 528, "Cup"]
                        ],
                        "ESP":
                        [
                            ["ESP League", "curr", "La Liga", 140, "League"],
                            ["ESP League", "prev", "La Liga", 140, "League"],
                            ["ESP Cup", "curr", "Copa del Rey", 143, "Cup"],
                            ["ESP Cup", "prev", "Copa del Rey", 143, "Cup"],
                            ["ESP LCup", "curr", "None", -1, "Cup"],
                            ["ESP LCup", "prev", "None", -1, "Cup"],
                            ["ESP SCup", "curr", "Super Cup", 556, "Cup"]
                        ],
                        "ITA": 
                        [
                            ["ITA League", "curr", "Serie A", 135, "League"],
                            ["ITA League", "prev", "Serie A", 135, "League"],
                            ["ITA Cup", "curr", "Coppa Italia", 137, "Cup"],
                            ["ITA Cup", "prev", "Coppa Italia", 137, "Cup"],
                            ["ITA LCup", "curr", "None", -1, "Cup"],
                            ["ITA LCup", "prev", "None", -1, "Cup"],
                            ["ITA SCup", "curr", "Super Cup", 547, "Cup"]
                        ],
                        "GER": 
                        [
                            ["GER League", "curr", "Bundesliga", 78, "League"],
                            ["GER League", "prev", "Bundesliga", 78, "League"],
                            ["GER Cup", "curr", "DFB Pokal", 81, "Cup"],
                            ["GER Cup", "prev", "DFB Pokal", 81, "Cup"],
                            ["GER LCup", "curr", "None", -1, "Cup"],
                            ["GER LCup", "prev", "None", -1, "Cup"],
                            ["GER SCup", "curr", "Super Cup", 529, "Cup"]
                        ],
                        "FRA": 
                        [
                            ["FRA League", "curr", "Ligue 1", 61, "League"],
                            ["FRA League", "prev", "Ligue 1", 61, "League"],
                            ["FRA Cup", "curr", "Coupe de France", 66, "Cup"],
                            ["FRA Cup", "prev", "Coupe de France", 66, "Cup"],
                            ["FRA LCup", "curr", "None", -1, "Cup"],
                            ["FRA LCup", "prev", "None", -1, "Cup"],
                            ["FRA SCup", "curr", "Trophée des Champions", 526, "Cup"]
                        ],
                        "NED": 
                        [
                            ["NED League", "curr", "Eredivisie", 88, "League"],
                            ["NED League", "prev", "Eredivisie", 88, "League"],
                            ["NED Cup", "curr", "KNVB Beker", 90, "Cup"],
                            ["NED Cup", "prev", "KNVB Beker", 90, "Cup"],
                            ["NED LCup", "curr", "None", -1, "Cup"],
                            ["NED LCup", "prev", "None", -1, "Cup"],
                            ["NED SCup", "curr", "Super Cup", 543, "Cup"]
                        ],
                        "POR": 
                        [
                            ["POR League", "curr", "Primeira Liga", 94, "League"],
                            ["POR League", "prev", "Primeira Liga", 94, "League"],
                            ["POR Cup", "curr", "Taça de Portugal", 96, "Cup"],
                            ["POR Cup", "prev", "Taça de Portugal", 96, "Cup"],
                            ["POR LCup", "curr", "Taça da Liga", 97, "Cup"],
                            ["POR LCup", "prev", "Taça da Liga", 97, "Cup"],
                            ["POR SCup", "curr", "Super Cup", 550, "Cup"]
                        ],
                        "BEL": 
                        [
                            ["BEL League", "curr", "Jupiler Pro League", 144, "League"],
                            ["BEL League", "prev", "Jupiler Pro League", 144, "League"],
                            ["BEL Cup", "curr", "Cup", 147, "Cup"],
                            ["BEL Cup", "prev", "Cup", 147, "Cup"],
                            ["BEL LCup", "curr", "None", -1, "Cup"],
                            ["BEL LCup", "prev", "None", -1, "Cup"],
                            ["BEL SCup", "curr", "Super Cup", 519, "Cup"]
                        ],
                        "TUR": 
                        [
                            ["TUR League", "curr", "Süper Lig", 203, "League"],
                            ["TUR League", "prev", "Süper Lig", 203, "League"],
                            ["TUR Cup", "curr", "Cup", 206, "Cup"],
                            ["TUR Cup", "prev", "Cup", 206, "Cup"],
                            ["TUR LCup", "curr", "None", -1, "Cup"],
                            ["TUR LCup", "prev", "None", -1, "Cup"],
                            ["TUR SCup", "curr", "Super Cup", 551, "Cup"]
                        ],
                        "SCO": 
                        [
                            ["SCO League", "curr", "Premiership", 179, "League"],
                            ["SCO League", "prev", "Premiership", 179, "League"],
                            ["SCO Cup", "curr", "FA Cup", 181, "Cup"],
                            ["SCO Cup", "prev", "FA Cup", 181, "Cup"],
                            ["SCO LCup", "curr", "League Cup", 185, "Cup"],
                            ["SCO LCup", "prev", "League Cup", 185, "Cup"],
                            ["SCO SCup", "curr", "None", -1, "Cup"]
                        ],
                        "CZE": 
                        [
                            ["CZE League", "curr", "Czech Liga", 345, "League"],
                            ["CZE League", "prev", "Czech Liga", 345, "League"],
                            ["CZE Cup", "curr", "Cup", 347, "Cup"],
                            ["CZE Cup", "prev", "Cup", 347, "Cup"],
                            ["CZE LCup", "curr", "None", -1, "Cup"],
                            ["CZE LCup", "prev", "None", -1, "Cup"],
                            ["CZE SCup", "curr", "None", -1, "Cup"]
                        ],
                        "SUI": 
                        [
                            ["SUI League", "curr", "Super League", 207, "League"],
                            ["SUI League", "prev", "Super League", 207, "League"],
                            ["SUI Cup", "curr", "Schweizer Pokal", 209, "Cup"],
                            ["SUI Cup", "prev", "Schweizer Pokal", 209, "Cup"],
                            ["SUI LCup", "curr", "None", -1, "Cup"],
                            ["SUI LCup", "prev", "None", -1, "Cup"],
                            ["SUI SCup", "curr", "None", -1, "Cup"]
                        ],
                        "AUT": 
                        [
                            ["AUT League", "curr", "Bundesliga", 218, "League"],
                            ["AUT League", "prev", "Bundesliga", 218, "League"],
                            ["AUT Cup", "curr", "Cup", 220, "Cup"],
                            ["AUT Cup", "prev", "Cup", 220, "Cup"],
                            ["AUT LCup", "curr", "None", -1, "Cup"],
                            ["AUT LCup", "prev", "None", -1, "Cup"],
                            ["AUT SCup", "curr", "None", -1, "Cup"]
                        ],
                        "DEN": 
                        [
                            ["DEN League", "curr", "Superliga", 119, "League"],
                            ["DEN League", "prev", "Superliga", 119, "League"],
                            ["DEN Cup", "curr", "DBU Pokalen", 121, "Cup"],
                            ["DEN Cup", "prev", "DBU Pokalen", 121, "Cup"],
                            ["DEN LCup", "curr", "None", -1, "Cup"],
                            ["DEN LCup", "prev", "None", -1, "Cup"],
                            ["DEN SCup", "curr", "None", -1, "Cup"]
                        ],
                        "NOR": 
                        [
                            ["NOR League", "curr", "Eliteserien", 103, "League"],
                            ["NOR League", "prev", "Eliteserien", 103, "League"],
                            ["NOR Cup", "curr", "NM Cupen", 105, "Cup"],
                            ["NOR Cup", "prev", "NM Cupen", 105, "Cup"],
                            ["NOR LCup", "curr", "None", -1, "Cup"],
                            ["NOR LCup", "prev", "None", -1, "Cup"],
                            ["NOR SCup", "curr", "None", -1, "Cup"]
                        ],
                        "ISR": 
                        [
                            ["ISR League", "curr", "Ligat Ha'al", 383, "League"],
                            ["ISR League", "prev", "Ligat Ha'al", 383, "League"],
                            ["ISR Cup", "curr", "State Cup", 384, "Cup"],
                            ["ISR Cup", "prev", "State Cup", 384, "Cup"],
                            ["ISR LCup", "curr", "Toto Cup Ligat Al", 385, "Cup"],
                            ["ISR LCup", "prev", "Toto Cup Ligat Al", 385, "Cup"],
                            ["ISR SCup", "curr", "Super Cup", 659, "Cup"]
                        ],
                        "GRE": 
                        [
                            ["GRE League", "curr", "Super League 1", 197, "League"],
                            ["GRE League", "prev", "Super League 1", 197, "League"],
                            ["GRE Cup", "curr", "Cup", 199, "Cup"],
                            ["GRE Cup", "prev", "Cup", 199, "Cup"],
                            ["GRE LCup", "curr", "None", -1, "Cup"],
                            ["GRE LCup", "prev", "None", -1, "Cup"],
                            ["GRE SCup", "curr", "None", -1, "Cup"]
                        ],
                        "UKR": 
                        [
                            ["UKR League", "curr", "Premier League", 333, "League"],
                            ["UKR League", "prev", "Premier League", 333, "League"],
                            ["UKR Cup", "curr", "Cup", 335, "Cup"],
                            ["UKR Cup", "prev", "Cup", 335, "Cup"],
                            ["UKR LCup", "curr", "None", -1, "Cup"],
                            ["UKR LCup", "prev", "None", -1, "Cup"],
                            ["UKR SCup", "curr", "None", 678, "Cup"]
                        ],
                        "SRB": 
                        [
                            ["SRB League", "curr", "Super Liga", 286, "League"],
                            ["SRB League", "prev", "Super Liga", 286, "League"],
                            ["SRB Cup", "curr", "Cup", 732, "Cup"],
                            ["SRB Cup", "prev", "Cup", 732, "Cup"],
                            ["SRB LCup", "curr", "None", -1, "Cup"],
                            ["SRB LCup", "prev", "None", -1, "Cup"],
                            ["SRB SCup", "curr", "None", -1, "Cup"]
                        ],
                        "POL": 
                        [
                            ["POL League", "curr", "Ekstraklasa", 106, "League"],
                            ["POL League", "prev", "Ekstraklasa", 106, "League"],
                            ["POL Cup", "curr", "Cup", 108, "Cup"],
                            ["POL Cup", "prev", "Cup", 108, "Cup"],
                            ["POL LCup", "curr", "None", -1, "Cup"],
                            ["POL LCup", "prev", "None", -1, "Cup"],
                            ["POL SCup", "curr", "Super Cup", 727, "Cup"]
                        ],
                        "CRO": 
                        [
                            ["CRO League", "curr", "HNL", 210, "League"],
                            ["CRO League", "prev", "HNL", 210, "League"],
                            ["CRO Cup", "curr", "Cup", 212, "Cup"],
                            ["CRO Cup", "prev", "Cup", 212, "Cup"],
                            ["CRO LCup", "curr", "None", -1, "Cup"],
                            ["CRO LCup", "prev", "None", -1, "Cup"],
                            ["CRO SCup", "curr", "Super Cup", 1021, "Cup"]
                        ],
                        "CYP": 
                        [
                            ["CYP League", "curr", "1. Division", 318, "League"],
                            ["CYP League", "prev", "1. Division", 318, "League"],
                            ["CYP Cup", "curr", "Cup", 321, "Cup"],
                            ["CYP Cup", "prev", "Cup", 321, "Cup"],
                            ["CYP LCup", "curr", "None", -1, "Cup"],
                            ["CYP LCup", "prev", "None", -1, "Cup"],
                            ["CYP SCup", "curr", "Super Cup", 852, "Cup"]
                        ],
                        "HUN": 
                        [
                            ["HUN League", "curr", "NB I", 271, "League"],
                            ["HUN League", "prev", "NB I", 271, "League"],
                            ["HUN Cup", "curr", "Magyar Kupa", 273, "Cup"],
                            ["HUN Cup", "prev", "Magyar Kupa", 273, "Cup"],
                            ["HUN LCup", "curr", "None", -1, "Cup"],
                            ["HUN LCup", "prev", "None", -1, "Cup"],
                            ["HUN SCup", "curr", "None", -1, "Cup"]
                        ],
                        "SWE": 
                        [
                            ["SWE League", "curr", "Allsvenskan", 113, "League"],
                            ["SWE League", "prev", "Allsvenskan", 113, "League"],
                            ["SWE Cup", "curr", "Svenska Cupen", 115, "Cup"],
                            ["SWE Cup", "prev", "Svenska Cupen", 115, "Cup"],
                            ["SWE LCup", "curr", "None", -1, "Cup"],
                            ["SWE LCup", "prev", "None", -1, "Cup"],
                            ["SWE SCup", "curr", "None", -1, "Cup"]
                        ],
                        "ROU": 
                        [
                            ["ROU League", "curr", "Liga I", 283, "League"],
                            ["ROU League", "prev", "Liga I", 283, "League"],
                            ["ROU Cup", "curr", "Cupa României", 285, "Cup"],
                            ["ROU Cup", "prev", "Cupa României", 285, "Cup"],
                            ["ROU LCup", "curr", "None", -1, "Cup"],
                            ["ROU LCup", "prev", "None", -1, "Cup"],
                            ["ROU SCup", "curr", "Supercupa", 555, "Cup"]
                        ],
                        "BUL": 
                        [
                            ["BUL League", "curr", "First League", 172, "League"],
                            ["BUL League", "prev", "First League", 172, "League"],
                            ["BUL Cup", "curr", "Cup", 174, "Cup"],
                            ["BUL Cup", "prev", "Cup", 174, "Cup"],
                            ["BUL LCup", "curr", "None", -1, "Cup"],
                            ["BUL LCup", "prev", "None", -1, "Cup"],
                            ["BUL SCup", "curr", "Super Cup", 656, "Cup"]
                        ],
                        "RUS": 
                        [
                            ["RUS League", "curr", "Premier League", 235, "League"],
                            ["RUS League", "prev", "Premier League", 235, "League"],
                            ["RUS Cup", "curr", "Cup", 237, "Cup"],
                            ["RUS Cup", "prev", "Cup", 237, "Cup"],
                            ["RUS LCup", "curr", "None", -1, "Cup"],
                            ["RUS LCup", "prev", "None", -1, "Cup"],
                            ["RUS SCup", "curr", "Super Cup", 663, "Cup"]
                        ],
                        "AZB": 
                        [
                            ["AZB League", "curr", "Premyer Liqa", 419, "League"],
                            ["AZB League", "prev", "Premyer Liqa", 419, "League"],
                            ["AZB Cup", "curr", "Cup", 420, "Cup"],
                            ["AZB Cup", "prev", "Cup", 420, "Cup"],
                            ["AZB LCup", "curr", "None", -1, "Cup"],
                            ["AZB LCup", "prev", "None", -1, "Cup"],
                            ["AZB SCup", "curr", "None", -1, "Cup"]
                        ],
                        "SVK": 
                        [
                            ["SVK League", "curr", "Super Liga", 332, "League"],
                            ["SVK League", "prev", "Super Liga", 332, "League"],
                            ["SVK Cup", "curr", "Cup", 680, "Cup"],
                            ["SVK Cup", "prev", "Cup", 680, "Cup"],
                            ["SVK LCup", "curr", "None", -1, "Cup"],
                            ["SVK LCup", "prev", "None", -1, "Cup"],
                            ["SVK SCup", "curr", "None", -1, "Cup"]
                        ]
                      }
    return(Ass_TournIdType)                        