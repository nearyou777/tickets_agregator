import requests
from dotenv import load_dotenv
import os
load_dotenv()


def save_image(picture_name:str, image_link:str):
    with open(f'imgs/{picture_name}', 'wb') as f:
        r = requests.get(image_link)
        f.write(r.content)
    return picture_name



def google_image_search(query, num_results=1):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv('GOOGLE_API_KEY'),
        "cx": os.getenv('CX'),
        "q": query,
        "searchType": "image", 
        "num": num_results  
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        image_urls = [item['link'] for item in data.get('items', []) if int(item['image']['width']) <= 1280 and int(item['image']['height']) <= 1280 and int(item['image']['width']) > int(item['image']['height']) and 'wikimedia' not in item['link']]
        if num_results == 10:
            image_urls = [item['link'] for item in data.get('items', [])]

        if len(image_urls) == 0:
            return google_image_search(query=query, num_results= num_results+1)
        else:
            print(image_urls)
            return image_urls[0]
    else:
        print("Error: ", response.status_code, response.text)
        return None
    
if __name__ == '__main__':
    google_image_search(query='sunset')
