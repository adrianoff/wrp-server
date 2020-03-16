from bs4 import BeautifulSoup
import requests
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrp_server.settings')

import django
django.setup()

from core.models import Picture, Painter

BASE_URL = 'https://gallerix.ru'

painters_urls = [
    #'https://google.com'
    'https://gallerix.ru/album/aivazovsky'
]


headers = {
    'Host': 'gallerix.ru',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,uk;q=0.5'
}

for painter_url in painters_urls:
    req = requests.get(painter_url, headers=headers, verify=False)

    if req.status_code != 200:
        continue

    soup = BeautifulSoup(req.content, 'html.parser')
    painter_name = str(soup.find('b', itemprop='name').contents[0])

    try:
        painter_object = Painter.objects.get(url=painter_url)
    except Painter.DoesNotExist:
        painter_object = Painter()
        painter_object.name = painter_name
        painter_object.url = painter_url
        painter_object.save()

    divs = soup.find_all("div", class_="pic")

    for div in divs[0:20]:
        picture_link = BASE_URL + div.find('a')['href']
        try:
            picture_object = Picture.objects.get(link_info=picture_link)
            continue
        except Painter.DoesNotExist:
            req = requests.get(picture_link, headers=headers, verify=False)
            soup = BeautifulSoup(req.content, 'html.parser')

            picture_name = str(soup.find('h1', class_='panel-title').contents[0])
