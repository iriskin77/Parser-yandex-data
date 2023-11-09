from bs4 import BeautifulSoup
import requests
import lxml
from pymystem3 import Mystem
import asyncio
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import json
from Headers import headers

url = 'https://dzen.ru/news?issue_tld=ru'

class Parser:

     json_articles_row = []
     index = 1

     def get_links_cards(self, main_url, headers):

         """"Функция получает ссыки на все новости со страницы"""""

         response = requests.get(url=main_url, headers=headers)
         response.encoding = 'utf-8'
         soup = BeautifulSoup(response.text, 'html.parser')
         res = soup.find_all('a', class_='mg-card__link')
         links = [i['href'] for i in res]
         return links

     async def get_texts (self, session, link, headers):

         """"Функция собирает заголовок текста и основное содержание и кладет в словарь с ключами title и body"""""

         retry_options = ExponentialRetry(attempts=5)
         retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)
         ua = UserAgent()
         fake_ua = {'user-agent': ua.random}
         async with retry_client.get(url=link, headers=headers) as response:
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
                 task = asyncio.create_task(self.get_texts(session=session, link=link, headers=fake_ua))
                 tasks.append(task)
             await asyncio.gather(*tasks)

         # Здесь сохраняются тексты
         with open(r'C:\Parser_yandex\texts_row.json', 'w', encoding='utf-8') as file_json:
             json.dump(self.json_articles_row, file_json, indent=4, ensure_ascii=False)

     def __call__(self, url_yandex, headers, *args, **kwargs):
         links = self.get_links_cards(url_yandex, headers)
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
         asyncio.run(self.main(links))


if __name__ == '__main__':

    obj = Parser()
    res = obj(url, headers)









