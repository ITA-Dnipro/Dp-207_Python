from bs4 import BeautifulSoup
import requests


class ScraperForRestaurants:
    """
    Main class for parsing info from donor-site tomato.ua
    """
    def __init__(self, city, text_request='', page_number=1):
        self.city = city
        self.text_request = text_request
        self.page_number = page_number
        self.URL = f'http://tomato.ua/{self.city}/p-{page_number}'
        self.HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }

    def get_content(self, params=''):
        response = requests.get(self.URL, headers=self.HEADERS, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='search-item__box')
        content = []

        for item in items:
            item_title = item.find('a', class_='search-item__center-title desctop').get_text().strip().replace('\n', '').replace('  ', '')
            item_type = item.find('div', class_='search-item__center-content-item').get_text().strip().replace('\n', '').replace('Тип:', '').replace('  ', '')
            item_address = item.find('div', class_='search-item__center-item-loc d-d-f').find('span').get_text().strip().replace('\n', '').replace('  ', '')
            
            if item.find('span', class_='average_bill') is not None:
                temp_price_lvl = item.find('span', class_='average_bill').attrs['data-val'].strip().replace('\n', '').replace('  ', '')
                item_price_lvl = "price level: "
                for _ in range(int(temp_price_lvl)):
                    item_price_lvl += "$"
            else:
                item_price_lvl = ''
            if item.find('div', class_='search-item__time-work p-10') is not None:
                item_timetable = item.find('div', class_='search-item__time-work p-10').get_text().strip().replace('\n', '').replace('  ', '')
            else:
                item_timetable = ''    
            
            if item.find('div', class_='rest_block_raiting').get_text() is not None and item.find('div', class_='rest_block_raiting').get_text().strip().replace('\n', '').replace('  ', '') is not "?":
                item_rating = item.find('div', class_='rest_block_raiting').get_text().strip().replace('\n', '').replace('  ', '')
            else:
                item_rating = 'Not Rated'
            item_photo = item.find('a', class_='search-item__left-search_item_img').attrs['style'].replace("background-image: url('", '').replace("')", '')

            content.append(
                {
                    'title':item_title,
                    'timetable':item_timetable,
                    'type':item_type,
                    'address':item_address,
                    'price_lvl':item_price_lvl,
                    'rating':item_rating,
                    'photo': item_photo
                }
            )
        return content


if __name__ == "__main__":
    parser = ScraperForRestaurants()
    result = parser.get_content()