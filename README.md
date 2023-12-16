## What is this?

it is a cli parser to collect data from yandex dzen

## How to install

+ Clone the repo

+ Install virtual environment
  + python3.10 -m venv venv
  + venv/bin/activate (for Linux)
  + .\venv\Scripts\activate (for Windows)

+ Install dependencies: pip install -r requierements

+ Migrate databas: alembic upgrade head

## How to use

+ To parse all categories and all articles, you shoud use:
  
   + python manage.py fetch_group 

+ To choose categories you want to parse use:

  + python manage.py fetch_group --categories Интересное, Екатеринубрг   

+ To parse only one category you should use:
   
   + python manage.py fetch_category --category Спорт

You can set timer to parse yandex dzen every hour/ten hours/day etc. Default value of the timer is an hour. Use the following options to change the timer:

+ python manage.py fetch_group --categories Интересное, Екатеринубрг --set_timer 24 

Now the parser starts every 24 hours  


## How it works


![](https://github.com/iriskin77/Parser-yandex-data/blob/master/manage_parser.png)

![](https://github.com/iriskin77/Parser-yandex-data/blob/master/yandex_parser.png)
