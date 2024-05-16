import tls_client
import requests
import json
s = tls_client.Session(client_identifier='chrome_105')

json_data = {
    'email': 'Vitaliytravels@gmail.com',
    'password': 'Test1234567890!',
    'company_id': '1',
}

response = s.post('https://api-v2.pomelotravel.com/api/v1/login', json=json_data)
print(response)
auth_token = response.json()['token']

params = {
    'company_id': 1,
    'type': 'International,Domestic',
    'airports': '',
    'page': 1,
    'per_page': 10000
}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'authorization': f'Bearer {auth_token}',
    'baggage': 'sentry-environment=production,sentry-public_key=6e9a1e0e3c20b614109d37d4ca2f13e3,sentry-trace_id=7e27f5a697044bb99979796b4fc87604',
    'origin': 'https://app.pomelotravel.com',
    'priority': 'u=1, i',
    'referer': 'https://app.pomelotravel.com/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sentry-trace': '7e27f5a697044bb99979796b4fc87604-aa95ed5b90b058e6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://api-v2.pomelotravel.com/api/v1/deals-pomelo',
    headers=headers,
    params=params
)
for item in response.json()['data']:
    title = item['title']
    price = item['price']
    book = item["booking_links"][0]['link']
    id = item['id']
    type = 'Cash'
    cabin = item["ticket_type"]
# with open('test2.json', 'w') as f:
#     json.dump(response.json(),f,indent=2)