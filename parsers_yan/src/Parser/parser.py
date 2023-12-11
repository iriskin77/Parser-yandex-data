import time
import lxml
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from parsers_yan.src.Parser.headers import headers
from selenium import webdriver
from datetime import date


class Parser:

     res_dict: dict = {}

     def test_func(self):
         with webdriver.Chrome() as driver:
             driver.get("https://freelance.habr.com/tasks/221239")


     def get_links_section(self, main_url: str, headers: dict) -> dict:
         dct = {}
         response = requests.get(url=main_url, headers=headers)
         response.encoding = 'utf-8'
         soup = BeautifulSoup(response.text, 'html.parser')
         sections = soup.find('div', class_='base-scroll__contentContainer-2m base-tabs__tabsContainer-15').find_all('a', class_='tab__tab-24 link-button__rootElement-32 base-button__rootElement-75 base-button__m-3E base-button__regular-1v')
         links_section = [link['href'] for link in sections]
         for index in range(len(sections)):
             name_section = sections[index].find('span', class_='base-button__childrenContent-1L').text
             link_section = links_section[index]
             dct[name_section] = link_section
         return dct


     def get_links_cards(self, section_links: dict, headers) -> dict:

         """"Функция получает ссыки на все новости со страницы, name : [link1, link2]"""""
         dct = {}
         for item in section_links.items():
             name = item[0]
             url_section = item[1]

             with webdriver.Firefox() as driver:
                 driver.get(url_section)
                 page_height = driver.execute_script("return document.body.scrollHeight")
                 window_height = driver.execute_script("return window.innerHeight")
                 num_scroll = page_height // window_height
                 lst_category_links = []

                 for _ in range(num_scroll):
                     time.sleep(8)
                     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                     time.sleep(4)
                     links_section = driver.find_elements(By.CLASS_NAME, "mg-card__link")
                     links_section_clear = [i.get_attribute("href") for i in links_section]
                     for link in links_section_clear:
                         lst_category_links.append(link)

                 dct[name] = lst_category_links


         return dct


     async def get_texts (self, session, link_article, name_section, headers):

         """"Функция собирает заголовок текста и основное содержание и кладет в словарь с ключами title и body"""""

         retry_options = ExponentialRetry(attempts=5)
         retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)
         ua = UserAgent()
         fake_ua = {'user-agent': ua.random}
         # proxy=r'https://217.29.63.202:10448'
         async with retry_client.get(url=link_article, headers=fake_ua) as response:
             if response.ok:

                 resp = await response.text()
                 link_card = BeautifulSoup(resp, 'lxml')

                 header_article = link_card.find('a', class_='mg-story__title-link').get_text(strip=True)
                 body_article = link_card.find( 'div', class_='mg-story-summarization mg-story-summarization_teaser-type_first mg-story-summarization_has-bullets').text
                 source_link = link_card.find('a', class_='mg-story__title-link')['href']
                 time_parse = str(date.today())


                 #Сохраняем тексты в списка, чтобы потом сохранить в файл в формате json

                 self.res_dict[name_section].append({
                     'title' : header_article,
                     'body' : body_article,
                     'link_dzen' : link_article,
                     'link_source' : source_link,
                     'date_parse' : time_parse
                 })

     async def main(self, dct_section_link):
         ua = UserAgent()
         fake_ua = {'user-agent': ua.random}

         async with aiohttp.ClientSession(headers=headers) as session:

             for item in dct_section_link.items():
                  tasks = []
                  name = item[0]
                  links_section = item[1]
                  self.res_dict[name] = []
                  for link_article in links_section:
                      task = asyncio.create_task(self.get_texts(session=session, link_article=link_article, name_section=name, headers=headers))
                      tasks.append(task)
                  await asyncio.gather(*tasks)











