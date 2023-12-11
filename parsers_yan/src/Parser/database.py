import sqlalchemy as db
from sqlalchemy import select
from parsers_yan.src.Parser.models import Category, Article, Base
from sqlalchemy.orm import sessionmaker
from parsers_yan.src.Parser.config import settings



# Сделать нормальную таблицу и сделать одну функцию, в которую будет попадать json, и далее все записывается в таблицу

class Database:

    sqlite_db_path = settings.DATABASE_URL_sqlite()

    sync_engine = db.create_engine(url=sqlite_db_path, echo=True)
    session = sessionmaker(autoflush=False, bind=sync_engine)

    def create_table(self):
        #Base.metadata.drop_all(bind=self.sync_engine)
        Base.metadata.create_all(bind=self.sync_engine)

    def insert_categories(self, json_articles):

        with self.session(autoflush=False, bind=self.sync_engine) as sess:
            for name_section in json_articles:
                name = sess.query(Category).filter_by(name_category=name_section).first()
                if name is None:
                    data_section = Category(name_category=name_section)
                    sess.add(data_section)
            sess.commit()

    def insert_articles(self, json_articles):

        with self.session(autoflush=False, bind=self.sync_engine) as sess:
            for name_section in json_articles:
                for article in json_articles[name_section]:
                     print(article)
                     title = article['title']
                     body = article['body']
                     link_dzen = article['link_dzen']
                     link_source = article['link_source']
                     date_parse = article['date_parse']
                     fk = sess.query(Category).filter_by(name_category=name_section).one().id
                     if fk is not None:
                         data = Article(category_id=fk, title=title, body=body, link_dzer=link_dzen, link_source=link_source, time_parse=date_parse)
                         sess.add(data)
            sess.commit()

    def select_data(self):
        with self.session(autoflush=False, bind=self.sync_engine) as sess:
            query = select(Category.name_category)
            res = sess.execute(query).fetchall()
            for i in res:
                print(i)



db = Database()
db.create_table()





