from parsers_yan.src.Parser.database import Database
from parsers_yan.src.Parser.parser import Parser
from parsers_yan.src.Parser.headers import headers
import asyncio
import json


main_url = 'https://dzen.ru/news?issue_tld=ru'

def main():

    pars = Parser()

    my_db = Database()

    dct = pars.get_links_section(main_url=main_url, headers=headers)
    my_db.write_sql_section(dct)
    res = pars.get_links_cards(dct, headers=headers)
    my_db.insert_categories(res)
    my_db.insert_articles(res)

    # with open(r'links.json', 'r', encoding='utf-8') as links:
    #     a = json.load(links)
    #     asyncio.run(pars.main(a))
    #     res = pars.res_dict
    #     print(res)
    #     with open(r'texts_row9.json', 'a', encoding='utf-8') as file_json:
    #         json.dump(res, file_json, indent=4, ensure_ascii=False)

    # with open('texts_row9.json', 'r', encoding='utf-8') as file:
    #     a = json.load(file)
    #     my_db.insert_categories(a)
    #     my_db.insert_articles(a)

    #my_db.select_data()



    # with open(r'links.json', 'w', encoding='utf-8') as file_json:
    #     json.dump(res, file_json, indent=4, ensure_ascii=False)

    #print(res)

    #print(res)

    # asyncio.run(pars.main(d))
    # #json_articles
    # res = pars.res_dict
    # print(res)
    #
    # with open(r'texts_row8.json', 'w', encoding='utf-8') as file_json:
    #     json.dump(res, file_json, indent=4, ensure_ascii=False)

    #my_db.insert_categories(res)
    #my_db.insert_articles(res)

    # with open(r'texts_row.json', 'r', encoding='utf-8') as file_json:
    #     json_articles = json.load(file_json)
    #
    #     my_db.write_sql_texts(json_articles)

    # with Session(autoflush=False, bind=engine) as db:
    #     # получение всех объектов
    #     people = db.query(Article).all()
    #     for i in people:
    #         print(i.id, i.category_id, i.title, i.body)

if __name__ == '__main__':
    main()



