import asyncio
import aiohttp
import argparse
from parser_ydzen.parser.services.config import headers
from parser_ydzen.parser.services.base import ManageParser
from parser_ydzen.parser.services.logs import init_logger
from parser_ydzen.parser.database import Database
from parser_ydzen.parser.services.utils import CollectLinksMixin, RetrieveArticleInfoMixin
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from datetime import datetime
from fake_useragent import UserAgent


class ParsGroupCategories(ManageParser,
                          CollectLinksMixin,
                          RetrieveArticleInfoMixin):

    command: str = 'fetch_group'
    url_main_page: str = 'https://dzen.ru/news?issue_tld=ru'
    res_dict: dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = Database()
        self.scheduler = BlockingScheduler()
        self.logger = init_logger(__name__)

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--categories',
            default=None,
            nargs='+',
            type=str,
            help='collecting categories from yandex dzen. Default: all categories',
        )

        parser.add_argument(
            '--set_timer',
            default=1,
            type=int,
            help='set timer. Default - an hour',
        )

    async def collect_info_articles(self, dct_section_link):

        # ua = UserAgent()
        # fake_ua = {'user-agent': ua.random}

        try:

            async with aiohttp.ClientSession(headers=headers) as session:
                self.logger.info(f"Fn: {self.collect_info_articles.__name__}. Starting to collect articles info")

                for item in dct_section_link.items():
                    self.logger.info(f"Fn: {self.collect_info_articles.__name__}. Category {item[0]} in process")
                    tasks = []
                    name = item[0]
                    links_section = item[1]
                    self.res_dict[name] = []
                    for link_article in links_section:
                        task = asyncio.create_task(self.get_info_article(
                               session=session,
                               link_article=link_article,
                               name_section=name,
                               headers=headers)
                        )
                        tasks.append(task)
                    await asyncio.gather(*tasks)
                    self.logger.info(f"Fn: {self.collect_info_articles.__name__}. Articles were collected successflly from the category {item[0]}")

        except Exception as ex:
            self.logger.critical(f"Fn: {self.collect_info_articles.__name__}. Failed to collect info articles. Message error: {ex}")

    def start_parser(self) -> None:

        try:
            self.logger.info(f"Fn: {self.start_parser.__name__}. Parser ParsGroupCategory has started")
            # Choose categories to parse
            categories_parse = self.init_kwargs['categories']
            #Collecting links of the categories we have choosen to parse
            links_categories = self._collect_links_categories(main_url=self.url_main_page,
                                                              headers=headers,
                                                              categories_choice=categories_parse)

            # Collecting links to articles of the categories we are parsing
            links_articles_cards = self._collect_links_cards(section_links=links_categories, headers=headers)
            # In async way we collect info from every card. As a result we have a file-json
            asyncio.run(self.collect_info_articles(links_articles_cards))

            # Insert Json into Sql
            self.database.insert_categories(self.res_dict)
            self.database.insert_articles(self.res_dict)

            self.logger.info(f"Fn: {self.start_parser.__name__}. Parser ParsGroupCategory has finished correctly")

        except Exception as ex:
            self.logger.critical(f"Fn: {self.start_parser.__name__}. Failed to work the parser. Message error: {ex}")


    def execute(self) -> None:
        super().execute()

        timer = self.init_kwargs['set_timer']
        start = self.scheduler.add_job(self.start_parser, 'interval', hours=timer)

        for job in self.scheduler.get_jobs():
            job.modify(next_run_time=datetime.now())

        self.scheduler.start()
