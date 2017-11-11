import logging
import re
import requests
import time

from parsers.booking_catalog_parser import BookingCatalogParser
from scrappers.scrapper import Scrapper

logger = logging.getLogger(__name__)


class BookingScrapper(Scrapper):
    _base_url = 'https://booking.com/searchresults.ru.html?'
    _hotels_per_page = 15

    def __init__(self, proxy=None, storage=None):
        super().__init__()
        self._proxy = proxy
        self._proxy_url = None
        self._storage = storage
        self._retries = 5
        self._links = []
        # Try to get list of Moscow hotels
        self._params = {
            'aid': 376376,
            'dest_id': -2960561,
            'dest_type': 'city',
            'rows': self._hotels_per_page,
            'offset': 0,
        }

    def scrap_process(self, limit=100):
        logging.info('Run scrap process with limit {}'.format(limit))

        while limit > 0:
            logging.info('Try to scrape hotels offset {}'.format(self._params['offset']))
            data = self.do_scrap(self._base_url, self._params)
            if not data:
                return False
            parser = BookingCatalogParser(data)
            for link in parser.catalog_links():
                res = self.scrap_hotel(link)
                if not res:
                    return False
                limit -= 1
                if limit == 0:
                    return True
                time.sleep(0.5)
            self._params['offset'] += self._hotels_per_page

    def scrap_hotel(self, url):
        file_name = self.get_slug_from_url(url)
        if file_name:
            if self._storage.has(file_name):
                logging.info('Skip hotel {}'.format(file_name))
                return True
            logging.info('Try to scrape hotel {}'.format(file_name))
            data = self.do_scrap(url)
            return self._storage.put(file_name, data)
        return False

    def do_scrap(self, url, params=None):
        if self._proxy and self._proxy_url is None:
            self.timeout = 5
            self._proxy_url = self._proxy.get_proxy()
            logging.info('Use proxy {}'.format(self._proxy_url))
            if self._proxy_url is None:
                logging.error('Proxy not found')
                return False

        logging.info('Try to scrape url {} | params {} | proxy {}'.format(url, params, self._proxy_url))

        try:
            return self._do_request(url, params, self._proxy_url)
        except (requests.ConnectionError, requests.ReadTimeout) as e:
            logging.error(e)
            if self._proxy:
                logging.info('Try to reconnect proxy {}'.format(self._proxy_url))
                if self._retries == 0:
                    logging.info('Ended attempts to proxy reconnect')
                    return False
                self._proxy.forget_proxy(self._proxy_url)
                self._retries -= 1
                self._proxy_url = None
                return self.do_scrap(url, params)
            else:
                return False
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    def get_slug_from_url(url):
        slug_search = re.search('https://booking\\.com/hotel/ru/([^#/]+)', url, re.IGNORECASE)

        if slug_search:
            return slug_search.group(1)
        return None
