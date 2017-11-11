import requests

from parsers.proxy_catalog_parser import ProxyCatalogParser
from scrappers.scrapper import Scrapper


class ProxyScrapper(Scrapper):
    _base_url = 'https://www.ip-adress.com/proxy-list'

    def __init__(self):
        super().__init__()
        self._except = []

    def get_proxy(self):
        data = self._do_request(self._base_url)
        parser = ProxyCatalogParser(data)
        for ip in parser.proxy_ips():
            url = 'http://{}'.format(ip)
            if url in self._except:
                continue
            try:
                self._do_request('https://ya.ru', proxy=url)
                return url
            except requests.ConnectionError:
                continue
        return None

    def forget_proxy(self, url):
        self._except.append(url)
