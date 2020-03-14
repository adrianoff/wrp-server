from bs4 import BeautifulSoup
import requests

painters_urls = [
    #'https://google.com'
    'https://gallerix.ru/album/aivazovsky'
]


#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for painter_url in painters_urls:
    req = requests.get(painter_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.a['animsition-link']