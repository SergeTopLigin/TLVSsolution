'''
добавить в final_standings.json ключ 'club_qouta' по только что рассчитаным participants из games.json
а также 'club_TLpos' и 'club_NATpos'
в квоту добавить подробнее: нац лига сезон и место

итоговый вид словаря final_standings.json
{
  "Atalanta": {
    "IDapi": 499,
    "nat": "ITA",
    "TL_rank": 1.63,
    "visual_rank": 67,
    "played": 3,
    "buffer": false,
добавить:
    "club_TLpos": 1
    "club_NATpos": 7
    "club_qouta": [
        "UCL curr 8",
        "TopLiga 1",
        "ITA League prev 2"
        ]
    }
}
'''