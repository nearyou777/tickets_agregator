import requests
import json
import html2text
from going_cfg import headers, cookies

def cash_offers(data:list):
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
        type = 'cash'
        cabin =  item['cos']
        price = item['price']
        original_price = item['normalPrice']
        dates = ", ".join(item["availabilities"])
        bookURL = 'https://www.google.com/travel/flights/search'
        departure_cities = '\n'.join([f'{i["originIata"]}' for i in item["departureAirports"]])
        departure_airports = ', '.join([f'({i["originIata"]})' for i in item["departureAirports"]])
        book_guide = '''You can book this flight using google flights!\n or by clicking the button  BOOK NOW bellow'''
        image_link = item["featureImage"]
        picture_name = image_link.split('/')[-1].split('.')[0]
        with open(f'imgs/{picture_name}', 'wb') as f:
            f.write(requests.get(image_link).content)
        summary = ''
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


def scrape_points_deals(data:list) -> list:
    params = {
        'page': '1',
        'per_page': '100',
    }

    response = requests.get('https://www.going.com/api/airframe/v2/points-campaigns', params=params, headers=headers, cookies=cookies)

    for item in response.json()['data']:
        #TODO: dates
        print(item)
        name = item["campaign_name"]
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

        departure_airports = ', '.join(item["origin_airports"])



def main():
    scrape_points_deals([])


if __name__ == '__main__':
    main()
    