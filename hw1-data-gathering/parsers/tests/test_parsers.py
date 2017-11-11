import os
import unittest
from abc import ABC, abstractmethod

from parsers.booking_catalog_parser import BookingCatalogParser
from parsers.booking_hotel_parser import BookingHotelParser
from parsers.proxy_catalog_parser import ProxyCatalogParser


class TestParser(ABC, unittest.TestCase):
    def setUp(self):
        base_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(base_path, self.get_response_file_path()), 'r') as r:
            self._parser = self.init_parser(r.read())

    @abstractmethod
    def init_parser(self, html):
        """Returns response handler"""

    @abstractmethod
    def get_response_file_path(self):
        """Returns path to response file"""


class TestBookingCalalogParser(TestParser):
    def test_catalog_links(self):
        expected = ['https://booking.com/hotel/ru/paradiseotel-moskva1234.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/standart-hotel.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/savoy.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/mezhdunarodnaya-2.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/hb-central-superior-apartments.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/metropolis-moscow.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/smart-apartments-in-historical-center.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/ministry-suite-smolenskaya.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/morion.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/gorodm-apartment-on-tsvetnoy-boulevard.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/3-room-apartment-on-smolensky-boulevard.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/lakshmi-apartament-belorusskaya.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/apartments-nice-arbat-4-rooms.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/apartment-on-smolenskaya-naberezhnaya-5-47-3.ru.html#hotelTmpl',
                    'https://booking.com/hotel/ru/kudrinskaya-1-apartment.ru.html#hotelTmpl'
                    ]

        actual = self._parser.catalog_links()

        self.assertEqual(expected, actual)
        self.assertEqual(15, len(actual))

    def init_parser(self, html):
        return BookingCatalogParser(html)

    def get_response_file_path(self):
        return 'responses/booking_catalog_response.html'


class TestProxyCalalogParser(TestParser):
    def test_proxy_ips(self):
        expected = ['186.94.46.203:8080', '54.169.9.27:8080', '94.23.56.95:8080', '180.251.56.84:3128',
                    '118.97.29.203:80', '66.70.191.5:3128', '5.196.189.50:8080', '167.205.6.6:80',
                    '85.235.188.194:8080', '198.50.219.232:8080', '194.14.207.87:80', '107.170.243.244:80',
                    '82.64.24.52:80', '52.40.59.11:80', '92.222.74.221:80', '37.187.116.199:80', '54.37.13.33:80',
                    '91.121.88.53:80', '111.13.109.27:80', '158.69.197.236:80', '74.208.110.38:80', '64.34.21.84:80',
                    '92.38.47.239:80', '173.212.202.65:80', '163.172.215.220:80', '52.57.95.123:80', '104.197.98.54:80',
                    '18.220.146.56:80', '51.15.160.216:80', '168.128.29.75:80', '95.85.50.218:80', '35.187.81.58:80',
                    '212.83.164.85:80', '176.31.50.61:80', '94.177.175.232:80', '52.163.62.13:80', '146.148.33.10:80',
                    '202.159.36.70:80', '35.202.22.18:80', '52.174.89.111:80', '115.70.186.106:8080',
                    '137.74.254.242:3128', '192.158.236.57:3128', '163.172.217.103:3128', '162.223.91.18:3128',
                    '165.227.53.107:3128', '54.36.182.96:3128', '195.154.163.181:3128', '89.236.17.106:3128',
                    '122.3.29.175:53281']

        actual = self._parser.proxy_ips()

        self.assertEqual(expected, actual)
        self.assertEqual(50, len(actual))

    def init_parser(self, html):
        return ProxyCatalogParser(html)

    def get_response_file_path(self):
        return 'responses/proxies_catalog_response.html'


class TestBookingHotelParser(TestParser):
    def test_title(self):
        self.assertEqual('Савой', self._parser.title())

    def test_stars(self):
        self.assertEqual(5.0, self._parser.stars())

    def test_rating(self):
        self.assertEqual(8.9, self._parser.rating())

    def test_reviews_count(self):
        self.assertEqual(1724, self._parser.reviews_count())

    def test_the_year_of_the_beginning_on_the_booking(self):
        self.assertEqual(2009, self._parser.the_year_of_the_beginning_on_the_booking())

    def test_has_free_wifi(self):
        self.assertTrue(self._parser.has_free_wifi())

    def test_gallery_images(self):
        expected1 = ['https://s-ec.bstatic.com/images/hotel/max500/792/79223335.jpg',
                     'https://s-ec.bstatic.com/images/hotel/square60/142/14250861.jpg',
                     'https://t-ec.bstatic.com/images/hotel/square60/788/78889717.jpg',
                     'https://s-ec.bstatic.com/images/hotel/square60/788/78889801.jpg',
                     'https://s-ec.bstatic.com/images/hotel/square60/142/14250861.jpg']

        expected2 = ['https://t-ec.bstatic.com/images/hotel/square60/174/17476127.jpg',
                     'https://t-ec.bstatic.com/images/hotel/square60/922/92234237.jpg',
                     'https://t-ec.bstatic.com/images/hotel/square60/371/37108343.jpg',
                     'https://t-ec.bstatic.com/images/hotel/square60/508/50819641.jpg',
                     'https://t-ec.bstatic.com/images/hotel/square60/174/17476127.jpg']

        images = self._parser.gallery_images()
        self.assertEqual(33, len(images))
        self.assertEqual(expected1, images[:5])
        self.assertEqual(expected2, images[-5:])

    def test_address(self):
        self.assertEqual('Улица Рождественка 3/6 стр.1, Мещанский, Москва, Россия', self._parser.address())

    def test_hotel_summary(self):
        text = 'Элегантный отель «Савой» с классической итальянской мебелью расположен менее чем в 10 минутах ходьбы от Кремля. К услугам гостей роскошные номера и крытый бассейн. Гостям отеля предлагается размещение в номерах и люксах с ортопедическими матрасами и гипоаллергенными подушками, бесплатным Wi-Fi и отделанной мрамором ванной комнатой с полом с подогревом. Гости могут поплавать в бассейне и отдохнуть в сауне, а также посетить салон красоты. Гости могут отведать превосходные блюда местной и европейской кухни в ресторане Savoy. На круглосуточной стойке регистрации можно получить информацию об экскурсиях и билетах. Дружелюбный и профессиональный персонал говорит на английском языке.'
        self.assertEqual(text, self._parser.hotel_summary())

    def test_district_summary(self):
        text = 'Мещанский — отличный выбор, если вам интересны культура, история и музеи.'
        self.assertEqual(text, self._parser.district_summary())

    def test_reviews_summary(self):
        text = 'Расположение этого варианта — одно из лучших в Москве! Гости довольны им больше, чем расположением других вариантов в этом районе. Парам особенно нравится расположение — они оценили проживание в этом районе для поездки вдвоем на 9,6. Здесь лучшее соотношение цены и качества в Москве! По сравнению с другими вариантами в этом городе, гости получают больше за те же деньги.'
        self.assertEqual(text, self._parser.reviews_summary())

    def test_geo_summary(self):
        text = 'Это любимая часть города Москва среди наших гостей согласно независимым отзывам.'
        self.assertEqual(text, self._parser.geo_summary())

    def init_parser(self, html):
        return BookingHotelParser(html)

    def get_response_file_path(self):
        return 'responses/savoy.ru.html'
