## What is this?

it is a cli parser to collect news from yandex dzen

## How to install

+ Clone the repo

+ Install virtual environment
  + python3.10 -m venv venv
  + venv/bin/activate (for Linux)
  + .\venv\Scripts\activate (for Windows)

+ Install dependencies: pip install -r requierements

+ Migrate databas: alembic upgrade head

## How to use

+ To parse all categories and all news you shoud use:
  
   + python manage.py fetch_group 

+ To choose only categories you want to parse use --categories. For example:

  + python manage.py fetch_group --categories Интересное, Екатеринубрг   

+ To parse only one category you should use:
   
   + python manage.py fetch_category --category Спорт

You can set timer to parse yandex dzen every hour/ten hours/day etc. Default value of the timer is an hour. Use the following options to change the timer --set_timer. For example:

+ python manage.py fetch_group --categories Интересное, Екатеринубрг --set_timer 24 

Now the parser starts every 24 hours  


## How it works


![](https://github.com/iriskin77/Parser-yandex-data/blob/master/manage_parser.png)

#### The parser that collects news from a group of categories

![](https://github.com/iriskin77/Parser-yandex-data/blob/master/images/ParserGroupCategories.png)

#### The parser that collects news from only one category

![](https://github.com/iriskin77/Parser-yandex-data/blob/master/images/ParserSingleCategory.png)


## Notes

If you have read up to this point, you may have realized that this structure/architecture is too complex for parsing a site like yandex zen (at least, I think so). I suppose it would have been enough to create two small classes, or even several functions in order to complete the task. But I sincerely wanted to complicate this project using mixins, cli and other features. Just for fun and for practice :)
