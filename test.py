# import undetected_chromedriver as uc 
from time import sleep
from bs4 import BeautifulSoup
import requests
from requests import Session
import json
# headers = {
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# params = {
#     'returnTo': '/deals',
# }
# s = Session()

# response = s.get('https://www.going.com/api/auth/login', params=params, headers=headers)
# print(response)
# # print(response.text)
# r = s.get(response.url, headers=headers)
# print(r.url)
# data = {
#     'username': 'vitravelsoft@gmail.com',
#     'password': 'Asd123!@#',
#     'action': 'default',
# }
# r = s.post(r.url, data=data)
# soup = BeautifulSoup(r.text, 'lxml')
# token = json.loads(soup.find('script', id="__NEXT_DATA__").text)['props']['pageProps']["accessToken"]

a = 'dfadsdsf ffkjdslfjdsjkl'
b =a.title()
print(b)
# headers = {
#     'accept': '*/*',
#     'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
#     'authorization': f'Bearer {token}',
#     'content-type': 'application/json',
#     'origin': 'https://www.going.com',
#     'priority': 'u=1, i',
#     'referer': 'https://www.going.com/',
#     'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
# }

# json_data = {
#     'offset': 0,
#     'per_page': 16,
#     'origin_iata': [],
#     'airline_id': [],
#     'destination_tag_id': [],
#     'availabilities': [],
#     'class_of_service': [],
# }
# response = s.get('https://www.going.com/api/airframe/v2/points-campaigns')
# print(response.json())
# response = requests.post('https://api.going.com/api/v1/deal-packs', headers=headers, json=json_data)
# print(response.json())
# with open('test.json', 'w') as f:
#     json.dump(json.loads(token), f, indent=2)
# print(r.url)
# print(r.text)
# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(r.text)
# response = s.get('https://www.going.com/api/auth/callback')
# print(response.json())
# json_data = {
#     'offset': 0,
#     'per_page': 100,
#     'origin_iata': [],
#     'airline_id': [],
#     'destination_tag_id': [],
#     'availabilities': [],
#     'class_of_service': [],
# }

# response = s.get('https://api.going.com/api/v1/deal-packs', json=json_data)
# print(response.json())
# with open('test.json', 'w') as f:
#     json.dump(response.json(),f,indent=2)

# print(r.text)
# driver = uc.Chrome()
# driver.get('https://www.going.com/deals')
# sleep(10000)