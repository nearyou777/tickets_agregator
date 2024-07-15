import requests
from datetime import datetime,timedelta
# headers = {
#     'accept': '*/*',
#     'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
#     'if-none-match': 'W/"8079-VWzMxq8QDubh5Q2Axd4G65dnZ3Q"',
#     'origin': 'https://www.pointhound.com',
#     'priority': 'u=1, i',
#     'referer': 'https://www.pointhound.com/',
#     'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
# }

# params = {
#     'origin': 'JFK',
#     'endDate': f'{(datetime.now() + timedelta(weeks=16)).date()}',
#     'startDate': f'{datetime.now().date()}',
#     'cabinClasses': 'economy',
# }
# print((datetime.now() + timedelta(weeks=16)).date())
# response = requests.get('https://scout.pointhound.com/flights/explore/search', params=params, headers=headers)
# print(response)
# import json
# with open('test2.json', 'w') as f:
#     json.dump(response.json(),f,indent=2)



import requests

cookies = {
    '_ga': 'GA1.1.1860182362.1720344320',
    '_hjSessionUser_3719013': 'eyJpZCI6ImUzYzdjMWU1LTFjMTctNWFhZi04YzcwLTQzYTNiNTAwZWUxYiIsImNyZWF0ZWQiOjE3MjAzNDQzMjAxNDEsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjSession_3719013': 'eyJpZCI6IjViYWU2ZWM0LTdhYTktNGVhMC05NmJmLTRhM2IyY2IzMGUwNyIsImMiOjE3MjAzNDQzMjAxNDIsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_hjDonePolls': '993356',
    '_ga_SDDPCWH86G': 'GS1.1.1720344320.1.1.1720344535.0.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'baggage': 'undefined',
    # 'cookie': '_ga=GA1.1.1860182362.1720344320; _hjSessionUser_3719013=eyJpZCI6ImUzYzdjMWU1LTFjMTctNWFhZi04YzcwLTQzYTNiNTAwZWUxYiIsImNyZWF0ZWQiOjE3MjAzNDQzMjAxNDEsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_3719013=eyJpZCI6IjViYWU2ZWM0LTdhYTktNGVhMC05NmJmLTRhM2IyY2IzMGUwNyIsImMiOjE3MjAzNDQzMjAxNDIsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjDonePolls=993356; _ga_SDDPCWH86G=GS1.1.1720344320.1.1.1720344535.0.0.0',
    'priority': 'u=1, i',
    'referer': 'https://www.pointhound.com/explore?search=7a0384afbb56ddb7b72f5a88f690e2c6',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '33d7bbd8a1ff45679185b01feb221b9b-ba85cb59a8241866-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

params = {
    'searchId': 'avs_ozZQHlGgMw',
    'take': '16',
    'offset': '0',
    'sortBy': 'points',
    'sortOrder': 'asc',
    'passengers': '1',
    'countries': 'AG,AW,BS,BB,BM,KY,CR,DO,SV,GT,MX,PA,PR,LC,SX,TC,VI,AT,BE,CZ,DK,FI,FR,DE,GR,IS,IE,IT,NL,PL,PT,RS,ES,SE,CH,GB,CN,HK,IN,ID,IL,JP,JO,LB,QA,SA,SG,KR,TW,TH,TR,AE,AR,BR,CL,CO,EC,PE,DZ,CI,EG,ET,GH,KE,MA,NG,SN,ZA,TZ,AU,NZ,BB,BM,KY,CR,SV,GH,MX,ZA,DZ,AG,AU,BB,BM,BR,KY,CO,CI,EG,FI,GH,IN,ID,IT,JO,LB,MA,NZ,QA,SA,ZA,ES,CH,TR,AE,CO,GT,IS,ZA,KR,CH,AE,IS,DZ,BB,BE,CZ,DK,ET,FI,IS,RS',
    'regions': 'US-AK,US-HI,US-HI,US-HI,US-AK,US-HI,US-AK',
    'earnProgramIds': 'pep_ZRGnAepMcY,pep_a9ue0M8Jmz,pep_3KRWjyajPr,pep_3HN9iHCTDI,pep_LJ3oxvytYb,pep_LzwFfWwlgs,pep_oKAeOffKQ7',
    'redeemProgramIds': 'prp_kMCkTo3GCR,prp_nNix7sQfIi,prp_DUsVaWTUzo,prp_20MH5wRp83,prp_qYBEJAysbA,prp_5EyDDagMq1,prp_BTQuleisDI,prp_2N4BM2TYmY,prp_kR4sEVjfW8,prp_TcZLnN6OgF,prp_c67CoFIfdC,prp_v14WyLi8b3',
}

response = requests.get('https://www.pointhound.com/api/explore', params=params, cookies=cookies, headers=headers)
print(response)
import json
with open('test2.json', 'w') as f:
    json.dump(response.json(),f,indent=2)

