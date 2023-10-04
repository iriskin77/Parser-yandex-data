from bs4 import BeautifulSoup
import requests
import lxml
from pymystem3 import Mystem
import asyncio
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import json

headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'news_lang=ru; yandex_login=talcore; ys=udn.cDrQktC70LDQtNC40YHQu9Cw0LIg0JrQsNGA0L/QtdC90LrQvg%3D%3D#c_chck.3181849896; yandexuid=7355079031598165761; mda2_beacon=1672991591886; gdpr=0; _ym_uid=1668166334590200044; addruid=J16Al8s1i5J74M9S9pL5k1W1f9; Session_id=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.bRabFjTPl-KB0YFwm7thxr4P1Eg; sessionid2=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.fakesign0000000000000000000; tmr_lvid=25aa36deb66ec3f5fd31de74352c56df; tmr_lvidTS=1665515375244; _ym_d=1693207925; Zen-User-Data={%22zen-theme%22:%22light%22}; zen_sso_checked=1; rec-tech=true; _ym_isad=1; KIykI=1; crookie=GwkL3T35JZAFN7/LgkLy5B06+N//nBiHRavbYemTc3SQ283H5odlLAaFAbEviWDO04s3S8SNGtCpq/kPhcdHkItBFYI=; cmtchd=MTY5NjMwODI2NzIwOQ==; _yasc=NEEDPcWQa1OaQo640rfL6v+8e9D3HVcXi8nYWOEebBJActfjCMY2F5mAmVGLC8g6; bltsr=1; tmr_detect=1%7C1696312690921',
        'Host': 'dzen.ru',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows"
    }


headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

url = 'https://dzen.ru/news?issue_tld=ru'

class Parser:

     json_articles_row = []
     #check_list = ('игра', "сыграть", "проиграть", "поиграть", "отыграть", "переиграть")
     index = 1

     def get_links_cards(self, main_url, headers):

         """"Функция получает ссыки на все новости со страницы"""""

         response = requests.get(url=main_url, headers=headers)
         response.encoding = 'utf-8'
         soup = BeautifulSoup(response.text, 'html.parser')
         res = soup.find_all('a', class_='mg-card__link')
         links = [i['href'] for i in res]
         return links

     async def get_words(self, session, link, headers):

         """"Функция собирает все слова со всех новостей в двумерный массив, который определен как res в классе Parser"""""

         retry_options = ExponentialRetry(attempts=5)
         retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)
         ua = UserAgent()
         fake_ua = {'user-agent': ua.random}
         async with retry_client.get(url=link, headers=headers2) as response:
             if response.ok:

                 resp = await response.text()
                 link_card = BeautifulSoup(resp, 'lxml')

                 # Получаем текст заголовка
                 header_article = link_card.find('a', class_='mg-story__title-link')


                 # Получаем основной текст статьи
                 body_article = link_card.find('div', class_='mg-snippets-group__body').find_all(class_='mg-snippet__text')
                 text = [i.text for i in body_article]

                 #Сохраняем тексты в списка, чтобы потом сохранить в файл в формате json

                 self.json_articles_row.append({
                     'index' : self.index,
                     'title' : header_article.text,
                     'body' : text
                 })

                 self.index += 1

     async def main(self, list_link):
         ua = UserAgent()
         fake_ua = {'user-agent': ua.random}

         async with aiohttp.ClientSession(headers=fake_ua) as session:
             tasks = []
             for link in list_link:
                 task = asyncio.create_task(self.get_words(session=session, link=link, headers=fake_ua))
                 tasks.append(task)
             await asyncio.gather(*tasks)

         # Здесь сохраняются тексты
         with open(r'texts_row.json', 'w', encoding='utf-8') as file_json:
             json.dump(self.json_articles_row, file_json, indent=4, ensure_ascii=False)

     def __call__(self, url_yandex, headers, *args, **kwargs):
         links = self.get_links_cards(url_yandex, headers)
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
         asyncio.run(self.main(links))


if __name__ == '__main__':

    obj = Parser()
    res = obj(url, headers2)









