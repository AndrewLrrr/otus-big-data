"""
Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .


ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью выше)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

"""

import logging
import sys
import pandas as pd

from parsers.booking_hotel_parser import BookingHotelParser
from scrappers.booking_scrapper import BookingScrapper
from scrappers.proxy_scrapper import ProxyScrapper
from storages.file_storage import FileStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRAPPED_STORAGE = 'booking'
TABLE_FORMAT_FILE = 'data.csv'
LIMIT = 1200


def gather_process(use_proxy):
    logger.info("gather")
    storage = FileStorage(SCRAPPED_STORAGE)
    proxy = ProxyScrapper() if use_proxy else None
    scrapper = BookingScrapper(proxy, storage)

    if scrapper.scrap_process(limit=LIMIT):
        logging.error('Success booking.com hotels scraping')
    else:
        logging.error('Failed booking.com hotels scraping')


def convert_data_to_table_format():
    logger.info("transform")
    storage = FileStorage(SCRAPPED_STORAGE)
    hotels = storage.keys()
    with open(TABLE_FORMAT_FILE, encoding='utf-8', mode='w') as csv_file:
        titles = []
        stars = []
        ratings = []
        reviews_counts = []
        have_free_wifi = []
        gallery_images_counts = []
        addresses = []
        start_years = []
        good_districts = []

        for hotel in hotels:
            parser = BookingHotelParser(storage.get(hotel))
            titles.append(parser.title())
            stars.append(parser.stars())
            ratings.append(parser.rating())
            reviews_counts.append(parser.reviews_count())
            have_free_wifi.append(parser.has_free_wifi())
            gallery_images_counts.append(len(parser.gallery_images()))
            addresses.append(parser.address())
            start_years.append(parser.the_year_of_the_beginning_on_the_booking())
            good_districts.append(parser.geo_summary() is not None)

        df = pd.DataFrame({
            'name': titles,
            'stars': stars,
            'rating': ratings,
            'reviews_count': reviews_counts,
            'has_free_wifi': have_free_wifi,
            'gallery_images_count': gallery_images_counts,
            'address': addresses,
            'start_year': start_years,
            'good_district': good_districts,
        })

        df.to_csv(csv_file, encoding='utf-8')


def stats_of_data():
    logger.info("stats")

    def get_district_from_address(addr):
        items = addr.split(',')
        if len(items) < 4:
            return None
        elif len(items) == 4 and not any(char.isdigit() for char in items[1]):
            return items[1].strip()
        elif len(items) == 5 and not any(char.isdigit() for char in items[2]):
            return items[2].strip()
        return None

    try:
        df = pd.read_csv(TABLE_FORMAT_FILE)
        print('~~ Исследование отелей Москвы ~~')
        print()

        print('Описание данных:')
        print(df.info())
        print()

        print('Распределение отелей по году начала присутствия на booking.com:')
        df2 = df.copy().dropna(subset=['start_year'])
        print(df2.groupby(['start_year'])['start_year'].agg(['count']).sort_values('count', ascending=False))
        print()

        print('Привлекательные районы по мнению туристов:')
        df3 = df.copy().dropna(subset=['address', 'good_district'])[['address', 'good_district']]
        df3.address = df3.address.apply(get_district_from_address)
        print(df3.dropna(subset=['address']).drop_duplicates().loc[df3.good_district == True].sort_values('address'))
        print()

        print('Непривлекательные районы по мнению туристов:')
        good_districts = df3.dropna(subset=['address']).drop_duplicates().loc[df3.good_district == True]['address'].values
        print(df3[~df3['address'].isin(good_districts)].dropna(subset=['address']).drop_duplicates().sort_values('address'))
        print()

        print('Процент наличия бесплатного Wi-fi в отелях:')
        print(
            (100 / df.dropna(subset=['has_free_wifi'])['has_free_wifi'].count()) \
            * df.dropna(subset=['has_free_wifi']).loc[df.has_free_wifi == True]['has_free_wifi'].count()
        )
        print()

        print('Распределение по звездам:')
        df['stars'].fillna(0, inplace=True)
        print(df.groupby(['stars'])['stars'].agg(['count']).sort_values('count'))
        print()

        print('Средний рейтинг отеля в распределении по звездам:')
        df4 = df.dropna(subset=['rating'])[['rating', 'stars']]
        print(df4.groupby('stars')['rating'].mean())
        print()

        print('Распределение отелей по районам:')
        print(df3.dropna(subset=['address'])
              .groupby(['address'])['address']
              .agg(['count'])
              .sort_values('count', ascending=False))
    except FileNotFoundError as e:
        logger.error(e)


if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        try:
            use_proxy = (sys.argv[2] == 'proxy')
        except IndexError:
            use_proxy = False
        gather_process(use_proxy)

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
