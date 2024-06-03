import requests
import json
import tls_client
import html2text
import pyshorteners
from sqlalchemy.orm import sessionmaker
from config import Tickets, NewTickets, engine
# s = requests.Session()
s = tls_client.Session(client_identifier='chrome_105')

def login():
    json_data = {
        'email': 'Vitaliytravels@gmail.com',
        'password': 'Test1234567890!',
        'company_id': '1',
    }

    r = s.post('https://api-v2.pomelotravel.com/api/v1/login', json=json_data)
    return r.json()['token']

def get_data():
    token = login()
    data = []
    headers = {
        'authorization': f'Bearer {token}',
    }
    r = s.get(
        'https://api-v2.pomelotravel.com/api/v1/deals-pomelo?company_id=1&type=International,Domestic&page=1&airports=&per_page=1000',
        headers=headers
    )
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    for item in r.json()['data']:
        #TODO: Optimise runtime
        title = item['title']
        price = item['price']
        original_price = item['normal_price']
        type = 'Cash'
        cabin = item["ticket_type"]
        id = f"Pomelo-{item['id']}"
        dates = item["deal_availability_duration"]
        bookURL = item["booking_links"][0]['link'] if item["booking_links"] else item["booking_instructions_override"][1]["booking_links"][0]['link']
        bookURL = pyshorteners.Shortener().tinyurl.short(bookURL)
        summary = text_maker.handle(item['message_body']).replace('*', '-').replace('--', '*')     
        book_guide = item["booking_instructions_override"] 
        if not book_guide:
            book_guide = '''✅Click the button below to find your desired dates using Google Flights.
✅Plug in the Available Travel Dates (below) for some of the cheapest itineraries for this deal.
✅Book deal!'''
        else:
            intro = text_maker.handle(item["booking_instructions_override"][0]['headline']).replace('*', '-').replace('--', '*')
            option1_title = text_maker.handle(item["booking_instructions_override"][1]['headline']).replace('*', '-').replace('--', '*')
            # short_url = pyshorteners.Shortener().tinyurl.short(url)
            option1_links  = [f'{i["label"]} - {pyshorteners.Shortener().tinyurl.short(i["link"])}' for i in item["booking_instructions_override"][1]["booking_links"]]
            try:
                option2_title = text_maker.handle(item["booking_instructions_override"][2]['headline']).replace('*', '-').replace('--', '*')
                option2_links =  [f'{i["label"]} - {pyshorteners.Shortener().tinyurl.short(i["link"])}' for i in item["booking_instructions_override"][2]["booking_links"]]
            except:
                option2_links = None
            if option2_links:
                book_guide = f'''*Booking Notes*: {intro}
    *Option1*: {option1_title}

    {option1_links}

    *Option2*: {option2_title}

    {option2_links}'''
            else:
                book_guide = f'''*Booking Notes*: {intro}
*Option1*: {option1_title}

{option1_links}
'''
        # print(item["departure_airport_deals"][0]["airport"])
        departure_cities = '\n'.join([f'{i["airport"]["airport_name"]} - ${i["price"]}' for i in item["departure_airport_deals"]])

        departure_airports = ', '.join([f'({i["airport"]["IATA"]})' for i in item["departure_airport_deals"]])
        image_link = f'https://d3mdkiyq6mk8lq.cloudfront.net/{item["featured_image"]}'
        picture_name = item["featured_image"].split('/')[-1]
        with open(f'out/{picture_name}', 'wb') as f:
            f.write(requests.get(image_link).content)
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
            
def add_pomelo() -> bool:
    data = get_data()

    Session = sessionmaker(bind=engine)
    session = Session()
    for item in data:
        exist = session.query(Tickets).filter_by(ID = item['ID']).first()
        if not exist:
            session.add(Tickets(**item))
            session.add(NewTickets(**item))
    session.commit()
    count = session.query(NewTickets).count()
    session.close()
    return count > 0


if __name__ == '__main__':
    add_pomelo()