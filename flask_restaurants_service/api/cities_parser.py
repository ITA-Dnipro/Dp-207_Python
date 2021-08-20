from bs4 import BeautifulSoup
import requests


URL = 'http://tomato.ua'
HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }


def get_content(params=''):
    response = requests.get(URL, headers=HEADERS, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find('div', class_='mein_header_form_loc location_select location_select__main').find_all('option')
    content = []
    for item in items:
        content.append((item.attrs['value'], item.text.strip()))
    

    return content


if __name__ == "__main__":
    result = get_content()
    print(result)