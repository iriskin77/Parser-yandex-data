import sqlalchemy as db
from sqlalchemy import select
from parser_ydzen.parser.models import Category, Article, Base
from sqlalchemy.orm import sessionmaker
from parser_ydzen.parser.services.config import settings
from parser_ydzen.parser.services.logs import init_logger


class Database:

    sqlite_db_path = settings.DATABASE_URL_sqlite
    sync_engine = db.create_engine(url=sqlite_db_path, echo=True)
    session = sessionmaker(autoflush=False, bind=sync_engine)

    def __init__(self):
        self.logger = init_logger(__name__)

    def create_table(self):
        # Base.metadata.drop_all(bind=self.sync_engine)
        Base.metadata.create_all(bind=self.sync_engine)

    def insert_categories(self, json_articles):

        with self.session(autoflush=False) as sess:
            try:
                self.logger.info(f"Fn: {self.insert_categories.__name__}. Starting to insert categories the table")
                for name_section in json_articles:
                    name = sess.query(Category).filter_by(name_category=name_section).first()
                    if name is None:
                        data_section = Category(name_category=name_section)
                        sess.add(data_section)

                sess.commit()
                self.logger.info(
                    f"Fn: {self.insert_categories.__name__}. Categories were inserted successfully")

            except Exception as ex:
                self.logger.critical(f"Fn: {self.insert_categories.__name__}. Failed to insert categories into db. Message error: {ex}")


    def insert_articles(self, json_articles):

        with self.session(autoflush=False) as sess:
            try:
                self.logger.info(f"Fn: {self.insert_categories.__name__}. Starting to insert articles into the table")
                print('json_articles', type(json_articles))
                for name_section in json_articles:
                    print('NAME_SECTION', name_section)
                    for article in json_articles[name_section]:

                        title = article['title']
                        print('title', title)
                        body = article['body']
                        link_dzen = article['link_dzen']
                        link_source = article['link_source']
                        date_parse = article['date_parse']
                        fk = sess.query(Category).filter_by(name_category=name_section).one().id
                        title_check = sess.query(Article).filter_by(title=title).one()
                        print('TITLE_CHECK', title_check)
                        if fk is not None:
                            if title_check is None:
                                data = Article(category_id=fk, title=title, body=body, link_dzer=link_dzen, link_source=link_source, time_parse=date_parse)
                                sess.add(data)
                    sess.commit()
                self.logger.info(f"Fn: {self.insert_categories.__name__}. Articles were inserted successfully")

            except Exception as ex:
                self.logger.critical(f"Fn: {self.insert_articles.__name__}. Failed to insert articles into db. Message error: {ex}")
