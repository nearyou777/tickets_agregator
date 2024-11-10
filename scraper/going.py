import requests
import json
import html2text
import datetime
from shared.models import Tickets, Session
from bs4 import BeautifulSoup
import os
from time import sleep
from images_scrapper import save_image


s = requests.Session()

def login() -> str:
    params = {
        'returnTo': '/deals',
    }
    
    max_retries = 15
    retry_count = 0

    while retry_count < max_retries:
        r = s.get('https://www.going.com/api/auth/login', params=params)
        data = {
            'username': os.getenv('WORKING_EMAIL'),
            'password': os.getenv('GOING_PASS'),
            'action': 'default',
        }
        r = s.post(r.url, data=data)
        soup = BeautifulSoup(r.text, 'lxml')
        
        try:
            return json.loads(soup.find('script', id="__NEXT_DATA__").text)['props']['pageProps']["accessToken"]
        except:
            print("Failed to retrieve token, retrying...")
            retry_count += 1
            sleep(120)  # Wait before retrying

    raise Exception("Failed to retrieve token after multiple attempts.")

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
        tickets = []
        with Session() as session:
            for row in session.query(Tickets).filter(Tickets.ID.like("%going%")).all():
                tickets.append(str(row.ID))
            session.commit()
        # print(tickets)
        if id in tickets:
            continue
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
        save_image(picture_name, image_link)

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
        title = item["campaign_name"]
        id = f'going-{item["id"]}'
        tickets = []
        with Session() as session:
            for row in session.query(Tickets).filter(Tickets.ID.like("%going%")).all():
                tickets.append(str(row.ID))
            session.commit()
        if id in tickets:
            continue
        cabin = item["class_of_service"]
        type = 'Points/Miles'
        image_link = item["main_image"]["lg_url"]
        picture_name = image_link.split('/')[-1].split('.')[0]
        save_image(picture_name, image_link)
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
    return data if len(data) > 0 else None


if __name__ == '__main__':
    add_going()
    