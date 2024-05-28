import requests

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpT1laS1VzOXRZTWZRN0ZaelJGciJ9.eyJpc3MiOiJodHRwczovL2F1dGguZ29pbmcuY29tLyIsInN1YiI6ImF1dGgwfDY2NTNhNGRhMjM4ODVkZWEyOGJmZTc4NyIsImF1ZCI6WyJodHRwczovL2FwcC5zY290dHNjaGVhcGZsaWdodHMuY29tL2FwaSIsImh0dHBzOi8vZ29pbmctcHJvZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzE2NzU3ODkwLCJleHAiOjE3MTY4NDQyOTAsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJJSFRMQThWOTJwWlJwd0laeWJKdEFtZ2lCeDdlRWRzVCJ9.WouLwXMpc8xeWP6CNdeu7tGzyMjKdJ6XZ81GGnLCwQ5KMu8ZgknzsZ4V5wxMKuw_HbLGLBsTT9HLcbsK2mxzKREp0x3cyW5IRy-L4lMtf5hUpDFb5AY9XiLUJA56GzVDz6bEMjD1wi4Kk4NFvVH8t510TVCJJAJdhh9k3JU_ggkLg06_RGvk6ZB8gz1fiafCCC21XPoLqyvQcG9jOWYk6_PuTRj8IFPSSZ3eTEdQNCy-0OWMvzjpOJnw6-Xh6er8N_jJeyaI7LBToDja3KfRneNLT8Hw1Q9Rv3a5lXElkdnarXbBXQM-UBEpPQi4sjrnRO93mV5O1OU-s0iT5px4Qg',
    'content-type': 'application/json',
    'origin': 'https://www.going.com',
    'priority': 'u=1, i',
    'referer': 'https://www.going.com/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

json_data = {
    'offset': 0,
    'per_page': 479,
    'origin_iata': [],
    'airline_id': [],
    'destination_tag_id': [],
    'availabilities': [],
    'class_of_service': [],
}
count = 0
while True:
    response = requests.post('https://api.going.com/api/v1/deal-packs', headers=headers, json=json_data)
    # print(response)
    count += 1
    print(count)
    response.json()
# import json
# with open('going.json','w')as f:
#     json.dump(response.json(),f,indent=2)