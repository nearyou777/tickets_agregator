import requests
from bs4 import BeautifulSoup
import html2text
def login():
    s = requests.Session()
    login_data = {
        'username': 'vitaliytavels',
        'password': 'Asd123!@#',
    }
    s.post('https://straighttothepoints.co/login/', data=login_data)
    return s

def get_links(s:requests.Session):
    r = s.get('https://straighttothepoints.co/account/archive.php')

    return [f"https://straighttothepoints.co/account/{i.find('a').get('href')}" for i in BeautifulSoup(r.text, 'lxml').find_all('div', class_='col-12 col-lg-3 mb-4')]


def get_data(s:requests.Session, links:list):
    data = []
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    for url in links:
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        id = url.split('?')[-1].split('=')[-1]
        title = soup.find('h1').text.strip()
        departure_airports = ', '.join([i.text.strip() for i in soup.find('div', class_='col-lg-7 col-sm-12').find('div', class_='row').find_all('div', class_='col-6')[0].find_all('div')[1:]])
        arrival_airports = ', '.join([i.text.strip() for i in soup.find('div', class_='col-lg-7 col-sm-12').find('div', class_='row').find_all('div', class_='col-6')[1].find_all('div')[1:]])
        departure_cities = '\n'.join([i.text.strip() for i in soup.find('div', class_='col-lg-7 col-sm-12').find('div', class_='row').find_all('div', class_='col-6')[0].find_all('div')[1:]])
        departure_cities  = f'{departure_cities}\n*Arrival Airports*:\n\n{arrival_airports}'
        type = 'Points'
        cabin = soup.find('div', class_='col-lg-7 col-sm-12').find('div', class_='row my-4').find_all('div', class_='col-6')[-1].find_all('div')[-1].text.strip()
        dates = soup.find('div', class_='col-lg-7 col-sm-12').find_all('div', class_='row my-4')[-1].find_all('div')[-1].text.strip()
        airline = soup.find('div', class_='col-lg-7 col-sm-12').find('div', class_='row my-4').find_all('div', class_='col-6')[0].find_all('div')[-1].text.strip()
        title = f'{title}\n{airline}'
        guide  = text_maker.handle(str(soup.find_all('div', class_='container py-5')[-1].find('div').find('div', class_='col-lg-7 col-sm-12')))
        summary = soup.find('div', class_='col-12 col-lg-5').text.strip()
        img_link = f"https://straighttothepoints.co/account/{soup.find('img', class_='d-block mx-lg-auto img-fluid shadow').get('src')}"
        # with open('')     
        picture_name = img_link.split('/')[-1]
        with open(f'imgs/{picture_name}', 'wb') as f:
            f.write(s.get(img_link).content)

        # data.append({
        #     'ID' : id,
        #     'Title': title, 
        #     'Type': type, 
        #     'Cabin': cabin,
        #     'Price': price, 
        #     'OriginalPrice' : original_price,
        #     'Dates' : dates,
        #     'Book' : bookURL,
        #     'DepartureCities' : departure_cities.strip(),
        #     'DepartureAirports' : departure_airports,
        #     'BookGuide' : guide, 
        #     'Summary' : summary,
        #     'PictureName' : picture_name})
def main():
    s = login()
    get_data(s, get_links(s))


if __name__ == '__main__':
    main()