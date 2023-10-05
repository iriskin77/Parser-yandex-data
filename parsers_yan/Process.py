from pymystem3 import Mystem
import json
from nltk import pos_tag

class Process:


    json_texts_sorted = []
    words = []
    index = 1

    def lemmatize_texts(self, json_articles):
        """"Принимает на вход json файл с ключами title и body, далее проводит лемматизацию"""""

        print("Функция lemmatize_texts начала работу")
        # Лемматизируем заголовок статьи
        m = Mystem()
        # print(json_articles)
        for text in json_articles:
            # print('Переменная text из функции lemmatize_texts', text['title'])
            lemm_header_article = m.lemmatize(text['title'])
            lemm_header_words = [word for word in lemm_header_article if word.isalpha()]
            text['title'] = lemm_header_words

        for text in json_articles:
            # print('Переменная lemm_body', body)
            lemm_body = [m.lemmatize(sentence) for sentence in text['body']]
            text['body'] = lemm_body

        for text in json_articles:
            lemmatized_sentences = []
            for sentence in text['body']:
                lst = [word for word in sentence if word.isalpha()]
                lemmatized_sentences.append(lst)
            text['body'] = lemmatized_sentences

        print('Функция lemmatize_texts завершилась', json_articles)
        return json_articles

    def check_lemmatized_texts(self, json_articles):
        print("Функция check_lemmatized_texts начала работу")
        for text in json_articles:

                if ('игра' in text['title']) or ('игра' in text['body']):

                    self.json_texts_sorted.append({
                        'index': self.index,
                        'title': text['title'],
                        'body': text['body']
                    })

                    self.index += 1
                    text['body'].append(text['title'])
                    self.words.append(text['body'])

        #print('Переменная self.all_text', self.all_text)
        print('Функция check_lemmatized_texts завершилась', self.words)
        return self.words

    def make_onedim_array(self, list_article_words):

        """"Функция получает трехмерный массив из слов и превращает в одномерный массив из слов"""""

        print("Функция make_onedim_array начала работу")
        result = []

        for text in list_article_words:
            for sentence in text:
                for word in sentence:
                    result.append(word)
        print('Функция make_onedim_array завершилась', result)
        return result

    def count_words(self, list_words):

        """Функция считает топ 50 наиболее частотных слов"""""

        print("Функция count_words начала работу")
        dct_words = {}

        for word in list_words:
            if word in dct_words:
                dct_words[word] += 1
            else:
                dct_words[word] = 1

        # сортировка словаря по убыванию
        dct_sorted = sorted(dct_words.items(), key=lambda x: x[1], reverse=True)

        top_words = [word[0] for word in dct_sorted]

        if len(top_words) >= 50:
            top_words_text = ' '.join(top_words[:50])
            print('Переменная top_words_text, если > 50', top_words_text)
            return top_words_text
        elif 50 < len(top_words) > 0:
            top_words_text = ' '.join(top_words)
            print('Переменная, если < 50', top_words_text)
            return top_words_text
        elif len(top_words) <= 0:
            return 'Нет текстов со словом игра('

if __name__ == '__main__':

    obj = Process()

    """"Открываем файл с изначальными (необработанными) текстами, лемматизируем, выбираем из них те, в которых есть слова игра. 
    В один файл (top_words) кладем топ частотных слов из этих текстов, 
    в другой файл (texts_sorted) кладем лемматизированные тексты, в которых есть слово игра"""""

    with open(r'C:\Parser_yandex\texts_row.json', 'r', encoding='utf-8') as file_json, \
            open(r'C:\Parser_yandex\words.json', 'w', encoding='utf-8') as top_words, \
            open(r'C:\Parser_yandex\texts_sorted.json', 'w', encoding='utf-8') as texts_sorted:
        data_texts = json.load(file_json)
        lemmatized_text = obj.lemmatize_texts(data_texts)
        three_dim_array = obj.check_lemmatized_texts(lemmatized_text)
        words = obj.make_onedim_array(three_dim_array)
        result = obj.count_words(words)

        # топ слов по частотности в отсортированных текстах
        top_words.write(result)

        # файл с отсортированными лемматизированными текстами текстами
        json.dump(obj.json_texts_sorted, texts_sorted, indent=4, ensure_ascii=False)

    """Сравниваем лемматизированные тексты со словом игра из файла  texts_sorted со всеми изначальными (необработанными) текстами.
    Если есть совпадение, значит, в изначальном (необработанном) тексте есть слово игра. Кладем такой текст в отдельный файл (texts_games)"""

    with open(r'C:\Parser_yandex\texts_games.json', 'w', encoding='utf-8') as texts_games, \
        open(r'C:\Parser_yandex\texts_sorted.json', 'r', encoding='utf-8') as texts_sorted, \
        open(r'C:\Parser_yandex\texts_row.json', 'r', encoding='utf-8') as texts_row:
        data_row = json.load(texts_row)
        data_sorted = json.load(texts_sorted)

        for row_text in data_row:
            for sorted_text in data_sorted:
                if row_text['index'] == sorted_text['index']:
                    json.dump(row_text, texts_games, indent=4, ensure_ascii=False)






