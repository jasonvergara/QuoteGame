import requests
from bs4 import BeautifulSoup


def scraped_quotes(base_url, url):
    data = []
    while url:
        r = requests.get(f"{base_url}{url}")
        soup = BeautifulSoup(r.text, "html.parser")
        quotes = soup.find_all('div', {'class': 'quote'})

        for quote in quotes:
            data.append({'quote': quote.find(class_='text').text.encode('ascii', 'ignore').decode('utf-8'),
                         'author': quote.find(class_='author').text,
                         'link': quote.find('a')['href']})

        next_button = soup.find('li', {'class': 'next'})
        url = next_button.find('a')['href'] if next_button else None

    return data

