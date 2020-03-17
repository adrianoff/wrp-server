from bs4 import BeautifulSoup
import requests
import os
import uuid

from django.core.files import File

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
        except Picture.DoesNotExist:
            req = requests.get(picture_link, headers=headers, verify=False)
            soup = BeautifulSoup(req.content, 'html.parser')

            picture_name = str(soup.find('h1', class_='panel-title').contents[0])

            file_url = BASE_URL + soup.find('a', class_='sui font-weight-400 font-size-16')['href']
            filepath = 'static/pictures/' + uuid.uuid4().hex[:6].lower() + '.jpeg'
            with open(filepath, "wb") as file:
                new_headers = headers.copy()
                new_headers['Referer'] = picture_link
                new_headers['Sec-Fetch-Mode'] = 'navigate'
                new_headers['Sec-Fetch-Site'] = 'same-origin'
                response = requests.get(file_url, headers=new_headers, verify=False)
                soup = BeautifulSoup(response.content, 'html.parser')

                new_headers['Cookie'] = 'LOC=6%3ARU; _ym_uid=1584193274307759205; _ym_d=1584193274; _ga=GA1.2.1316766645.1584193275; marker=qoshppbs1u9cdu4pbkdhhav6p3; _fbp=fb.1.1584193335644.763158178; __gads=ID=1a20c5ae5e2af1b2:T=1584193335:S=ALNI_Mb_geQU23L3XbyDT6Z_Iu6IQdfUjQ; __utmz=63997296.1584193347.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fid=6218156f-a46e-438f-a9c5-2de16cce6cc5; PHPSESSID=baf6949b24f2c14cc851cca346d422a6; _gid=GA1.2.67504545.1584389092; _ym_isad=2; _ym_visorc_253414=w; __utma=63997296.1316766645.1584193275.1584193347.1584475219.2; __utmc=63997296; __utmb=63997296.5.10.1584475219; _ym_wasSynced=%7B%22time%22%3A1584475551446%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; _ym_visorc_62733=w'
                link = 'https:' + soup.find('a')['href']
                response = requests.get(link, headers=new_headers, verify=False)

                file.write(response.content)
                file.close()

            picture_object = Picture()
            picture_object.name = picture_name
            picture_object.painter = painter_object
            picture_object.link_info = picture_link
            picture_object.file = filepath
            picture_object.save()
