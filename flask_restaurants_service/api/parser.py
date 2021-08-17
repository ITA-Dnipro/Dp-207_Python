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
            content.append(
                {
                    'title':item.find('a', class_='search-item__center-title desctop').get_text().strip().replace('\n', '').replace('  ', ''),
                    'timetable':item.find('div', class_='search-item__time-work p-10').get_text().strip().replace('\n', '').replace('  ', ''),
                    'type':item.find('div', class_='search-item__center-content-item').get_text().strip().replace('\n', '').replace('Тип:', '').replace('  ', ''),
                    'address':item.find('div', class_='search-item__center-item-loc d-d-f').find('span').get_text().strip().replace('\n', '').replace('  ', ''),
                    'price_lvl':item.find('span', class_='average_bill').attrs['data-val'].strip().replace('\n', '').replace('  ', ''),
                    'rating':item.find('div', class_='rest_block_raiting').get_text().strip().replace('\n', '').replace('  ', ''),
                    'photo':item.find('a', class_='search-item__left-search_item_img').attrs['style'].replace("background-image: url('", '').replace("')", '') 
                }
            )
        return content


if __name__ == "__main__":
    parser = ScraperForRestaurants("dnepr")
    result = parser.get_content()
    print(result)