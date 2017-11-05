import logging
import re

import requests
import time
from requests import RequestException

from decorators.decorators import retry
from parsers.booking_catalog_parser import BookingCatalogParser

logger = logging.getLogger(__name__)


class BookingScrapper:
    _base_url = 'https://booking.com/searchresults.ru.html?'
    _hotels_per_page = 15
    _headers = {
        'User-Agent': 'Hello my name is AI bot and I need some hotels from you:)'
    }

    def __init__(self, proxy=None, storage=None):
        self._proxy = proxy
        self._storage = storage
        self._retries = 5
        self._links = []
        self.timeout = 5

    def scrap_process(self, limit=10):
        # Try to get list of Moscow hotels
        params = {
            'aid': 376376,
            'dest_id': -2960561,
            'dest_type': 'city',
            'rows': self._hotels_per_page,
            'offset': 0,
        }

        proxy = None
        if self._proxy:
            proxy = self._proxy.get_proxy()
            logging.info('Use proxy {}'.format(proxy))
            if proxy is None:
                logging.error('Proxy not found')
                return False

        parser = BookingCatalogParser()

        while limit > 0:
            try:
                data = self._do_request(self._base_url, params, proxy)
                links = parser.get_catalog_links(data)
                if len(links) > limit:
                    links = links[:limit]
                    limit = 0
                else:
                    limit -= len(links)
                params['offset'] += self._hotels_per_page
                for link in links:
                    self.scrap_hotel(link, proxy)
                    time.sleep(0.5)
                time.sleep(0.5)
            except requests.ConnectionError as e:
                logging.error(e)
                if self._retries == 0:
                    return False
                self._proxy.forget_proxy(proxy)
                self._retries -= 1
                self.scrap_process(limit)
            except Exception as e:
                logging.error(e)
                return False
        return True

    def scrap_hotel(self, url, proxy=None):
        data = self._do_request(url, proxy=proxy)
        file_name = self.get_slug_from_url(url)
        if file_name:
            self._storage.put(file_name, data.replace('\n', ''))

    @retry(RequestException)
    def _do_request(self, url, params=None, proxy=None):
        response = requests.get(
            url,
            params=params,
            headers=self._headers,
            timeout=self.timeout,
            proxies={'https': proxy}
        )

        response.raise_for_status()

        return response.text

    @staticmethod
    def get_slug_from_url(url):
        slug_search = re.search('https://booking\\.com/hotel/ru/([^#/]+)', url, re.IGNORECASE)

        if slug_search:
            return slug_search.group(1)
        return None
