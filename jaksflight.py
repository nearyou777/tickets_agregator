import requests

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsiaWQiOiI2NmM1ZDViNDE2YzI5ZDQwNzI4MGJiNGIiLCJlbWFpbCI6InZpdGFsaXl0cmF2ZWxzQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoidml0YWxpeXRyYXZlbHNAZ21haWwuY29tIiwiZmlyc3ROYW1lIjoiIiwibGFzdE5hbWUiOiIiLCJoYXNCaWxsaW5nIjp0cnVlfSwiaWF0IjoxNzI1Mzg0MTQ1LCJleHAiOjE3NjE2NzIxNDV9.t6ci0aaRqHOkU1Xwhkfl_80iwv8zvFk9nfnTo-dMTMQ',
    'origin': 'https://members.jacksflightclub.com',
    'priority': 'u=1, i',
    'referer': 'https://members.jacksflightclub.com/deals/archive',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-jfc-source': 'web',
}

params = {
    'page': '100',
    'archive': '0',
    'limit': '50',
}\

response = requests.get('https://jacksflightclub.com/api/deals', params=params, headers=headers)
# print(response)s
import json

with open('test2.json', 'w') as f:
    json.dump(response.json(),f,indent=2)
print(response.json())