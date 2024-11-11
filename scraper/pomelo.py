import requests
import tls_client
import html2text
import pyshorteners
from shared.models import Tickets, Session
from PIL import Image
import os
from time import sleep
import logging
from dotenv import load_dotenv
from images_scrapper import save_image

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
load_dotenv()
s = tls_client.Session(client_identifier='chrome_105')
logger = logging.getLogger(__name__)
def login():
    json_data = {
        'email': os.getenv('WORKING_EMAIL'),
        'password': os.getenv('POMELO_PASS'),
        'company_id': '1',
    }

    r = s.post('https://api-v2.pomelotravel.com/api/v1/login', json=json_data)
    return r.json()['token']


def reduce_image_size(input_path, output_path, max_size_mb=10):
    max_size_bytes = 1024 * 1024
    
    with Image.open(input_path) as img:
        width, height = img.size
        

        output_format = output_path.split('.')[-1].upper() if output_path.split('.')[-1].upper() != 'JPG' else 'JPEG'
        if output_format not in ['JPEG', 'JPG', 'PNG']:
            output_format = 'PNG'
            output_path = output_path.rsplit('.', 1)[0] + '.PNG'
        
        img.save(output_path, format=output_format, optimize=True, quality=95)
        final_size = os.path.getsize(output_path)
        
        while final_size > max_size_bytes:
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), Image.LANCZOS)
            sleep(0.2)
            img.save(output_path, format=output_format, optimize=True, quality=95)
            final_size = os.path.getsize(output_path)
    if input_path != output_path:
        os.remove(input_path)
    return output_path



def get_data():
    token = login()
    data = []
    headers = {
        'authorization': f'Bearer {token}',
    }
    try:
        r = s.get(
            'https://api-v2.pomelotravel.com/api/v1/deals-pomelo?company_id=1&type=International,Domestic&page=1&airports=&per_page=1000',
            headers=headers
        )
    except:
        sleep(60)
        r = s.get(
            'https://api-v2.pomelotravel.com/api/v1/deals-pomelo?company_id=1&type=International,Domestic&page=1&airports=&per_page=1000',
            headers=headers
        )

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    tickets = []
    with Session() as session:
        for row in session.query(Tickets).filter(Tickets.ID.like("%Pomelo%")).all():
            tickets.append(str(row.ID))
        session.commit()
    for item in r.json()['data'][:10]:
        title = item['title']
        price = item['price']
        original_price = item['normal_price']
        type = 'Cash'
        cabin = item["ticket_type"]
        id = f"Pomelo-{item['id']}"
        if id in tickets:
            continue
        dates = item["deal_availability_duration"]

        try:
            bookURL = item["booking_links"][0]['link'] if item["booking_links"] else item["booking_instructions_override"][1]["booking_links"][0]['link']
            bookURL = str(pyshorteners.Shortener().tinyurl.short(bookURL))
        except:
            bookURL = item["booking_links"][0]['link'] if item["booking_links"] else item["booking_instructions_override"][1]["booking_links"][0]['link']

        summary = text_maker.handle(item['message_body']).replace('*', '-').replace('--', '*').replace('pomelo flight expert', '').replace('shelbi', '').replace('\-', '').strip()
        
        book_guide = item["booking_instructions_override"] 
        if not book_guide:
            book_guide = '''✅Click the button below to find your desired dates using Google Flights.
✅Plug in the Available Travel Dates (below) for some of the cheapest itineraries for this deal.
✅Book deal!'''
        else:
            intro = text_maker.handle(item["booking_instructions_override"][0]['headline']).replace('*', '-').replace('--', '*')
            option1_title = text_maker.handle(item["booking_instructions_override"][1]['headline']).replace('*', '-').replace('--', '*')
            try:
                option1_links  = '\n'.join([f'{i["label"]} - {pyshorteners.Shortener().tinyurl.short(i["link"])}' for i in item["booking_instructions_override"][1]["booking_links"]])
            except:
                option1_links  = '\n'.join([f'{i["label"]} - {i["link"]}' for i in item["booking_instructions_override"][1]["booking_links"]])

            try:
                option2_title = text_maker.handle(item["booking_instructions_override"][2]['headline']).replace('*', '-').replace('--', '*')
                try:
                    option2_links =  '\n'.join([f'{i["label"]} - {pyshorteners.Shortener().tinyurl.short(i["link"])}' for i in item["booking_instructions_override"][2]["booking_links"]])
                except:
                    option2_links =  '\n'.join([f'{i["label"]} - {i["link"]}' for i in item["booking_instructions_override"][2]["booking_links"]])

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
                

        departure_cities = '\n'.join([f'<b>{i["airport"]["airport_name"]} - ${i["price"]}</b>' for i in item["departure_airport_deals"]])
        departure_airports = ', '.join([f'({i["airport"]["IATA"]})' for i in item["departure_airport_deals"]])


        image_link = f'https://d3mdkiyq6mk8lq.cloudfront.net/{item["featured_image"]}'
        picture_name = item["featured_image"].split('/')[-1]

        with open(f'imgs/{picture_name}', 'wb') as f:
            r = requests.get(image_link)
            f.write(r.content)
            if r.status_code == 413:
                image_link = f'https://d3mdkiyq6mk8lq.cloudfront.net/{item["original_deal_image"]}'
                try:
                    picture_name = item["original_deal_image"].split('/')[-1]
                except:
                    picture_name = None
                if picture_name != None:
                    save_image(picture_name, image_link)

        if picture_name:
            path = reduce_image_size(f'imgs/{picture_name}', f'imgs/{picture_name}').split('/')[1]
        else: path = None
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
            'PictureName' : path})

    return data
            
def add_pomelo() -> bool:
    data = get_data()
    return data if len(data) > 0 else None


if __name__ == '__main__':
    add_pomelo()