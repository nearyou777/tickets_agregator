import requests
import json
import html2text
import datetime
from models import Tickets, NewTickets, engine, Session
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()
s = requests.Session()
def login() -> str:
    # headers = {
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    #     'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    # }

    params = {
        'returnTo': '/deals',
    }
    response = s.get('https://www.going.com/api/auth/login', params=params)
    r = s.get(response.url)
    data = {
        'username': os.getenv('working_mail'),
        'password': os.getenv('going_pass'),
        'action': 'default',
    }
    r = s.post(r.url, data=data)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    return json.loads(soup.find('script', id="__NEXT_DATA__").text)['props']['pageProps']["accessToken"]



def cash_offers(data:list, token:str):
    headers = {
        'authorization': f'Bearer {token}',
    }
    json_data = {
        'offset': 0,
        'per_page': 100,
        'origin_iata': [],
        'airline_id': [],
        'destination_tag_id': [],
        'availabilities': [],
        'class_of_service': [],
    }

    response = requests.post('https://api.going.com/api/v1/deal-packs', headers=headers, json=json_data)

    for item in response.json()['data']:
        id = f"going-{item['destinationMarketId']}"
        title = item["name"]
        type = 'Cash'
        cabin =  item['cos'].title()
        price = item['price']
        try:
            original_price = item['normalPrice']
        except:
            original_price = 0
        dates = ", ".join(item["availabilities"])
        bookURL = 'https://www.google.com/travel/flights/search'
        departure_cities = '\n'.join([f'{i["originIata"]}' for i in item["departureAirports"]])
        departure_airports = ', '.join([f'({i["originIata"]})' for i in item["departureAirports"]])
        book_guide = '''You can book this flight using google flights!\n or by clicking the button  BOOK NOW bellow'''
        image_link = item["featureImage"]
        picture_name = image_link.split('/')[-1].split('.')[0]
        with open(f'imgs/{picture_name}', 'wb') as f:
            f.write(requests.get(image_link).content)

        summary = f'''✈️Enjoy this deal to {title}✈️\non these dates:\n {dates}\nfor lowest price of {price}'''
        data.append({
            'ID' : id,
            'Title': title, 
            'Type': type, 
            'Cabin': cabin,
            'Price': price, 
            'OriginalPrice' : original_price,
            'Dates' : dates,
            'Book' : bookURL,
            'DepartureCities' : departure_cities.strip(),
            'DepartureAirports' : departure_airports,
            'BookGuide' : book_guide, 
            'Summary' : summary,
            'PictureName' : picture_name})
        
    return data


def scrape_points_deals(data:list, token:str) -> list:

    response = s.get('https://www.going.com/api/airframe/v2/points-campaigns')
    for item in response.json()['data']:
        #TODO: dates
        print(item)
        title = item["campaign_name"]
        id = f'going-{item["id"]}'
        cabin = item["class_of_service"]
        type = 'Points/Miles'
        image_link = item["main_image"]["lg_url"]
        picture_name = image_link.split('/')[-1].split('.')[0]
        with open(f'imgs/{picture_name}', 'wb') as f:
            f.write(requests.get(image_link).content)
        price = item["cost_ranges"]["points"]['min']
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        book_guide = text_maker.handle(item["booking_tip"])
        departure_cities = '\n'.join(item["origin_airports"])
        bookURL = 'https://www.google.com/travel/flights/search'
        departure_airports = ', '.join(item["origin_airports"])
        departure_dates = ', '.join([datetime.datetime.strptime(i, "%Y-%m-%d").strftime("%d %B %Y") for i in item["date_ranges"]["departure"]])
        return_dates = ', '.join([datetime.datetime.strptime(i, "%Y-%m-%d").strftime("%d %B %Y") for i in item["date_ranges"]["departure"]])
        dates = f'''<b>Departure:</b> {departure_dates}\n\n<b>Return:</b> {return_dates}'''
        summary = f'''✈️Deal Summary: Enjoy this deal to {title}✈️\non these dates {dates}\nfor lowest price of {price}'''
        original_price = 0
        data.append({
            'ID' : id,
            'Title': title, 
            'Type': type, 
            'Cabin': cabin,
            'Price': price, 
            'OriginalPrice' : original_price,
            'Dates' : dates,
            'Book' : bookURL,
            'DepartureCities' : departure_cities.strip(),
            'DepartureAirports' : departure_airports,
            'BookGuide' : book_guide, 
            'Summary' : summary,
            'PictureName' : picture_name})
    return data


def add_going():
    token = login()
    data = scrape_points_deals(cash_offers([], token), token)
    with Session() as session:
        if len(data) == 0:
            session.query(NewTickets).delete()
            session.commit()
            return False
        for item in data:
            exist = session.query(Tickets).filter_by(ID = item['ID']).first()
            if not exist:
                session.add(Tickets(**item))
                session.add(NewTickets(**item))
        session.commit()
        count = session.query(NewTickets).count()
        session.commit()
    return count > 0


if __name__ == '__main__':
    add_going()
    