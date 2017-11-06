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

    def scrap_process(self, limit=30):
        logging.info('Run scrap process with limit {}'.format(limit))

        proxy = None
        if self._proxy:
            proxy = self._proxy.get_proxy()
            logging.info('Use proxy {}'.format(proxy))
            if proxy is None:
                logging.error('Proxy not found')
                return False

        while limit > 0:
            try:
                logging.info('Try to scrape hotels offset {} | proxy {}'.format(self._params['offset'], proxy))
                data = self._do_request(self._base_url, self._params, proxy)
                parser = BookingCatalogParser(data)
                for link in parser.catalog_links():
                    res = self.scrap_hotel(link, proxy)
                    if res:
                        limit -= 1
                    if limit == 0:
                        return True
                    time.sleep(0.5)
                self._params['offset'] += self._hotels_per_page
                time.sleep(0.5)
            except requests.ConnectionError as e:
                logging.error(e)
                if self._proxy:
                    logging.info('Try to reconnect proxy {}'.format(proxy))
                    if self._retries == 0:
                        return False
                    self._proxy.forget_proxy(proxy)
                    self._retries -= 1
                    return self.scrap_process(limit)
                else:
                    return False
            except Exception as e:
                logging.error(e)
                return False

    def scrap_hotel(self, url, proxy=None):
        logging.info('Try to scrape hotel {} | proxy {}'.format(url, proxy))
        file_name = self.get_slug_from_url(url)
        if file_name:
            if self._storage.has(file_name):
                logging.info('Skip hotel {}'.format(file_name))
                return True
            data = self._do_request(url, proxy=proxy)
            logging.info('Scrape hotel {}'.format(file_name))
            return self._storage.put(file_name, data)
        return False

    @staticmethod
    def get_slug_from_url(url):
        slug_search = re.search('https://booking\\.com/hotel/ru/([^#/]+)', url, re.IGNORECASE)

        if slug_search:
            return slug_search.group(1)
        return None
