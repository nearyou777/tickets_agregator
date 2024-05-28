import requests
import json
import pandas as pd
cookies = {
    'ASP.NET_SessionId': 'wop1ivg4vgibjjlzmyr25hxo',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'ASP.NET_SessionId=wop1ivg4vgibjjlzmyr25hxo',
    'origin': 'https://shop.ticket-center-hohenschwangau.de',
    'priority': 'u=1, i',
    'referer': 'https://shop.ticket-center-hohenschwangau.de/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
    'dtStartDate': '03.05.2024',
    'dtSelectedDate': '02.11.2024',
    'nPoolNr': '24',
    'nTicketTypeNr': '41',
    'bReservation': 'true',
    'PersonSelection': [],
    'SelectedSubContigents': [],
    'nPlaces': 1,
    'nDays': 0,
}

response = requests.post(
    'https://shop.ticket-center-hohenschwangau.de/Shop/PerformResStart2/de-DE/39901/',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

data = []
for item in response.json():
    

# print(response)
# with open('test.json', 'w') as f:
#     json.dump(response.json(),f,indent=2)