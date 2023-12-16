import time
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from parser_ydzen.parser.services.logs import init_logger


class CollectLinksMixin:

    logger = init_logger(__name__)

    def _collect_links_categories(
            self, main_url: str, headers: dict, categories_choice=None) -> dict:

        try:
            self.logger.info(f"Fn: {self._collect_links_categories.__name__}. Collecting links of categories has started")

            dct = {}
            response = requests.get(url=main_url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            sections = soup.find(
                'div', class_='base-scroll__contentContainer-2m base-tabs__tabsContainer-15').find_all(
                'a', class_='tab__tab-24 link-button__rootElement-32 base-button__rootElement-75 base-button__m-3E base-button__regular-1v'
            )
            links_section = [link['href'] for link in sections]
            for index in range(len(sections)):
                name_section = sections[index].find('span', class_='base-button__childrenContent-1L').text
                link_section = links_section[index]
                if categories_choice is not None:
                    if name_section in categories_choice:
                        dct[name_section] = link_section
                else:
                    dct[name_section] = link_section
            return dct

        except Exception as ex:
            self.logger.critical(f"Fn: {self._collect_links_categories.__name__}. Failed to collect links of categories from yandex dzen. Message error: {ex}")


    def _collect_links_cards(self, section_links: dict, headers) -> dict:
        """"Output: { name1 : [link1, link2] , name2 : [link1, link2] ...}"""""
        try:
            self.logger.info(f"Fn: {self._collect_links_cards.__name__}. Collecting links of cards has started")

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

        except Exception as ex:
            self.logger.critical(f"Fn: {self._collect_links_cards.__name__}. Failed to collect links of cards with articles from yandex dzen. Message error: {ex}")


class RetrieveArticleInfoMixin:

    logger = init_logger(__name__)

    async def get_info_article(self, session, link_article, name_section, headers):

        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(
                       raise_for_status=False,
                       retry_options=retry_options,
                       client_session=session,
                       start_timeout=0.5)

        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        # proxy=r'https://217.29.63.202:10448'

        try:

            async with retry_client.get(url=link_article, headers=fake_ua) as response:
                if response.ok:

                    resp = await response.text()
                    link_card = BeautifulSoup(resp, 'lxml')

                    header_article = link_card.find(
                        'a', class_='mg-story__title-link').get_text(strip=True)
                    body_article = link_card.find(
                        'div',
                        class_='mg-story-summarization mg-story-summarization_teaser-type_first mg-story-summarization_has-bullets').text
                    source_link = link_card.find(
                        'a', class_='mg-story__title-link')['href']
                    time_parse = str(date.today())

                # Сохраняем тексты в списка, чтобы потом сохранить в файл в
                # формате json

                    self.res_dict[name_section].append({
                        'title': header_article,
                        'body': body_article,
                        'link_dzen': link_article,
                        'link_source': source_link,
                        'date_parse': time_parse
                    })

        except Exception as ex:
            self.logger.critical(f"Fn: {self.get_texts.__name__}. Failed to retrieve the article from yandex dzen. Message error: {ex}")

