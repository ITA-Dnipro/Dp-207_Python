import requests
from lxml import html
from random import choice
import time
import concurrent.futures
import json


class CustomException(Exception):
    def __init__(self, msg):
        self.msg = msg


class CityNotExists(CustomException):
    pass


class ScraperForHotel():
    """
    Class for scrapping the site hotels24.ua
    """

    desktop_agents = [
        'Mozilla/5.0 (Window s NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) '
        'Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 '
        'Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

    URL = 'https://hotels24.ua'

    def __init__(self, city):
        self.city = city

    @staticmethod
    def random_headers():
        return {'User-Agent': choice(ScraperForHotel.desktop_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    @staticmethod
    def add_domen(url_for_detail):
        url_for_detail = ScraperForHotel.URL + '/' + url_for_detail
        return url_for_detail

    @staticmethod
    def parse_adress(adress):
        tmp = adress[1].split(', ')
        adress = ' '.join(tmp).strip()
        return adress

    @staticmethod
    def request(url):
        """
        Takes url and send request to the url and returns tree of elements DOM
        """
        try:
            response = requests.get(url, headers=ScraperForHotel.random_headers())
            tree = html.fromstring(response.text)
            return tree
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    @staticmethod
    def find_url_for_cities(url):
        """
        Find the appropriate url for cities list
        """
        tree = ScraperForHotel.request(url)
        href = tree.xpath('//div[@class = "panel active"]/ul/li/a/@href')
        count = 0
        if href:
            print(count)
            url = 'https:' + href[-1]
            return url
        elif href or count <= 2:
            print(count)
            ScraperForHotel.find_url_for_cities(url)
        else:
            return

    @staticmethod
    def find_detail(url):
        """
        Find necessary informatiom about hotel and pack it into dict
        """
        url = ScraperForHotel.add_domen(url)
        tree = ScraperForHotel.request(url)
        detail = tree.xpath('//*[@id="hotel-description-panel-content"]/text()')
        contacts = tree.xpath('//span[@class="phone-img"]/text()')
        prices = tree.xpath('//table[@class="room-table"]/tr/td[2]/table/tr/td[2]/input/@value')
        rooms = tree.xpath('//table[@class="room-table"]/tr/td[2]/table/caption/text()')
        prices_for_rooms = dict(zip(rooms, prices))
        photo = tree.xpath('//div[@id="image_container"]/img/@src')
        name = tree.xpath('//span[@class="fn"]/text()')
        city = tree.xpath('//div[@class="hotel-line"]/a/span/strong/text()')
        adress = ScraperForHotel.parse_adress(tree.xpath('//div[@class="hotel-line"]/a/span/text()'))
        count = 0
        if all([detail, contacts, prices_for_rooms, photo, name, city, adress]) and count <= 2:
            data = {}
            data['detail'] = detail[0].strip().replace('\n', '').replace('  ', '')
            data['contacts'] = contacts[0]
            data['prices'] = prices_for_rooms
            data['photo'] = 'https:' + photo[0]
            data['hotel_name'] = name[0]
            data['city'] = city[0]
            data['adress'] = adress
            return data
        elif any([detail, contacts, prices_for_rooms, photo, name, city, adress]) and count <= 2:
            count += 1
            ScraperForHotel.find_detail(url)
        else:
            return

    def find_city_url(self, url):
        """
        Find the appropriate url for the searched city
        """
        url_for_all_cities = ScraperForHotel.find_url_for_cities(url)
        tree = self.request(url_for_all_cities)
        cities = tree.xpath(
            '//div[@class="catalog-name-region"]/following-sibling::ul/li/a[@class="regionSmallReg"]/text()')
        hrefs = tree.xpath(
            '//div[@class="catalog-name-region"]/following-sibling::ul/li/a[@class="regionSmallReg"]/@href')
        for index, city in enumerate(cities):
            if city == self.city:
                return ScraperForHotel.add_domen(hrefs[index])
        else:
            raise CityNotExists("Such city doesn't exist")

    @staticmethod
    def find_urls_for_hotels_in_city(url):
        """
        Find the list of urls for the hotels
        """
        tree = ScraperForHotel.request(url)
        amount = len(tree.xpath('//div[@class="hotel-container "]'))
        hrefs = tree.xpath('//div[@class="hotel-container "]/div[1]/div[2]/a[1]/@href')
        amount = amount if amount <= 100 else 100
        return hrefs[:amount]

    def parse(self):
        """
        Get around urls for hotels and return json with detail info for hotels
        """
        start = time.perf_counter()
        urls = ScraperForHotel.find_urls_for_hotels_in_city(self.find_city_url(ScraperForHotel.URL))
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as p:
            data = list(p.map(self.find_detail, urls))
        end = time.perf_counter()
        print(end - start)
        return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    city = 'Киев'
    ScraperForHotel(city).parse()
